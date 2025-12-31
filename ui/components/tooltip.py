import customtkinter as ctk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        # Povezivanje događaja (Enter = miš ušao, Leave = miš izašao)
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        
        # Koordinate (malo ispod i desno od kursora)
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Kreiranje prozora bez okvira (overrideredirect)
        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Izgled label-a
        label = ctk.CTkLabel(self.tooltip_window, text=self.text, 
                             fg_color="#333", text_color="#FFF", 
                             corner_radius=5, padx=10, pady=5, font=("Arial", 10))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None