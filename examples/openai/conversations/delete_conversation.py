# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from rich import print

from examples import common

openai_client = common.build_openai_client()

deleted = openai_client.conversations.delete("conv_b485050b69e54a12ae82cb2688a7217d")
print(deleted)
