# Available Tools and Usage Guide

This repository uses a special tool interface. Below is a concise reference of all tools available in this environment, their purpose, key rules, and simple usage notes.

Important global rules
- OS: Windows. Use PowerShell-style commands when applicable and Windows path separators (\\).
- Don’t mix special tools with terminal commands in the same action. Use the right tool for the job (e.g., use search_project instead of find/grep).
- When a tool expects a file path, provide a direct path (no raw image bytes). 
- Keep changes minimal and focused on the described issue.

Tools catalog

1) functions.bash
- Purpose: Execute standard terminal commands (PowerShell) locally.
- Input: { command: string }
- Rules:
  - Use Windows PowerShell syntax.
  - Do NOT use it to create or open files (use create/open tools instead).
  - Avoid interactive commands (e.g., vim, python REPL).
  - Don’t combine with other special tools in the same command.
  - Prefer search_project over terminal find.
- Example: { "command": "dir" }

2) functions.search_project
- Purpose: Project-wide search (files, symbols, or exact text in files).
- Input: { search_term: string, path?: string }
- Behavior/Rules:
  - Case-insensitive.
  - Files: matches if all parts of search_term appear in the path.
  - Symbols: matches if all parts appear in the symbol’s name or FQN.
  - Text: exact phrase only (no fuzzy or wildcard within code text). Keep phrases short (2–3 words) for best results.
  - Provide path to narrow the scope when helpful.
- Examples:
  - search_term: "class User"
  - search_term: "MyFunction", path: "src\\module"

3) functions.get_file_structure
- Purpose: Quickly list a file’s structure (imports and symbol definitions with line ranges).
- Input: { file: string }
- Use to navigate before opening specific sections.

4) functions.open
- Purpose: Open 100 lines of a file starting at a given line.
- Input: { path: string, line_number?: number }
- Use together with get_file_structure/search_project to jump to relevant sections.

5) functions.open_entire_file
- Purpose: Attempt to open an entire file (use sparingly for large files).
- Input: { path: string }
- Use only when you really need the whole file content.

6) functions.scroll_down / functions.scroll_up
- Purpose: Move the current file view by 100 lines down or up.
- Input: none.

7) functions.create
- Purpose: Create a new file with given content (or fully rewrite a file created during the current session).
- Input: { filename: string, content: string }
- Rules:
  - Don’t include line numbers in content.
  - Don’t wrap content in triple quotes.
  - Don’t create files outside the repo.

8) functions.search_replace
- Purpose: Apply search-and-replace edits to an existing file.
- Input: { file_path: string, search: string, replace: string }
- Rules:
  - The search block must match existing lines exactly once (character-for-character, including comments, spacing, and newlines).
  - Use a concise but unique continuous block for search.
  - Don’t use partial line fragments for search.
  - No diff syntax (+/-), no escaping with backslashes.
  - For multiple edits, call the tool multiple times.

9) functions.undo_edit
- Purpose: Revert the last edit made to the project within the current session.
- Input: none.

10) functions.submit
- Purpose: Submit the final solution and end the session.
- Input: none.

11) functions.ask_user
- Purpose: Ask the user for clarification/unblockers.
- Input: { message: string }
- Tips: Be concise yet informative; explain what you need to proceed.

12) functions.run_test
- Purpose: Run unit tests (builds necessary components as needed).
- Input: { path: string, testName?: string }
- Rules:
  - Path can be: full path to test file(s), FQN of test class, or directory with tests.
  - Always provide full absolute or full relative path from repo root.
  - You can add debug logs inside tests (language-specific) with a [DEBUG_LOG] prefix.
- Examples:
  - path: "tests\\MyTest.kt"
  - path: "com.example.MyTest"
  - path: "D:\\abs\\path\\to\\tests"

13) functions.build
- Purpose: Build the entire project.
- Input: none.
- Notes:
  - Can be long. Prefer running specific tests that trigger builds when possible.
  - Not a substitute for verifying functionality.

Workflow and response formatting requirements
- Each assistant response must include exactly one <UPDATE> block (with <PREVIOUS_STEP>, <PLAN>, <NEXT_STEP>) followed immediately by a tool call.
- Keep the user informed: explain findings, plan, and immediate next action in every response.
- Use specialized tools when possible; don’t mix them with terminal commands.
- Follow Windows/PowerShell conventions and use backslashes in paths.

Current date/time reference: 2026-09-16 23:00 (local).
