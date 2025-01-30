<div align="center">

# Text Improvement Assistant

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=flat-square&logo=python)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-FF4B4B.svg?style=flat-square&logo=streamlit)](https://streamlit.io)
[![DSPy](https://img.shields.io/badge/DSPy-2.5.6-green.svg?style=flat-square)](https://dspy.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

## Overview

Text Improvement Assistant is an AI-powered tool that helps improve text quality using DSPy and large language models. It provides both a web interface (Streamlit) and CLI for text enhancement with reasoning and issue identification.

## Features

- 🌐 **Web Interface**: User-friendly Streamlit interface
- 🔄 **Multiple Completions**: Generate multiple improved versions
- 📝 **Example Management**: Save and edit example improvements
- 🤖 **DSPy Integration**: Leverages DSPy for LLM optimization
- 💻 **CLI Support**: Command-line interface for scripting

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/text_improvement.git
cd text_improvement

# Install dependencies
pip install -r requirements.txt

# Set up your OpenRouter API key
export OPENROUTER_API_KEY='your-api-key'
```

## Usage

### Web Interface

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

### Command Line

```bash
python main.py
```

Commands:
- `\note <text>`: Add instruction note
- `\add`: Add last run to examples

## Configuration

The system uses:
- DSPy with DeepSeek Chat model
- JSON storage for examples and instructions
- Streamlit for web interface
- Temperature of 1.5 for varied outputs

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
