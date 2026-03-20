# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

"""Demonstrates function-calling responses with multiple tools."""

import json

from openai.types.responses import ResponseFunctionToolCall
from openai.types.responses.response_input_param import FunctionCallOutput
from rich import print

from examples.agenthub.openai import common
from examples.fc_tools import execute_function_call, fc_tools

MODEL = "openai.gpt-4.1"


def main():
    openai_client = common.build_agenthub_client()

    # Creates first request
    response = openai_client.responses.create(
        model=MODEL,
        input="what is the weather in seattle?",
        previous_response_id=None,  # root of the history
        tools=fc_tools,
    )
    print(response.output)

    # Based on output if it is function call, execute the function and provide output back
    if isinstance(response.output[0], ResponseFunctionToolCall):
        obj = response.output[0]
        function_name = obj.name
        function_args = json.loads(obj.arguments)

        function_response = execute_function_call(function_name, function_args)

        response = openai_client.responses.create(
            model=MODEL,
            input=[
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=obj.call_id,
                    output=str(function_response),
                )
            ],
            previous_response_id=response.id,
            tools=fc_tools,
        )
        print(response.output)

    # Ask followup question related to previoud context
    response = openai_client.responses.create(
        model=MODEL,
        input="what clothes should i wear in this weather?",
        previous_response_id=response.id,
        tools=fc_tools,
    )
    print(response.output)

    # Based on FCTool execute the function tool output
    if isinstance(response.output[0], ResponseFunctionToolCall):
        obj = response.output[0]
        function_name = obj.name
        function_args = json.loads(obj.arguments)

        function_response = execute_function_call(function_name, function_args)

        response = openai_client.responses.create(
            model=MODEL,
            input=[
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=obj.call_id,
                    output=str(function_response),
                )
            ],
            previous_response_id=response.id,
            tools=fc_tools,
        )
        print(response.output)


if __name__ == "__main__":
    main()
