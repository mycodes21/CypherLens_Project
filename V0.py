import customtkinter as ctk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageFilter, ImageOps
import io
import threading # Da interfejs ne blokira dok AI radi

# --- PODEŠAVANJA DIZAJNA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") # Možeš probati i "green" ili "blue"

class ModernStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup prozora
        self.title("Studio Pro - AI Background Tool")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Promenljive
        self.original_image = None
        self.processed_image = None
        self.is_processing = False

        # --- LAYOUT (GRID) ---
        self.grid_columnconfigure(1, weight=1) # Desna strana se širi
        self.grid_rowconfigure(0, weight=1)

        # --- LEVI MENI (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1) # Spacer na dnu

        # Logo / Naslov
        self.logo_label = ctk.CTkLabel(self.sidebar, text="STUDIO PRO", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Dugme za upload
        self.btn_upload = ctk.CTkButton(self.sidebar, text="Učitaj Sliku", command=self.select_image, height=40, font=ctk.CTkFont(weight="bold"))
        self.btn_upload.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Separator
        ctk.CTkLabel(self.sidebar, text="OPCIJE OBRADE", text_color="gray").grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")

        # Opcije (Switches)
        self.switch_white_bg = ctk.CTkSwitch(self.sidebar, text="Bela Pozadina (Shop)")
        self.switch_white_bg.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.switch_shadow = ctk.CTkSwitch(self.sidebar, text="Dodaj Senku (Drop Shadow)")
        self.switch_shadow.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Dugme za ponovnu obradu (ako promeniš opcije)
        self.btn_reprocess = ctk.CTkButton(self.sidebar, text="Osveži Prikaz", command=self.start_processing_thread, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.btn_reprocess.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        
        # Spacer
        self.label_status = ctk.CTkLabel(self.sidebar, text="Spremno", anchor="w", text_color="gray")
        self.label_status.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        # --- DESNA STRANA (PREVIEW) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Image Container
        self.image_display = ctk.CTkLabel(self.main_frame, text="Učitaj sliku da počneš", font=ctk.CTkFont(size=16), fg_color=("gray85", "gray17"), corner_radius=15)
        self.image_display.pack(expand=True, fill="both", pady=(0, 20))

        # Progress Bar (Indeterminate)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=10)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.pack_forget() # Sakrij dok ne zatreba

        # Save Button (Veliko dugme dole desno)
        self.btn_save = ctk.CTkButton(self.main_frame, text="SAČUVAJ REZULTAT", command=self.save_image, height=50, fg_color="#2CC985", font=ctk.CTkFont(size=15, weight="bold"), state="disabled")
        self.btn_save.pack(fill="x")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp")])
        if file_path:
            self.original_image = Image.open(file_path)
            # Prikaz originala odmah
            self.display_image(self.original_image)
            # Pokreni obradu
            self.start_processing_thread()

    def start_processing_thread(self):
        if not self.original_image:
            return
        
        if self.is_processing:
            return

        self.is_processing = True
        self.btn_save.configure(state="disabled")
        self.label_status.configure(text="AI Obrađuje sliku...", text_color="#3B8ED0")
        
        # Animacija progress bara
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.start()

        # Pokretanje u novom threadu da UI ne zablokira
        threading.Thread(target=self.process_image, daemon=True).start()

    def process_image(self):
        try:
            # 1. REMBG - Uklanjanje pozadine
            # alpha_matting poboljšava ivice, ali je sporije. Ovde koristimo default za brzinu.
            no_bg = remove(self.original_image)

            final_img = no_bg

            # 2. PRODUCT STUDIO LOGIKA
            
            # Ako treba senka
            if self.switch_shadow.get() == 1:
                final_img = self.add_drop_shadow(final_img)

            # Ako treba bela pozadina
            if self.switch_white_bg.get() == 1:
                new_bg = Image.new("RGBA", final_img.size, "WHITE")
                new_bg.paste(final_img, (0, 0), final_img)
                final_img = new_bg.convert("RGB") # Konvertuj u RGB jer JPG ne podržava transparenciju
            
            self.processed_image = final_img
            
            # Vraćanje na glavni thread za update UI-a
            self.after(0, self.update_ui_success)

        except Exception as e:
            print(e)
            self.after(0, lambda: messagebox.showerror("Greška", str(e)))
            self.is_processing = False

    def add_drop_shadow(self, image, offset=(15, 15), background_color=0, shadow_color=0, blur=20):
        # Kreiranje senke na osnovu alpha kanala slike
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Izdvoji alpha kanal (oblik objekta)
        alpha = image.split()[3]
        
        # Napravi praznu sliku za senku, malo veću da senka ne bude isečena
        total_width = image.width + abs(offset[0]) + 2*blur
        total_height = image.height + abs(offset[1]) + 2*blur
        
        shadow = Image.new('RGBA', (total_width, total_height), (0,0,0,0))
        
        # Pozicioniraj crnu siluetu
        shadow_left = blur + max(offset[0], 0)
        shadow_top = blur + max(offset[1], 0)
        
        # Nalepi siluetu (koristimo alpha kao masku da obojimo u crno/sivo)
        shadow.paste((0,0,0, 100), (shadow_left, shadow_top), mask=alpha)
        
        # Zamuti senku
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
        
        # Nalepi originalnu sliku preko senke
        img_left = blur - min(offset[0], 0)
        img_top = blur - min(offset[1], 0)
        
        shadow.paste(image, (img_left, img_top), image)
        
        # Kropuj nazad na originalne dimenzije (ili zadrži veće ako želiš padding)
        return shadow.crop((img_left, img_top, img_left + image.width, img_top + image.height))

    def update_ui_success(self):
        self.display_image(self.processed_image)
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.label_status.configure(text="Obrada završena.", text_color="green")
        self.btn_save.configure(state="normal")
        self.is_processing = False

    def display_image(self, img_obj):
        # Pametno skaliranje za prikaz
        display_width = self.main_frame.winfo_width() - 40
        display_height = self.main_frame.winfo_height() - 100
        
        if display_width < 100 or display_height < 100: 
            display_width, display_height = 500, 500

        # Zadrži aspect ratio
        ratio = min(display_width / img_obj.width, display_height / img_obj.height)
        new_size = (int(img_obj.width * ratio), int(img_obj.height * ratio))
        
        preview = ctk.CTkImage(light_image=img_obj, dark_image=img_obj, size=new_size)
        self.image_display.configure(image=preview, text="")

    def save_image(self):
        if not self.processed_image:
            return
            
        file_types = [("PNG Image", "*.png")]
        default_ext = ".png"
        
        # Ako je bela pozadina, nudimo i JPG
        if self.switch_white_bg.get() == 1:
            file_types.append(("JPEG Image", "*.jpg"))
        
        path = filedialog.asksaveasfilename(defaultextension=default_ext, filetypes=file_types)
        
        if path:
            self.processed_image.save(path)
            messagebox.showinfo("Sačuvano", f"Slika sačuvana na:\n{path}")

if __name__ == "__main__":
    app = ModernStudioApp()
    app.mainloop()