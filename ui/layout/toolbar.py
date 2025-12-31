import customtkinter as ctk

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, width=50, fg_color="#2b2b2b", corner_radius=0)
        self.app = app_instance
        self.buttons = {}
        
        # Layout
        self.pack_propagate(False) # Fiksna širina
        
        # Alatke
        self._add_tool_btn("✋", "move")
        self._add_tool_btn("✏️", "draw") # Opciono, ako imaš draw tool
        self._add_tool_btn("✂️", "crop")
        self._add_tool_btn("📏", "ruler")
        
    def _add_tool_btn(self, icon, tool_name):
        btn = ctk.CTkButton(self, text=icon, width=40, height=40, 
                            fg_color="transparent", text_color="gray",
                            hover_color="#444",
                            font=("Arial", 20),
                            # KLJUČNO: Klik na dugme zove app.set_active_tool
                            command=lambda t=tool_name: self.app.set_active_tool(t))
        btn.pack(pady=5, padx=5)
        self.buttons[tool_name] = btn

    def select_tool(self, tool_name):
        """
        Samo vizuelno označava dugme. 
        NE SME DA ZOVE self.app.set_active_tool() JER TO PRAVI PETLJU!
        """
        # 1. Resetuj sva dugmad na sivo
        for name, btn in self.buttons.items():
            if name == tool_name:
                btn.configure(fg_color="#66FCF1", text_color="black") # Aktivno
            else:
                btn.configure(fg_color="transparent", text_color="gray") # Neaktivno
        
        # 2. OVDE JE BIO PROBLEM - OBRISALI SMO POZIV APP-U

    def select_tool(self, tool_name):
        # Resetuj boje svih dugmića
        for btn in self.buttons.values():
            btn.configure(fg_color="transparent", text_color="gray")
            
        # Oboj aktivno dugme
        if tool_name in self.buttons:
            self.buttons[tool_name].configure(fg_color="#66FCF1", text_color="black")
            
        # Javi aplikaciji da promeni alat
        self.app.set_active_tool(tool_name)