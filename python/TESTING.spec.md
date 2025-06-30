# Python CLI Testing Spec

This is a specification for Claude Code to generate all unit tests for the SpecTree Python CLI implementation, following a test-driven development approach.

## Instructions for Claude Code

1. First, read all documentation in the project root:
   - README.md (understanding what SpecTree is)
   - README.spec.md (implementation details and edge cases)
   - python/README.md (CLI interface specification)

2. Create a complete test suite based on this specification
3. All tests should initially fail (since no implementation exists yet)
4. Place all test files in `python/tests/`
5. Create any necessary test fixtures within the tests directory

## Testing Framework
- Use pytest for all tests
- Test files should be named `test_*.py`
- Place tests in `python/tests/` directory
- Run tests with: `pytest`

## Test Coverage Goals

Create comprehensive tests that verify:
- All behavior described in README.md works correctly
- All edge cases in README.spec.md are handled properly
- The CLI interface described in python/README.md works as expected

Focus on testing behavior, not implementation details. Each edge case in README.spec.md should have at least one corresponding test.