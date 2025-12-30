import customtkinter as ctk

class BasePalette(ctk.CTkFrame):
    # Dodali smo 'app_instance=None' u __init__
    def __init__(self, parent, title, width=200, height=400, x=0, y=0, color_accent="#66FCF1", app_instance=None):
        super().__init__(parent, width=width, height=height, fg_color="#1a1a1a", corner_radius=0)
        
        # GLAVNA POPRAVKA:
        # Ako smo prosledili 'app_instance' (glavni prozor), onda je on self.parent (logički).
        # Ako nismo, probaj da nađeš glavni prozor preko winfo_toplevel().
        if app_instance:
            self.parent = app_instance
        else:
            self.parent = self.winfo_toplevel()

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)