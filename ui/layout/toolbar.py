import customtkinter as ctk

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, width=50, fg_color="#2b2b2b", corner_radius=0)
        self.app = app_instance
        self.buttons = {}
        
        # Layout
        self.pack_propagate(False) 
        
        # --- 1. NAVIGACIJA & MOVE ---
        self._add_tool_btn("✋", "move", "Pan View (Pomeri pogled)")
        self._add_tool_btn("✥", "move_layer", "Move Layer (Pomeri sloj)") # NOVO
        
        # --- 2. CRTANJE & RETUŠIRANJE ---
        self._add_tool_btn("🖌️", "brush", "Brush Tool")      # NOVO
        self._add_tool_btn("🧽", "eraser", "Eraser Tool")    # NOVO
        self._add_tool_btn("🧪", "eyedropper", "Pick Color") # NOVO
        
        # --- 3. OBLICI ---
        self._add_tool_btn("✂️", "crop", "Crop Image")
        self._add_tool_btn("⬜", "rect", "Rectangle")
        self._add_tool_btn("⭕", "circle", "Circle")
        self._add_tool_btn("📏", "line", "Line") 
        
        # --- 4. MERENJE & TEKST ---
        self._add_tool_btn("📐", "ruler", "Measure Distance")
        self._add_tool_btn("T", "text", "Add Text")
        
    def _add_tool_btn(self, icon, tool_name, tooltip_text=""):
        # Koristimo okvir da bismo mogli kasnije dodati Tooltip ako treba
        btn = ctk.CTkButton(self, text=icon, width=40, height=40, 
                            fg_color="transparent", text_color="gray",
                            hover_color="#444",
                            font=("Arial", 18),
                            command=lambda t=tool_name: self.app.set_active_tool(t))
        btn.pack(pady=3, padx=5)
        self.buttons[tool_name] = btn

    def select_tool(self, tool_name):
        for name, btn in self.buttons.items():
            if name == tool_name:
                btn.configure(fg_color="#66FCF1", text_color="black")
            else:
                btn.configure(fg_color="transparent", text_color="gray")