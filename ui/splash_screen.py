import customtkinter as ctk

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True) # Sklanja window bar (frameless)
        
        # Centriranje
        w, h = 600, 350
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.configure(fg_color="#0B0C10")
        
        # Logo / Naslov
        ctk.CTkLabel(self, text="CYPHERLENS", font=("Impact", 48), text_color="#66FCF1").place(relx=0.5, rely=0.3, anchor="center")
        ctk.CTkLabel(self, text="Industrial Image Engineering", font=("Arial", 14), text_color="gray").place(relx=0.5, rely=0.45, anchor="center")
        
        # Verzija
        ctk.CTkLabel(self, text="v10.0 Enterprise", font=("Arial", 10), text_color="#333").place(relx=0.95, rely=0.95, anchor="se")

        # Loading Bar
        self.progress = ctk.CTkProgressBar(self, width=400, height=4, progress_color="#66FCF1")
        self.progress.place(relx=0.5, rely=0.7, anchor="center")
        self.progress.set(0)
        
        self.status_lbl = ctk.CTkLabel(self, text="Initializing...", font=("Consolas", 10), text_color="gray")
        self.status_lbl.place(relx=0.5, rely=0.75, anchor="center")

        # --- LOGIKA UČITAVANJA (BEZ THREADING-A) ---
        self.loading_steps = [
            "Loading Torch Engines...", 
            "Initializing AI Models...", 
            "Loading UI Components...", 
            "Calibrating G-Code Engine...", 
            "Connecting Layer Manager...",
            "Ready!"
        ]
        self.step_index = 0
        
        # Pokreni simulaciju učitavanja posle 500ms
        self.after(500, self.process_loading_step)

    def process_loading_step(self):
        if self.step_index < len(self.loading_steps):
            # Ažuriraj tekst i progres
            step_text = self.loading_steps[self.step_index]
            self.status_lbl.configure(text=step_text)
            
            progress_val = (self.step_index + 1) / len(self.loading_steps)
            self.progress.set(progress_val)
            
            self.step_index += 1
            
            # Zakaži sledeći korak za 600ms (brzina učitavanja)
            self.after(600, self.process_loading_step)
        else:
            # Kraj - zatvori splash
            self.destroy()