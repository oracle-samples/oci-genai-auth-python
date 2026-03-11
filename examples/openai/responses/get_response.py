# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

retrieved_response = openai_client.responses.retrieve(
    response_id="resp_ord_yp5uu39vlnur5hdndgpsdqjp40eiurzij5lsrbu9z4cidb4l"
)
print(retrieved_response)
