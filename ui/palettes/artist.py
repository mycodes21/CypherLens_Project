import customtkinter as ctk
from tkinter import colorchooser
from .base_palette import BasePalette

class ArtistBox(BasePalette):
    def __init__(self, parent):
        start_x = parent.winfo_x() + 50
        start_y = parent.winfo_y() + 500
        
        super().__init__(parent, title="Artist Studio", width=250, height=350, x=start_x, y=start_y, color_accent="#FF00FF")
        self.current_color = "#FF0000" # Default crvena
        self.setup_content()

    def setup_content(self):
        # Brush Size
        ctk.CTkLabel(self.content_frame, text="BRUSH SIZE", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(10, 5))
        self.slider_size = ctk.CTkSlider(self.content_frame, from_=1, to=50, number_of_steps=50, button_color="#FF00FF", progress_color="#FF00FF")
        self.slider_size.set(5)
        self.slider_size.pack(fill="x", pady=5)

        # Color Picker
        ctk.CTkLabel(self.content_frame, text="COLOR", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(20, 5))
        
        self.btn_color = ctk.CTkButton(
            self.content_frame, text="", width=100, height=50, 
            fg_color=self.current_color, border_width=2, border_color="white",
            command=self.pick_color
        )
        self.btn_color.pack(pady=5)
        ctk.CTkButton(self.content_frame, text="Pick Color", fg_color="#333", command=self.pick_color).pack()

        # Tools
        ctk.CTkLabel(self.content_frame, text="TOOLS", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(20, 5))
        self.btn_draw = ctk.CTkButton(self.content_frame, text="✏️ DRAW MODE", fg_color="#333", hover_color="#FF00FF", command=self.parent.toggle_drawing)
        self.btn_draw.pack(fill="x", pady=5)

    def pick_color(self):
        color = colorchooser.askcolor(title="Choose Brush Color")[1]
        if color:
            self.current_color = color
            self.btn_color.configure(fg_color=color)
            self.parent.brush_color = color