# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

items = openai_client.conversations.items.list("conv_977e8f9d624849a79b8eca5e6d67f69a", limit=10)
print(items.data)
