# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from examples import common

MODEL = "claude-opus-4-6"


def _build_client():
    return common.build_anthropic_client()


def _handle_tool_use(block):
    if block.name == "client_tool_search":
        query = (block.input or {}).get("query", "").lower()
        references = []
        if "weather" in query:
            references.append({"type": "tool_reference", "tool_name": "get_weather"})
        if not references:
            return {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": "No matching tools found.",
            }
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": references,
        }

    if block.name == "get_weather":
        location = (block.input or {}).get("location", "unknown location")
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": f"Weather in {location}: 62F and sunny.",
        }

    return {
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": f"Unhandled tool '{block.name}'.",
    }


def main() -> None:
    client = _build_client()

    tools = [
        {
            "name": "client_tool_search",
            "description": "Search for a relevant tool by keyword.",
            "input_schema": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
        {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "defer_loading": True,
            "input_schema": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
            },
        },
    ]

    messages = [
        {
            "role": "user",
            "content": "What is the weather in Seattle?",
        }
    ]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=256,
            system="Use client_tool_search to discover tools before calling them.",
            messages=messages,
            tools=tools,
            tool_choice={"type": "auto"},
        )

        print(response.model_dump_json(indent=2))

        if response.stop_reason != "tool_use":
            break

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            tool_results.append(_handle_tool_use(block))

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    main()
