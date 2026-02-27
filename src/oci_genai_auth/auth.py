# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Generator, Mapping, Optional, Type

import httpx
import oci
import requests
from oci.config import DEFAULT_LOCATION, DEFAULT_PROFILE
from typing_extensions import override

logger = logging.getLogger(__name__)

OciAuthSigner = Type[oci.signer.AbstractBaseSigner]


class HttpxOciAuth(httpx.Auth, ABC):
    """
    Enhanced custom HTTPX authentication class that implements OCI request signing
    with auto-refresh.

    This class handles the authentication flow for HTTPX requests by signing them
    using the OCI Signer, which adds the necessary authentication headers for OCI API calls.
    It also provides automatic token refresh functionality for token-based authentication methods.
    Attributes:
        signer (oci.signer.Signer): The OCI signer instance used for request signing
        refresh_interval: Seconds between token refreshes (default: 3600 - 1 hour)
        _lock: Threading lock for thread-safe token refresh
        _last_refresh: Last refresh timestamp
    """

    def __init__(self, signer: OciAuthSigner, refresh_interval: int = 3600):
        """
        Initialize the authentication with a signer and refresh configuration.
        Args:
            signer: OCI signer instance
            refresh_interval: Seconds between token refreshes (default: 3600 - 1 hour)
        """
        self.signer = signer
        self.refresh_interval = refresh_interval
        self._lock = threading.Lock()
        self._last_refresh: Optional[float] = time.time()
        logger.info(
            "Initialized %s with refresh interval: %d seconds",
            self.__class__.__name__,
            refresh_interval,
        )

    def _should_refresh_token(self) -> bool:
        """
        Check if the token should be refreshed based on time interval.
        Returns:
            bool: True if token should be refreshed, False otherwise
        """
        if not self._last_refresh:
            return True
        current_time = time.time()
        return (current_time - self._last_refresh) >= self.refresh_interval

    @abstractmethod
    def _refresh_signer(self) -> None:
        """
        Abstract method to refresh the signer. Must be implemented by subclasses.
        This method should create a new signer instance with fresh credentials/tokens.
        """
        pass

    def _refresh_if_needed(self) -> None:
        """
        Refresh the signer if enough time has passed since last refresh.
        This method is thread-safe and will only refresh once per interval.
        """
        with self._lock:
            if self._should_refresh_token():
                logger.info("Time interval reached, refreshing %s ...", self.__class__.__name__)
                try:
                    self._refresh_signer()
                    self._last_refresh = time.time()
                    logger.info("%s token refresh completed successfully", self.__class__.__name__)
                except Exception as e:
                    logger.exception("Warning: Token refresh failed:", e)

    def _sign_request(self, request: httpx.Request, content: bytes) -> None:
        """
        Sign the given HTTPX request with the OCI signer using the provided content.
        Updates request.headers in place with the signed headers.
        """
        # Strip any SDK auth headers to avoid conflicting with OCI signing.
        request.headers.pop("Authorization", None)
        request.headers.pop("X-Api-Key", None)
        request.headers.pop("x-goog-api-key", None)

        # Remove Google API key query parameter if present.
        params = list(request.url.params.multi_items())
        if params:
            filtered = [(key, value) for key, value in params if key.lower() != "key"]
            if len(filtered) != len(params):
                request.url = request.url.copy_with(params=filtered)
        req = requests.Request(
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers),
            data=content,
        )
        prepared_request = req.prepare()
        self.signer.do_request_sign(prepared_request)  # type: ignore
        request.headers.update(prepared_request.headers)

    @override
    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """
        Authentication flow for HTTPX requests with automatic retry on 401 errors.
        This method:
        1. Checks if token needs refresh and refreshes if necessary
        2. Signs the request using OCI signer
        3. Yields the signed request
        4. If 401 error is received, attempts token refresh and retries once
        Args:
            request: The HTTPX request to be authenticated
        Yields:
            httpx.Request: The authenticated request
        """
        # Check and refresh token if needed
        self._refresh_if_needed()

        # Read the request content to handle streaming requests properly
        try:
            content = request.content
        except httpx.RequestNotRead:
            # For streaming requests, we need to read the content first
            content = request.read()

        self._sign_request(request, content)

        response = yield request

        # If we get a 401 (Unauthorized), try refreshing the token once and retry
        if response.status_code == 401:
            logger.info("Received 401 Unauthorized, attempting token refresh and retry...")
            with self._lock:
                try:
                    self._refresh_signer()
                    self._last_refresh = time.time()
                    self._sign_request(request, content)
                    yield request
                except Exception as e:
                    logger.exception("Token refresh on 401 failed:", e)


class OciSessionAuth(HttpxOciAuth):
    """
    OCI authentication implementation using session-based authentication.

    This class implements OCI authentication using a session token and private key
    loaded from the OCI configuration file. It's suitable for interactive user sessions.

    Attributes:
        signer (oci.auth.signers.SecurityTokenSigner): OCI signer using session token
    """

    def __init__(
        self,
        config_file: str = DEFAULT_LOCATION,
        profile_name: str = DEFAULT_PROFILE,
        refresh_interval: int = 3600,
        **kwargs: Mapping[str, Any],
    ):
        """
        Initialize a Security Token-based OCI signer.

        Parameters
        ----------
        config_file : str, optional
            Path to the OCI configuration file. Defaults to `~/.oci/config`.
        profile_name : str, optional
            Profile name inside the OCI configuration file to use.
            Defaults to "DEFAULT".
        refresh_interval:  int, optional
            Seconds between token refreshes (default: 3600 - 1 hour)
        **kwargs : Mapping[str, Any]
            Optional keyword arguments:
              - `generic_headers`: Optional[Dict[str, str]]
                    Headers to be used for generic requests.
                    Default: `["date", "(request-target)", "host"]`
              - `body_headers`: Optional[Dict[str, str]]
                    Headers to be used for signed request bodies.
                    Default: `["content-length", "content-type", "x-content-sha256"]`

        Raises
        ------
        oci.exceptions.ConfigFileNotFound
            If the configuration file cannot be found.
        KeyError
            If a required key such as `"key_file"` is missing in the config.
        Exception
            For any other initialization errors.
        """
        # Load OCI configuration and token
        self.config_file = config_file
        self.profile_name = profile_name
        config = oci.config.from_file(config_file, profile_name)
        token = self._load_token(config)

        # Load the private key from config
        key_path = config.get("key_file")
        if not key_path:
            raise KeyError(f"Missing 'key_file' entry in OCI config profile '{profile_name}'.")
        private_key = self._load_private_key(config)

        # Optional signer header customization
        generic_headers = kwargs.pop("generic_headers", None)
        body_headers = kwargs.pop("body_headers", None)

        additional_kwargs = {}
        if generic_headers:
            additional_kwargs["generic_headers"] = generic_headers
        if body_headers:
            additional_kwargs["body_headers"] = body_headers

        self.additional_kwargs = additional_kwargs
        signer = oci.auth.signers.SecurityTokenSigner(token, private_key, **self.additional_kwargs)
        super().__init__(signer=signer, refresh_interval=refresh_interval)

    def _load_token(self, config: Mapping[str, Any]) -> str:
        """
        Load session token from file specified in configuration.
        Args:
            config: OCI configuration dictionary
        Returns:
            str: Session token content
        """
        token_file = config["security_token_file"]
        with open(token_file, "r") as f:
            return f.read().strip()

    def _load_private_key(self, config: Any) -> str:
        """
        Load private key from file specified in configuration.
        Args:
            config: OCI configuration dictionary
        Returns:
            Private key object
        """
        return oci.signer.load_private_key_from_file(config["key_file"])

    def _refresh_signer(self) -> None:
        """
        Refresh the session signer by reloading token and private key.
        This method creates a new SecurityTokenSigner with fresh credentials
        loaded from the configuration files.
        """
        # Reload configuration in case it has changed
        config = oci.config.from_file(self.config_file, self.profile_name)
        token = self._load_token(config)
        private_key = self._load_private_key(config)
        self.signer = oci.auth.signers.SecurityTokenSigner(
            token, private_key, **self.additional_kwargs
        )


class OciResourcePrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using Resource Principal authentication with auto-refresh.

    This class implements OCI authentication using Resource Principal credentials,
    which is suitable for services running within OCI (like Functions, Container Instances)
    that need to access other OCI services. The resource principal token is automatically
    refreshed at specified intervals.
    """

    def __init__(self, refresh_interval: int = 3600, **kwargs: Any) -> None:
        """
        Initialize resource principal authentication.
        Args:
            refresh_interval: Seconds between token refreshes (default: 3600 - 1 hour)
            **kwargs: Additional arguments passed to the resource principal signer
        """
        self.kwargs = kwargs
        signer = oci.auth.signers.get_resource_principals_signer(**kwargs)
        super().__init__(signer=signer, refresh_interval=refresh_interval)

    def _refresh_signer(self) -> None:
        """
        Refresh the resource principal signer.
        This method creates a new resource principal signer which will
        automatically fetch fresh credentials from the OCI metadata service.
        """
        self.signer = oci.auth.signers.get_resource_principals_signer(**self.kwargs)


class OciInstancePrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using Instance Principal authentication with auto-refresh.

    This class implements OCI authentication using Instance Principal credentials,
    which is suitable for compute instances that need to access OCI services.
    The instance principal token is automatically refreshed at specified intervals.
    """

    def __init__(self, refresh_interval: int = 3600, **kwargs) -> None:  # noqa: ANN003
        """
        Initialize instance principal authentication.
        Args:
            refresh_interval: Seconds between token refreshes (default: 3600 - 1 hour)
            **kwargs: Additional arguments passed to InstancePrincipalsSecurityTokenSigner
        """
        self.kwargs = kwargs
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner(**kwargs)
        super().__init__(signer=signer, refresh_interval=refresh_interval)

    def _refresh_signer(self) -> None:
        """
        Refresh the instance principal signer.
        This method creates a new InstancePrincipalsSecurityTokenSigner which will
        automatically fetch fresh credentials from the OCI metadata service.
        """
        self.signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner(**self.kwargs)


class OciUserPrincipalAuth(HttpxOciAuth):
    """
    OCI authentication implementation using user principal authentication with auto-refresh.

    This class implements OCI authentication using API Key credentials loaded from
    the OCI configuration file. It's suitable for programmatic access to OCI services.
    Since API key authentication doesn't use tokens that expire, this class doesn't
    need frequent refresh but supports configuration reload at specified intervals.
    Attributes:
        config_file (str): Path to OCI configuration file
        profile_name (str): Profile name in the configuration file
        config (dict): OCI configuration dictionary
    """

    def __init__(
        self,
        config_file: str = DEFAULT_LOCATION,
        profile_name: str = DEFAULT_PROFILE,
        refresh_interval: int = 3600,
    ) -> None:
        """
        Initialize user principal authentication.
        Args:
            config_file: Path to OCI config file (default: ~/.oci/config)
            profile_name: Profile name to use (default: DEFAULT)
            refresh_interval: Seconds between config reloads (default: 3600 - 1 hour)
        """
        self.config_file = config_file
        self.profile_name = profile_name
        self.config = oci.config.from_file(config_file, profile_name)
        oci.config.validate_config(self.config)
        signer = oci.signer.Signer(
            tenancy=self.config["tenancy"],
            user=self.config["user"],
            fingerprint=self.config["fingerprint"],
            private_key_file_location=self.config.get("key_file"),
            pass_phrase=oci.config.get_config_value_or_default(self.config, "pass_phrase"),
            private_key_content=self.config.get("key_content"),
        )
        super().__init__(signer=signer, refresh_interval=refresh_interval)

    def _refresh_signer(self) -> None:
        """
        Refresh the user principal signer.
        For API key authentication, this recreates the signer with the same credentials.
        This is mainly useful if the configuration file has been updated.
        """
        # Reload configuration in case it has changed
        self.config = oci.config.from_file(self.config_file, self.profile_name)
        oci.config.validate_config(self.config)
        self.signer = oci.signer.Signer(
            tenancy=self.config["tenancy"],
            user=self.config["user"],
            fingerprint=self.config["fingerprint"],
            private_key_file_location=self.config.get("key_file"),
            pass_phrase=oci.config.get_config_value_or_default(self.config, "pass_phrase"),
            private_key_content=self.config.get("key_content"),
        )
