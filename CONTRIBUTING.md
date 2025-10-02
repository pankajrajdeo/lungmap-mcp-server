# Contributing to LungMAP MCP Server

Thank you for your interest in contributing to the LungMAP MCP Server! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/lungmap-mcp-server.git
cd lungmap-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run tests
python scripts/test_server.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write descriptive docstrings for functions and classes
- Keep functions focused and small

## Testing

Before submitting a pull request:

1. Run the test suite:
   ```bash
   python scripts/test_server.py
   ```

2. Test with Claude Desktop if possible
3. Test with LangChain integration if applicable

## Documentation

- Update relevant documentation when adding new features
- Include examples in docstrings
- Update README.md if needed
- Add or update configuration examples in `docs/mcp_config_examples.json`

## Pull Request Process

1. Ensure your branch is up to date with main
2. Write clear commit messages
3. Include a description of changes in your PR
4. Reference any related issues
5. Ensure all tests pass

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Feature Requests

Feature requests are welcome! Please:

- Check existing issues first
- Provide a clear description of the feature
- Explain the use case
- Consider implementation complexity

## Questions?

Feel free to open an issue for questions about contributing or using the project.
