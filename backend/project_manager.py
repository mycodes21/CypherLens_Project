import json
import os
import zipfile
import io
from PIL import Image
from tkinter import messagebox

class ProjectManager:
    @staticmethod
    def save_project(layer_manager, filepath):
        """
        Čuva projekat kao ZIP arhivu (.cph).
        Sada čuva i KOORDINATE (x, y) i TRANSFORMACIJE (scale, rotation).
        """
        try:
            with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
                metadata = []
                
                for index, layer in enumerate(layer_manager.layers):
                    # 1. Sačuvaj sliku
                    img_filename = f"layer_{index}.png"
                    img_byte_arr = io.BytesIO()
                    layer.image.save(img_byte_arr, format='PNG')
                    zf.writestr(img_filename, img_byte_arr.getvalue())
                    
                    # 2. Pripremi podatke za JSON (DODALI SMO NOVE PROMENLJIVE)
                    layer_data = {
                        "name": layer.name,
                        "visible": layer.visible,
                        "opacity": layer.opacity,
                        "image_file": img_filename,
                        # --- NOVI PODACI ---
                        "x": getattr(layer, 'x', 0),
                        "y": getattr(layer, 'y', 0),
                        "scale": getattr(layer, 'scale', 1.0),
                        "rotation": getattr(layer, 'rotation', 0)
                    }
                    metadata.append(layer_data)
                
                # 3. Sačuvaj JSON
                zf.writestr('project.json', json.dumps(metadata, indent=4))
                
            print(f"Project saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"Save Error: {e}")
            return False

    @staticmethod
    def load_project(filepath, layer_manager):
        """
        Učitava .cph fajl i popunjava slojeve.
        Otporan na stare fajlove koji nemaju x/y podatke.
        """
        try:
            with zipfile.ZipFile(filepath, 'r') as zf:
                if 'project.json' not in zf.namelist():
                    raise ValueError("Invalid project file: missing project.json")
                
                json_data = zf.read('project.json')
                metadata = json.loads(json_data)
                
                # Očisti trenutne slojeve
                layer_manager.layers = []
                layer_manager.active_index = -1
                
                for data in metadata:
                    img_file = data['image_file']
                    img_data = zf.read(img_file)
                    
                    image = Image.open(io.BytesIO(img_data)).convert("RGBA")
                    
                    # Dodaj sloj (add_layer ne vraća objekat u tvojoj verziji, pa ga uzimamo iz liste)
                    layer_manager.add_layer(image, data['name'])
                    new_layer = layer_manager.layers[-1] # Uzmi poslednji dodati
                    
                    # Vrati podešavanja (koristimo .get() za kompatibilnost sa starim fajlovima)
                    new_layer.visible = data.get('visible', True)
                    new_layer.opacity = data.get('opacity', 255)
                    
                    # --- NOVI PODACI (sa default vrednostima da ne pukne stari fajl) ---
                    new_layer.x = data.get('x', 0)
                    new_layer.y = data.get('y', 0)
                    new_layer.scale = data.get('scale', 1.0)
                    new_layer.rotation = data.get('rotation', 0)
            
            return True
            
        except Exception as e:
            print(f"Load Error: {e}")
            return False