# Contributing / Style Guide

This is a small sample style guide the **Style subagent** should read
(via Bob's document understanding) and check PRs against.

## Naming conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

## Docstrings
- Every public function must have a docstring describing what it does.

## Imports
- No unused imports.
- Standard library imports first, then third-party, then local imports.

## Strings
- Use double quotes `"..."` consistently, not a mix of single and double.

## Secrets
- Never hardcode credentials, API keys, or passwords in source code.
  Use environment variables or a secrets manager.

## Testing
- Every new function should have at least one corresponding unit test
  in `tests/`.
