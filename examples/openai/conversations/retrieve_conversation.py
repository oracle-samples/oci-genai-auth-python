# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

conversation = openai_client.conversations.retrieve(
    "conv_ord_wypqdfsxjfygwh0w4n5w00c3ucomut08y1p5zsogz3o709ug"
)
print(conversation)
