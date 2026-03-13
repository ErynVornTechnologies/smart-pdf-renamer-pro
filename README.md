# 📄 Smart PDF Renamer Pro (AI-Powered)

Automate the boring task of renaming messy PDF invoices and documents. This tool uses AI to analyze document content and suggest standardized, logical filenames.

## 🌟 Features

- **AI Content Analysis**: Reads the first page of your PDF to understand what the document is.
- **Smart Naming**: Automatically formats names to `YYYY-MM-DD_Company_Invoice.pdf`.
- **Multi-Provider LLM**: Choose from Gemini, OpenAI, Anthropic, LM Studio, or OpenRouter.
- **Modern GUI**: Built with `customtkinter` for a sleek, professional dark-mode experience.
- **Bulk Processing**: Process hundreds of files with one click.
- **Safety First**: Uses a source and destination folder to keep your original files untouched.
- **AI Agent Friendly**: Optimised for autonomous agents (Gemini, Claude, AntiGravity) to set up and run.

## 🛠️ Prerequisites

- Python 3.10+
- An API key for at least one LLM provider (see below)

## 🚀 Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/HappyBirdProduction/smart-pdf-renamer-pro.git
   cd smart-pdf-renamer-pro
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   - Copy `.env.example` to `.env`
   - Set your preferred `LLM_PROVIDER` and the corresponding API key:

   ```env
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=your-api-key-here
   ```

### Supported LLM Providers

| Provider | Env Variable | Default Model |
| --- | --- | --- |
| Google Gemini | `GOOGLE_API_KEY` | `gemini-2.5-flash` |
| OpenAI | `OPENAI_API_KEY` | `gpt-4o-mini` |
| Anthropic | `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` |
| LM Studio (local) | `LMSTUDIO_URL` | `local-model` |
| OpenRouter | `OPENROUTER_API_KEY` | `gemini-2.0-flash-exp:free` |

## 🎮 How to Use

1. Run `python renamer.py`
2. **Select Source Folder** — the folder with messy PDF files.
3. **Select Destination** — where renamed files should be saved.
4. **Click START RENAMING** — watch the AI process your documents in real-time.

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| API Key error | Check your `.env` file and make sure the correct key is set |
| PDF not recognized | Ensure the PDF contains selectable text (not a scanned image) |

---
*Brought to you by [aiBlackBox](https://aiblackbox.co.uk/). Follow us on [LinkedIn](https://www.linkedin.com/in/kamil-krzysztof-nagorski/) for more AI toolkits.*
