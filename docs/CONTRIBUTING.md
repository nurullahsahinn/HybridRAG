# 🤝 Contributing to Smart RAG Chatbot

Thank you for your interest in contributing! This project welcomes contributions from everyone.

## How to Contribute

### 🐛 Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/YOUR_USERNAME/smart-rag-chatbot/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs

### 💡 Suggesting Features

1. Check existing [Issues](https://github.com/YOUR_USERNAME/smart-rag-chatbot/issues) for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### 🔧 Pull Requests

1. **Fork the repository**
2. **Create a branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add amazing feature"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/smart-rag-chatbot.git
cd smart-rag-chatbot

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black isort flake8 mypy

# Run tests
pytest
```

## Code Style

### Python Style Guide
- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Write docstrings (Google style)

### Tools
```bash
# Format code
black .
isort .

# Lint
flake8 .

# Type check
mypy .
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific tests
pytest tests/test_validation.py -v
```

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Maintenance tasks

### Examples
```
feat: add support for PDF documents

Implements PDF loading and processing using PyPDF2.
Includes tests and documentation.

Closes #123
```

## Project Structure

Key directories:
- `main.py` - Core RAG engine
- `utils/` - Utility modules
- `tests/` - Test files
- `docs/` - Documentation

## Questions?

Feel free to open an issue or reach out!

