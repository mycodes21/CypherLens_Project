import customtkinter as ctk

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, width=50, fg_color="#2b2b2b", corner_radius=0)
        self.app = app_instance
        self.buttons = {}
        
        # Layout
        self.pack_propagate(False) 
        
        # --- ALATKE ---
        # Navigacija
        self._add_tool_btn("✋", "move")
        self._add_tool_btn("✂️", "crop")
        
        # Oblici i Crtanje
        self._add_tool_btn("✏️", "pencil")
        self._add_tool_btn("⬜", "rect")
        self._add_tool_btn("⭕", "circle")
        self._add_tool_btn("📏", "line") # Linija
        
        # Merenje i Tekst
        self._add_tool_btn("📐", "ruler")
        self._add_tool_btn("T", "text")
        
    def _add_tool_btn(self, icon, tool_name):
        btn = ctk.CTkButton(self, text=icon, width=40, height=40, 
                            fg_color="transparent", text_color="gray",
                            hover_color="#444",
                            font=("Arial", 20),
                            # KLJUČNO: Klikom zovemo set_active_tool
                            command=lambda t=tool_name: self.app.set_active_tool(t))
        btn.pack(pady=5, padx=5)
        self.buttons[tool_name] = btn

    def select_tool(self, tool_name):
        # Vizuelna promena (bez logike)
        for name, btn in self.buttons.items():
            if name == tool_name:
                btn.configure(fg_color="#66FCF1", text_color="black")
            else:
                btn.configure(fg_color="transparent", text_color="gray")