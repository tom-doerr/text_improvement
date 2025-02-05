<div align="center">

# Text Improvement Assistant

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=flat-square&logo=python)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-FF4B4B.svg?style=flat-square&logo=streamlit)](https://streamlit.io)
[![DSPy](https://img.shields.io/badge/DSPy-2.5.6-green.svg?style=flat-square)](https://dspy.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

## Overview

Text Improvement Assistant is an AI-powered tool that helps improve text quality using DSPy and large language models. It provides a web interface for text enhancement with reasoning and issue identification.

## Features

- 🌐 **Web Interface**: User-friendly Streamlit interface
- 🔄 **Multiple Completions**: Generate multiple improved versions
- 📝 **Example Management**: Save and edit example improvements
- 🤖 **DSPy Integration**: Leverages DSPy for LLM optimization
- 🔍 **Detailed Analysis**: Provides reasoning and identifies issues

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

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Configuration

The system uses:
- DSPy with Claude 3.5 Sonnet model
- JSON storage for examples and instructions
- Streamlit for web interface
- Temperature of 2.0 for varied outputs

## Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

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
