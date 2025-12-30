import customtkinter as ctk
import webbrowser

class CoffeeModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Support Development")
        
        w, h = 400, 250
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.resizable(False, False)
        
        # Učini ga modalnim (blokira ostale prozore)
        self.transient(parent)
        self.grab_set()
        
        ctk.CTkLabel(self, text="☕", font=("Arial", 64)).pack(pady=(20, 10))
        ctk.CTkLabel(self, text="Enjoying CypherLens?", font=("Arial", 18, "bold")).pack()
        ctk.CTkLabel(self, text="This is a free open-source tool.\nIf it helps your business, consider buying me a coffee!", 
                     font=("Arial", 12), text_color="gray").pack(pady=10)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Maybe Later", fg_color="transparent", border_width=1, 
                      text_color="gray", command=self.destroy).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="Buy Coffee 💖", fg_color="#FFDD00", text_color="black", hover_color="#E6C200",
                      command=self.open_link).pack(side="left", padx=10)

    def open_link(self):
        webbrowser.open("https://buymeacoffee.com/mycodes21")
        self.destroy()