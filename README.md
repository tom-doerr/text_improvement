<h1 align="center">Text Improvement Assistant</h1>

<p align="center">
    <a href="https://github.com/tom-doerr/text_improvement/stargazers"
        ><img
            src="https://img.shields.io/github/stars/tom-doerr/text_improvement?colorA=2c2837&colorB=c9cbff&style=for-the-badge&logo=starship"
            alt="Repository's starts"
    /></a>
    <a href="https://github.com/tom-doerr/text_improvement/issues"
        ><img
            src="https://img.shields.io/github/issues-raw/tom-doerr/text_improvement?colorA=2c2837&colorB=f2cdcd&style=for-the-badge&logo=starship"
            alt="Issues"
    /></a>
    <a href="https://github.com/tom-doerr/text_improvement/blob/main/LICENSE"
        ><img
            src="https://img.shields.io/github/license/tom-doerr/text_improvement?colorA=2c2837&colorB=b5e8e0&style=for-the-badge&logo=starship"
            alt="License"
    /><br />
    <a href="https://github.com/tom-doerr/text_improvement/commits/main"
        ><img
            src="https://img.shields.io/github/last-commit/tom-doerr/text_improvement/main?colorA=2c2837&colorB=ddb6f2&style=for-the-badge&logo=starship"
            alt="Latest commit"
    /></a>
    <a href="https://github.com/tom-doerr/text_improvement"
        ><img
            src="https://img.shields.io/github/repo-size/tom-doerr/text_improvement?colorA=2c2837&colorB=89DCEB&style=for-the-badge&logo=starship"
            alt="GitHub repository size"
    /></a>
</p>


## Overview

Text Improvement Assistant is an AI-powered tool that helps improve text quality using DSPy and large language models. It provides a web interface for text enhancement with reasoning and issue identification.

### How it Works

The assistant uses a few-shot learning approach to improve text quality:

1. **Examples**: You can save example improvements that demonstrate the kind of changes you want. Each example contains:
   - Original input text
   - Reasoning behind the changes
   - Issues identified
   - Improved version

2. **Learning**: When improving new text, the system:
   - Uses your saved examples to understand your style preferences
   - Applies similar improvement patterns to new inputs
   - Provides detailed reasoning for changes
   - Identifies potential issues
   - Generates improved versions

3. **Customization**: You can:
   - Add successful improvements as new examples
   - Edit existing examples
   - Provide custom instructions
   - Generate multiple variations

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
