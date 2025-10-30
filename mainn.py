from typing import List
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from google.generativeai import configure, GenerativeModel

# Configure Gemini API
configure(api_key="AIzaSyBsKfY9T6DyA-d9dcoN69rE5sZXrJXTwmk")
gemini_model = GenerativeModel("gemini-2.0-flash")

# Available Personas
PERSONAS = {
    "elon": "Elon Musk",
    "ratan": "Ratan Tata",
    "steve": "Steve Jobs"
}

def generate_advisory(persona_id: str, message: str) -> str:
    prompt = f"""
        You are {PERSONAS[persona_id]}, a legendary business leader and startup advisor.
        For EVERY input, always respond in this format:

        Advice Topic: <One-line title about the advice>
        1. <First step or key action, in detail>
        2. <Second actionable step>
        3. <Third step>
        4. <...continue to 6+ steps if possible...>

        End with a two-line motivational summary.

        Do NOT skip steps. Do NOT provide only a title or a short reply. Break down the answer, no matter how basic the question.
        User's question:
        {message}
        """
    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response else "⚠️ No response received, please try again."
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"


class AdviserUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Advisory Desktop App")
        self.geometry("900x700")
        self.configure(bg="#f0f8ff")
        self.setup_widgets()

    def setup_widgets(self):
        # Persona Selection
        ttk.Label(self, text="Select Advisor Persona:", font=("Arial", 14, "bold"), background="#f0f8ff").pack(pady=8)
        self.persona_var = tk.StringVar(value="elon")
        persona_menu = ttk.OptionMenu(self, self.persona_var, "elon", *PERSONAS.keys(), 
                                     command=lambda _: self.persona_var.set(_))
        persona_menu.pack(pady=5)

        # Query Input
        ttk.Label(self, text="Enter Your Question:", font=("Arial", 14, "bold"), background="#f0f8ff").pack(pady=8)
        self.query_entry = tk.Text(self, height=5, font=("Arial", 12))
        self.query_entry.pack(padx=20, pady=5, fill=tk.X)

        # Submit Button
        submit_btn = ttk.Button(self, text="Get Advisory Response", command=self.get_response)
        submit_btn.pack(pady=15)

        # Scrollable Response Output
        self.result_text = scrolledtext.ScrolledText(self, font=("Arial", 12), state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(padx=20, pady=10, expand=True, fill=tk.BOTH)

        # Configure tags for styling
        self.result_text.tag_config("heading", foreground="#0047AB", font=("Arial", 14, "bold"))
        self.result_text.tag_config("point", foreground="#228B22", font=("Arial", 12))
        self.result_text.tag_config("bold", font=("Arial", 12, "bold"))

    def get_response(self):
        persona_id = self.persona_var.get()
        message = self.query_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Input Error", "Please enter a valid query.")
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "Generating response...\n")
        self.result_text.config(state=tk.DISABLED)

        self.after(100, lambda: self.fetch_response(persona_id, message))

    def fetch_response(self, persona_id, message):
        response_text = generate_advisory(persona_id, message)
        self.display_response(response_text)

    def display_response(self, text: str):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        # Simple parser: split by lines, highlight headings and numbered bullets
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line.endswith(":") or line.startswith("•") or line[0].isdigit():
                self.result_text.insert(tk.END, line + "\n", "heading")
            elif line.startswith("- ") or line.startswith("* ") or line.startswith("• "):
                self.result_text.insert(tk.END, " • " + line[2:] + "\n", "point")
            else:
                self.result_text.insert(tk.END, line + "\n")
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = AdviserUI()
    app.mainloop()
