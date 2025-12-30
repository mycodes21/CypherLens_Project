import pickle
from tkinter import filedialog, messagebox
from PIL import Image

class ProjectManager:
    @staticmethod
    def save_project(current_image, history, redo_stack):
        """
        Čuva celo stanje aplikacije u .clp fajl (CypherLens Project).
        Koristi pickle da 'zaledi' podatke.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".clp",
            filetypes=[("CypherLens Project", "*.clp")],
            title="Save Project"
        )
        
        if not file_path:
            return None

        # Pakujemo sve podatke u jedan rečnik (Dictionary)
        project_data = {
            "image": current_image,
            "history": history,
            "redo_stack": redo_stack
        }

        try:
            with open(file_path, "wb") as f:
                pickle.dump(project_data, f)
            print(f"Projekat sačuvan: {file_path}")
            return True
        except Exception as e:
            print(f"Greška pri čuvanju projekta: {e}")
            return False

    @staticmethod
    def load_project():
        """
        Učitava .clp fajl i vraća podatke nazad u aplikaciju.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("CypherLens Project", "*.clp")],
            title="Open Project"
        )

        if not file_path:
            return None

        try:
            with open(file_path, "rb") as f:
                data = pickle.load(f)
            return data # Vraća rečnik sa slikom i istorijom
        except Exception as e:
            print(f"Greška pri učitavanju projekta: {e}")
            return None

    @staticmethod
    def export_image(image):
        """
        Čuva SAMO trenutnu sliku u standardnom formatu (JPG, PNG...).
        """
        if not image:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("Bitmap", "*.bmp"),
                ("TIFF Image", "*.tiff")
            ],
            title="Export Image"
        )

        if file_path:
            try:
                # Ako je JPG, moramo konvertovati RGBA u RGB (jer JPG ne podržava providnost)
                if file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg"):
                    if image.mode == "RGBA":
                        rgb_im = image.convert("RGB")
                        rgb_im.save(file_path)
                    else:
                        image.save(file_path)
                else:
                    image.save(file_path)
                
                print(f"Slika exportovana: {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Neuspešan export: {e}")