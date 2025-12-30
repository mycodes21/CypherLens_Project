import customtkinter as ctk
from .base_palette import BasePalette

class Toolbar(BasePalette):
    def __init__(self, parent):
        # Pozicioniranje
        start_x = parent.winfo_x() + 20
        start_y = parent.winfo_y() + 100
        
        # Malo viša paleta jer imamo dosta alata
        super().__init__(parent, title="Tools", width=80, height=520, x=start_x, y=start_y)
        
        self.active_tool = None
        self.buttons = {}
        self.setup_content()

    def setup_content(self):
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # DEFINICIJA SVIH ALATA
        tools = [
            ("✋", "move"),       ("🖌️", "brush"),
            ("✏️", "pencil"),     ("➖", "line"),  
            ("⬜", "rect"),       ("⭕", "circle"),
            ("T", "text"),        ("📏", "ruler"), # <--- NOVO
            ("✂️", "crop"),       ("🪄", "magic"),
            ("👻", "remove_bg"),  ("💾", "save")
        ]

        row = 0
        col = 0
        for icon, tool_name in tools:
            btn = ctk.CTkButton(
                self.content_frame, 
                text=icon, 
                width=35, height=35, 
                font=("Arial", 16, "bold"), 
                fg_color="#333", 
                hover_color="#66FCF1",
                corner_radius=5,
                command=lambda t=tool_name: self.select_tool(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.buttons[tool_name] = btn
            
            col += 1
            if col > 1:
                col = 0
                row += 1

    def select_tool(self, tool_name):
        # Resetuj boje svih dugmića
        for name, btn in self.buttons.items():
            btn.configure(fg_color="#333", text_color="white")
        
        # Oboj aktivni
        if tool_name in self.buttons:
            self.buttons[tool_name].configure(fg_color="#66FCF1", text_color="black")
        
        self.active_tool = tool_name
        # Javi glavnom prozoru
        self.parent.set_active_tool(tool_name)