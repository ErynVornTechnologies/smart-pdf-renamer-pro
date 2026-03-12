# 📄 Smart PDF Renamer Pro (AI-Powered)

Automate the boring task of renaming messy PDF invoices and documents. This tool uses **Google Gemini AI** to analyze document content and suggest standardized, logical filenames.

![App Screenshot](https://aiblackbox.co.uk/wp-content/uploads/2025/08/AIBLACKBOX-logonowe_.png)

## 🌟 Features

- **AI Content Analysis**: Reads the first page of your PDF to understand what the document is.
- **Smart Naming**: Automatically formats names to `YYYY-MM-DD_Company_Invoice.pdf`.
- **Modern GUI**: Built with `customtkinter` for a sleek, professional dark-mode experience.
- **Bulk Processing**: Process hundreds of files with one click.
- **Safety First**: Uses a source and destination folder to keep your original files untouched.

## 🛠️ Requirements

- Windows 10/11
- Python 3.10 or higher
- Google Gemini API Key

## 🚀 Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/smart-pdf-renamer.git
   cd smart-pdf-renamer
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key:**
   - Create a file named `.env` in the root folder.
   - Add your Gemini API key:

     ```env
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

## 🎮 How to Use

1. **Run the application:**

   ```bash
   python renamer.py
   ```

2. **Select Source Folder**: Pick the folder containing your messy PDF files.
3. **Select Destination**: Pick where the renamed files should be saved.
4. **Click START RENAMING**: Watch the AI process your documents in real-time.

## 📝 Disclaimer

This tool uses AI to analyze document content. While highly accurate, always verify important documents. Created for educational and productivity purposes.

---
Brought to you by **[AiBlackBox](https://aiblackbox.co.uk/)**.  
Follow us on **[LinkedIn](https://www.linkedin.com/in/kamil-krzysztof-nagorski/)** for more AI toolkits and autonomous engineering insights.
