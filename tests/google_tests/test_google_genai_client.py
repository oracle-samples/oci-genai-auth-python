from types import SimpleNamespace
from unittest.mock import MagicMock

import httpx
import pytest


class DummyAuth(httpx.Auth):
    def auth_flow(self, request):  # type: ignore[override]
        yield request


def test_builds_http_options(monkeypatch):
    genai = pytest.importorskip("google.genai")
    from oci_genai_support.google import COMPARTMENT_ID_HEADER, OciGoogleGenAI

    captured = {}
    fake_models = SimpleNamespace(
        generate_content=MagicMock(return_value="ok"),
        generate_images=MagicMock(return_value="ok"),
    )

    class FakeClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.models = fake_models

    monkeypatch.setattr(genai, "Client", FakeClient)

    auth = DummyAuth()
    client = OciGoogleGenAI(
        auth=auth,
        base_url="https://example.com",
        compartment_id="ocid1.compartment.oc1..dummy",
        headers={"X-Test": "1"},
    )

    http_options = captured["http_options"]
    assert http_options.base_url == "https://example.com"
    assert http_options.headers[COMPARTMENT_ID_HEADER] == "ocid1.compartment.oc1..dummy"
    assert http_options.headers["X-Test"] == "1"
    assert http_options.client_args["auth"] is auth
    assert http_options.async_client_args["auth"] is auth

    assert client.client.models is fake_models


def test_generate_helpers(monkeypatch):
    genai = pytest.importorskip("google.genai")
    from oci_genai_support.google import OciGoogleGenAI

    fake_models = SimpleNamespace(
        generate_content=MagicMock(return_value="content"),
        generate_images=MagicMock(return_value="images"),
    )

    class FakeClient:
        def __init__(self, **kwargs):
            self.models = fake_models

    monkeypatch.setattr(genai, "Client", FakeClient)

    client = OciGoogleGenAI(
        auth=DummyAuth(),
        base_url="https://example.com",
    )

    result = client.generate_content(model="gemini-2.0-flash-001", contents="hello")
    assert result == "content"
    fake_models.generate_content.assert_called_once_with(
        model="gemini-2.0-flash-001",
        contents="hello",
    )

    result = client.generate_images(model="imagen-3.0-generate-002", prompt="dragon")
    assert result == "images"
    fake_models.generate_images.assert_called_once_with(
        model="imagen-3.0-generate-002",
        prompt="dragon",
    )

    result = client.generate_image(model="imagen-3.0-generate-002", prompt="dragon")
    assert result == "images"
    assert fake_models.generate_images.call_count == 2


def test_api_key_passthrough(monkeypatch):
    genai = pytest.importorskip("google.genai")
    from oci_genai_support.google import OciGoogleGenAI

    captured = {}
    fake_models = SimpleNamespace(
        generate_content=MagicMock(return_value="content"),
        generate_images=MagicMock(return_value="images"),
    )

    class FakeClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.models = fake_models

    monkeypatch.setattr(genai, "Client", FakeClient)

    client = OciGoogleGenAI(
        auth=None,
        base_url="https://example.com",
        vertexai=False,
        api_key="test-key",
    )

    assert captured["api_key"] == "test-key"
    assert captured["vertexai"] is False
    assert "auth" not in captured["http_options"].client_args
    assert "auth" not in captured["http_options"].async_client_args

    result = client.generate_content(model="gemini-2.0-flash-001", contents="hello")
    assert result == "content"
