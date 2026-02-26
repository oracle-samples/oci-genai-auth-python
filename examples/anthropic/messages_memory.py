# Copyright (c) 2026 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/

from __future__ import annotations

from typing import Dict, List

from examples.anthropic.common import build_client, get_model

MEMORY_ROOT = "/memories"


def _normalize_path(path: str) -> str | None:
    if not path.startswith(MEMORY_ROOT):
        return None
    parts = [part for part in path.split("/") if part and part != "."]
    if ".." in parts:
        return None
    return "/" + "/".join(parts)


def _format_file_listing(memory_files: Dict[str, str]) -> str:
    if not memory_files:
        return "No stored memories yet."

    lines = ["Stored memories:"]
    for filename in sorted(memory_files):
        size = len(memory_files[filename].encode("utf-8"))
        lines.append(f"- {filename} ({size} bytes)")
    return "\n".join(lines)


def _format_file_content(file_text: str, view_range: List[int] | None) -> str:
    lines = file_text.splitlines()
    if view_range and len(view_range) == 2:
        start = max(1, view_range[0])
        end = min(len(lines), view_range[1])
        lines = lines[start - 1 : end]

    numbered = [f"{index + 1}: {line}" for index, line in enumerate(lines)]
    return "\n".join(numbered) if numbered else "(file is empty)"


def _handle_memory_command(memory_files: Dict[str, str], tool_input: dict) -> str:
    command = tool_input.get("command")
    raw_path = tool_input.get("path", "")
    path = _normalize_path(raw_path)

    if not command:
        return "Error: missing command in memory tool input."

    if not path:
        return f"Error: invalid path '{raw_path}'."

    if command == "view":
        if path == MEMORY_ROOT:
            return _format_file_listing(memory_files)
        if path not in memory_files:
            return f"Error: '{path}' not found."
        return _format_file_content(memory_files[path], tool_input.get("view_range"))

    if command == "create":
        if path in memory_files:
            return f"Error: '{path}' already exists."
        memory_files[path] = tool_input.get("file_text", "")
        return f"Created '{path}'."

    if command == "str_replace":
        if path not in memory_files:
            return f"Error: '{path}' not found."
        old = tool_input.get("old_str", "")
        new = tool_input.get("new_str", "")
        content = memory_files[path]
        count = content.count(old)
        if count == 0:
            return f"Error: '{old}' not found in '{path}'."
        if count > 1:
            return f"Error: '{old}' found {count} times in '{path}'."
        memory_files[path] = content.replace(old, new, 1)
        return f"Updated '{path}'."

    if command == "insert":
        if path not in memory_files:
            return f"Error: '{path}' not found."
        insert_line = tool_input.get("insert_line")
        if insert_line is None:
            return "Error: insert_line is required for insert."
        lines = memory_files[path].splitlines()
        index = max(0, min(len(lines), int(insert_line)))
        insert_text = tool_input.get("text", "")
        lines[index:index] = insert_text.splitlines() or [""]
        memory_files[path] = "\n".join(lines)
        return f"Inserted text into '{path}'."

    if command == "delete":
        if path == MEMORY_ROOT:
            memory_files.clear()
            return "Deleted all memories."
        if path not in memory_files:
            return f"Error: '{path}' not found."
        memory_files.pop(path)
        return f"Deleted '{path}'."

    if command == "rename":
        if path not in memory_files:
            return f"Error: '{path}' not found."
        new_path = _normalize_path(tool_input.get("new_path", ""))
        if not new_path:
            return "Error: new_path is required for rename."
        if new_path in memory_files:
            return f"Error: '{new_path}' already exists."
        memory_files[new_path] = memory_files.pop(path)
        return f"Renamed '{path}' to '{new_path}'."

    return f"Error: unsupported command '{command}'."


def main() -> None:
    client = build_client()
    memory_files: Dict[str, str] = {}

    messages = [
        {
            "role": "user",
            "content": "Remember that I prefer concise summaries and my favorite color is green.",
        }
    ]

    while True:
        response = client.beta.messages.create(
            model=get_model("claude-opus-4-6"),
            max_tokens=256,
            betas=["context-management-2025-06-27"],
            tools=[
                {
                    "type": "memory_20250818",
                    "name": "memory",
                }
            ],
            messages=messages,
        )

        print(response)

        if response.stop_reason != "tool_use":
            break

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if block.name != "memory":
                continue

            result = _handle_memory_command(memory_files, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                }
            )

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    main()
