import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class NewProjectDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.title("New Project")
        self.geometry("400x450")
        self.resizable(False, False)
        
        # Centriranje
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 225
            self.geometry(f"+{int(x)}+{int(y)}")
        except:
            pass # Ako ne uspe centriranje, nema veze
        
        self.transient(parent)
        self.grab_set()
        self.configure(fg_color="#1F2833")

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="CREATE NEW PROJECT", font=("Arial", 16, "bold"), text_color="#66FCF1").pack(pady=(20, 30))

        # Inputs
        self.entry_width = self.create_input("Width (px):", "1920")
        self.entry_height = self.create_input("Height (px):", "1080")

        # Background Type
        ctk.CTkLabel(self, text="Background:", text_color="gray").pack(pady=(10, 5))
        self.bg_var = ctk.StringVar(value="White")
        
        bg_frame = ctk.CTkFrame(self, fg_color="transparent")
        bg_frame.pack(pady=5)
        
        ctk.CTkRadioButton(bg_frame, text="White", variable=self.bg_var, value="White", text_color="white").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(bg_frame, text="Transparent", variable=self.bg_var, value="Transparent", text_color="white").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(bg_frame, text="Black", variable=self.bg_var, value="Black", text_color="white").pack(anchor="w", pady=2)

        # Buttons
        ctk.CTkButton(self, text="CREATE", fg_color="#66FCF1", text_color="black", height=40, width=200, command=self.create_project).pack(pady=(40, 10))
        ctk.CTkButton(self, text="CANCEL", fg_color="#333", text_color="white", width=200, command=self.destroy).pack()

    def create_input(self, label, default):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(pady=5)
        ctk.CTkLabel(f, text=label, width=100, anchor="e", text_color="#C5C6C7").pack(side="left", padx=10)
        entry = ctk.CTkEntry(f, width=150)
        entry.insert(0, default)
        entry.pack(side="left")
        return entry

    def create_project(self):
        try:
            # 1. Provera unosa
            w_str = self.entry_width.get()
            h_str = self.entry_height.get()
            
            if not w_str.isdigit() or not h_str.isdigit():
                messagebox.showerror("Error", "Dimensions must be whole numbers!")
                return

            w = int(w_str)
            h = int(h_str)
            
            if w <= 0 or h <= 0:
                messagebox.showerror("Error", "Dimensions must be larger than 0!")
                return

            # 2. Kreiranje slike
            bg_type = self.bg_var.get()
            color = (255, 255, 255, 255) # White
            if bg_type == "Black": color = (0, 0, 0, 255)
            elif bg_type == "Transparent": color = (0, 0, 0, 0)

            new_img = Image.new("RGBA", (w, h), color)
            
            # 3. Slanje u glavni prozor
            if hasattr(self.parent, 'set_new_project'):
                self.parent.set_new_project(new_img)
                self.destroy() # Zatvori prozor
            else:
                messagebox.showerror("Critical Error", "Main Window is missing 'set_new_project' function!")
            
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to create project:\n{e}")
            print(f"Error detail: {e}")