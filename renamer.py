import os
import threading
import shutil
import requests
from dotenv import load_dotenv
import pdfplumber
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
import webbrowser

# Load environment variables
load_dotenv()

# ===== LLM PROVIDER CONFIGURATION =====
# Set LLM_PROVIDER in your .env file or change here directly.
# Supported: "gemini", "openai", "anthropic", "lmstudio", "openrouter"
PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

# API Keys — set these in your .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Model names per provider — customize as needed
MODELS = {
    "gemini": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
    "lmstudio": os.getenv("LMSTUDIO_MODEL", "local-model"),
    "openrouter": os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free"),
}

LOGO_URL = "https://aiblackbox.co.uk/wp-content/uploads/2025/08/AIBLACKBOX-logonowe_.png"

# Appearance Configuration
ctk.set_appearance_mode("Dark")


def call_llm(prompt):
    """Route prompt to the configured LLM provider. Returns response text."""
    model_name = MODELS.get(PROVIDER, "")

    if PROVIDER == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()

    elif PROVIDER in ("openai", "lmstudio", "openrouter"):
        from openai import OpenAI
        if PROVIDER == "openai":
            client = OpenAI(api_key=OPENAI_API_KEY)
        elif PROVIDER == "lmstudio":
            client = OpenAI(base_url=LMSTUDIO_URL, api_key="lm-studio")
        else:
            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    elif PROVIDER == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

    else:
        raise ValueError(f"Unknown LLM provider: {PROVIDER}. Use: gemini, openai, anthropic, lmstudio, openrouter")


class PDFRenamerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Basic Window Configuration
        self.title("Smart PDF Renamer Pro")
        self.geometry("850x1000") 
        self.resizable(False, False)
        
        # Color matching
        self.bg_color = "#20212b"
        self.container_color = "#363847"
        self.accent_color = "#34ade1"
        self.text_color = "#ffffff"
        self.gray_text = "#9ea0a9"
        
        self.configure(fg_color=self.bg_color)

        # Variables
        self.input_path = ""
        self.output_path = ""
        
        self.create_widgets()

    def create_widgets(self):
        # --- Logo ---
        try:
            logo_response = requests.get(LOGO_URL, stream=True)
            img = Image.open(logo_response.raw)
            logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            self.label_logo = ctk.CTkLabel(self, image=logo_img, text="")
        except Exception:
            self.label_logo = ctk.CTkLabel(self, text="AI BlackBox", font=("Montserrat", 40, "bold"))
            
        self.label_logo.pack(pady=(50, 10))
        self.label_logo.bind("<Button-1>", lambda e: webbrowser.open("https://aiblackbox.co.uk/"))
        self.label_logo.configure(cursor="hand2")

        # --- Header Title ---
        self.lbl_header = ctk.CTkLabel(
            self, 
            text="AI-Powered Bulk PDF Invoices Renaming Tool", 
            font=("Montserrat", 26),
            text_color=self.text_color
        )
        self.lbl_header.pack(pady=(0, 40))

        # --- Folders Section ---
        self.folders_container = ctk.CTkFrame(self, fg_color=self.container_color, corner_radius=15, width=720, height=180)
        self.folders_container.pack(pady=10, padx=65, fill="x")
        self.folders_container.pack_propagate(False)

        # Source Folder Row
        self.source_frame = ctk.CTkFrame(self.folders_container, fg_color="transparent")
        self.source_frame.pack(fill="x", pady=(35, 10), padx=40)
        
        self.btn_input = ctk.CTkButton(
            self.source_frame, 
            text="Select Source Folder", 
            command=self.select_input, 
            width=220, 
            height=38,
            font=("Roboto", 18),
            fg_color=self.accent_color, 
            hover_color="#298cb5",
            corner_radius=8
        )
        self.btn_input.pack(side="left")
        
        self.lbl_input = ctk.CTkLabel(self.source_frame, text="No source selected", font=("Roboto", 18), text_color=self.gray_text)
        self.lbl_input.pack(side="right", padx=10)

        # Destination Folder Row
        self.dest_frame = ctk.CTkFrame(self.folders_container, fg_color="transparent")
        self.dest_frame.pack(fill="x", pady=10, padx=40)
        
        self.btn_output = ctk.CTkButton(
            self.dest_frame, 
            text="Select Destination", 
            command=self.select_output, 
            width=220, 
            height=38,
            font=("Roboto", 18),
            fg_color=self.accent_color, 
            hover_color="#298cb5",
            corner_radius=8
        )
        self.btn_output.pack(side="left")
        
        self.lbl_output = ctk.CTkLabel(self.dest_frame, text="No destination selected", font=("Roboto", 18), text_color=self.gray_text)
        self.lbl_output.pack(side="right", padx=10)

        # --- Progress ---
        self.progress_bar = ctk.CTkProgressBar(self, width=650, height=10, fg_color="#3d3f4b", progress_color=self.accent_color)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(60, 10))

        self.lbl_status = ctk.CTkLabel(self, text="READY", font=("Montserrat", 24), text_color=self.text_color)
        self.lbl_status.pack(pady=5)

        # --- Log Box ---
        self.log_box = ctk.CTkTextbox(
            self, 
            width=720, 
            height=130,
            font=("Consolas", 12), 
            fg_color="#000000", 
            text_color="#4ade80",
            border_width=0,
            corner_radius=10
        )
        self.log_box.pack(pady=20, padx=65)
        self.log_box.configure(state="disabled")

        # --- Action Button ---
        self.btn_start = ctk.CTkButton(
            self, 
            text="START RENAMING", 
            command=self.start_process_thread, 
            width=300, 
            height=60, 
            font=("Montserrat", 24), 
            fg_color=self.accent_color, 
            hover_color="#298cb5",
            corner_radius=10
        )
        self.btn_start.pack(pady=(10, 50))

        # --- Footer ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(side="bottom", pady=20)

        self.lbl_disclaimer = ctk.CTkLabel(
            self.footer_frame, 
            text="Disclaimer: This tool uses AI to analyze document content. Always verify results.", 
            font=("Roboto", 10), 
            text_color=self.gray_text
        )
        self.lbl_disclaimer.pack()

        self.links_frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        self.links_frame.pack(pady=(5, 0))

        self.lbl_f1 = ctk.CTkLabel(self.links_frame, text="Brought to you by ", font=("Roboto", 11), text_color=self.gray_text)
        self.lbl_f1.pack(side="left")
        
        self.lbl_link1 = ctk.CTkLabel(self.links_frame, text="AiBlackBox.", font=("Roboto", 11, "bold"), text_color=self.accent_color, cursor="hand2")
        self.lbl_link1.pack(side="left")
        self.lbl_link1.bind("<Button-1>", lambda e: webbrowser.open("https://aiblackbox.co.uk/"))

        self.lbl_f2 = ctk.CTkLabel(self.links_frame, text=" Follow us for more AI toolkits and autonomous engineering insights at ", font=("Roboto", 11), text_color=self.gray_text)
        self.lbl_f2.pack(side="left")

        self.lbl_link2 = ctk.CTkLabel(self.links_frame, text="LinkedIn.", font=("Roboto", 11, "bold"), text_color=self.accent_color, cursor="hand2")
        self.lbl_link2.pack(side="left")
        self.lbl_link2.bind("<Button-1>", lambda e: webbrowser.open("https://www.linkedin.com/in/kamil-krzysztof-nagorski/"))

    # --- Logic ---

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def select_input(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_path = folder
            self.lbl_input.configure(text=f"...{folder[-30:]}" if len(folder) > 30 else folder)

    def select_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path = folder
            self.lbl_output.configure(text=f"...{folder[-30:]}" if len(folder) > 30 else folder)

    def start_process_thread(self):
        if not GOOGLE_API_KEY and PROVIDER == "gemini":
            messagebox.showerror("Error", "API Key not found! Please provide it in .env file.")
            return
        if not self.input_path or not self.output_path:
            messagebox.showwarning("Warning", "Please select folders first.")
            return

        self.btn_start.configure(state="disabled", text="PROCESSING...")
        self.progress_bar.set(0)
        threading.Thread(target=self.process_files, daemon=True).start()

    def get_ai_name(self, text):
        if not text: return None
        try:
            prompt = (
                "Analyze the following text from an invoice document and suggest a standardized filename in the format: "
                "YYYY-MM-DD_Company_Invoice.pdf. Return ONLY the filename, nothing else.\n\n"
                f"Text extract:\n{text[:2000]}"
            )
            return call_llm(prompt)
        except Exception as e:
            self.log(f"LLM Error ({PROVIDER}): {str(e)}")
            return None

    def extract_text(self, pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if pdf.pages:
                    return pdf.pages[0].extract_text()
        except Exception as e:
            self.log(f"Error reading {os.path.basename(pdf_path)}: {str(e)}")
        return ""

    def process_files(self):
        files = [f for f in os.listdir(self.input_path) if f.lower().endswith('.pdf')]
        if not files:
            self.after(0, lambda: messagebox.showinfo("Info", "No PDF files found."))
            self.after(0, lambda: self.btn_start.configure(state="normal", text="START RENAMING"))
            return

        total = len(files)
        for i, filename in enumerate(files):
            self.after(0, lambda v=(i+1)/total, s=f"PROCESSING {i+1}/{total}": (self.progress_bar.set(v), self.lbl_status.configure(text=s)))
            
            old_path = os.path.join(self.input_path, filename)
            self.log(f"Analyzing: {filename}")
            
            text = self.extract_text(old_path)
            new_name = self.get_ai_name(text)
            
            if new_name:
                new_name = new_name.replace("```", "").replace("`", "").strip()
                if not new_name.lower().endswith('.pdf'): new_name += ".pdf"
                new_name = "".join([c for c in new_name if c.isalnum() or c in "._- "]).strip()
                
                new_path = os.path.join(self.output_path, new_name)
                try:
                    shutil.copy(old_path, new_path)
                    self.log(f"SUCCESS: -> {new_name}")
                except Exception as e:
                    self.log(f"COPY FAILED: {str(e)}")
            else:
                self.log(f"SKIPPED: {filename}")

        self.after(0, lambda: (
            self.progress_bar.set(1),
            self.lbl_status.configure(text="FINISHED!"),
            self.btn_start.configure(state="normal", text="START RENAMING"),
            messagebox.showinfo("Success", f"Processed {total} files.")
        ))

if __name__ == "__main__":
    app = PDFRenamerApp()
    app.mainloop()
