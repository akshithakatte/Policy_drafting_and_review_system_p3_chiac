# Policy Drafting and Review System

An AI-powered system for automated policy drafting, legal review, risk assessment, and iterative revision. This application leverages large language models to create comprehensive policy documents with built-in validation and quality scoring.

## Features

- **Automated Policy Drafting**: Generate initial policy drafts based on topics and requirements
- **Legal Review**: AI-powered legal compliance analysis and feedback
- **Risk Assessment**: Identify potential risks and compliance issues
- **Iterative Revision**: Multiple rounds of policy improvement based on feedback
- **Validation Checklist**: Ensure policies meet standard criteria
- **Quality Scoring**: Automated scoring of policy quality and completeness
- **Web Interface**: Streamlit-based user interface for easy interaction
- **Export Functionality**: Save policies and feedback in multiple formats
- **Diff Viewer**: Track changes between policy iterations

## Architecture

The system consists of several specialized agents:

- **PolicyDrafter**: Creates initial policy drafts
- **LegalReviewer**: Provides legal compliance feedback
- **RiskAuditor**: Identifies potential risks and issues
- **Reviser**: Incorporates feedback to improve policies
- **ValidationChecklist**: Ensures policy completeness
- **PolicyScorer**: Evaluates policy quality

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/akshithakatte/Policy_drafting_and_review_system_p3_chiac.git
   cd Policy_drafting_and_review_system_p3_chiac
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   GROQ_BASE_URL=https://api.groq.com/openai/v1
   LLM_MODEL=llama-3.3-70b-versatile
   ```

   Get your free Groq API key at: https://console.groq.com/keys

## Usage

### Web Interface

1. **Start the Streamlit application**
   ```bash
   streamlit run ui.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Use the interface** to:
   - Enter policy topics and requirements
   - Configure the number of iterations
   - View real-time progress and results
   - Download generated policies

### Command Line Interface

1. **Run the demo script**
   ```bash
   python demo.py
   ```

2. **Use the main application programmatically**
   ```python
   from app import PolicyDraftingSystem
   
   system = PolicyDraftingSystem()
   policy = system.run_workflow(
       topic="Data Privacy Policy",
       requirements="GDPR compliance required",
       iterations=2
   )
   ```

## Project Structure

```
policy_draft_and_review_agent_p3_chiac/
├── agents/                    # AI agents for different tasks
│   ├── policy_drafter.py     # Initial policy generation
│   ├── legal_reviewer.py     # Legal compliance analysis
│   ├── risk_auditor.py       # Risk assessment
│   ├── reviser.py           # Policy revision
│   └── validation_checklist.py # Policy validation
├── utils/                    # Utility modules
│   ├── diff_viewer.py       # Compare policy versions
│   ├── file_exporter.py     # Export functionality
│   └── scorer.py           # Policy quality scoring
├── exports/                 # Generated policies and feedback
├── app.py                   # Main application logic
├── ui.py                    # Streamlit web interface
├── config.py                # Configuration and API keys
├── demo.py                  # Demo script
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (create this)
```

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_BASE_URL`: Groq API base URL (optional, defaults to official endpoint)
- `LLM_MODEL`: Language model to use (optional, defaults to `llama-3.3-70b-versatile`)

### Model Options

The system supports various Groq models:
- `llama-3.3-70b-versatile` (default)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

## Output Formats

The system generates several types of output:

- **Policy drafts**: Complete policy documents in `.txt` format
- **Legal feedback**: Detailed legal analysis and recommendations
- **Risk assessments**: Risk identification and mitigation suggestions
- **Diff reports**: Side-by-side comparison of policy versions
- **Quality scores**: Numerical evaluation of policy quality

All outputs are saved in the `exports/` directory with timestamps for version control.

## Example Workflow

1. **Input**: "Create a Data Privacy Policy with GDPR compliance"
2. **Draft**: System generates initial policy draft
3. **Review**: Legal reviewer analyzes compliance
4. **Audit**: Risk auditor identifies potential issues
5. **Revise**: System incorporates feedback
6. **Validate**: Checklist ensures completeness
7. **Score**: Quality assessment provided
8. **Export**: Final policy and all feedback saved

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section below

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `GROQ_API_KEY` is correctly set in the `.env` file
2. **Model Not Available**: Try switching to a different model in the configuration
3. **Slow Performance**: Consider using a smaller model for faster responses
4. **Export Errors**: Check that the `exports/` directory has write permissions

### Getting Help

- Review the configuration section above
- Check the Groq API documentation: https://console.groq.com/docs
- Open an issue with detailed error information

## Acknowledgments

- Groq for providing fast, reliable language model inference
- Streamlit for the web interface framework
- OpenAI for the API compatibility layer
