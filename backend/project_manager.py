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
        
        Čuva projekat kao ZIP arhivu (.cph) koja sadrži:
        1. project.json (podaci o slojevima: ime, opacity, visible...)
        2. layer_0.png, layer_1.png... (slike svakog sloja)
        """
        try:
            with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
                metadata = []
                
                # Prolazimo kroz sve slojeve iz LayerManager-a
                for index, layer in enumerate(layer_manager.layers):
                    # 1. Sačuvaj sliku u memoriju pa u ZIP
                    img_filename = f"layer_{index}.png"
                    img_byte_arr = io.BytesIO()
                    layer.image.save(img_byte_arr, format='PNG')
                    zf.writestr(img_filename, img_byte_arr.getvalue())
                    
                    # 2. Pripremi podatke za JSON
                    layer_data = {
                        "name": layer.name,
                        "visible": layer.visible,
                        "opacity": layer.opacity,
                        "image_file": img_filename
                    }
                    metadata.append(layer_data)
                
                # 3. Sačuvaj JSON opis celog projekta
                zf.writestr('project.json', json.dumps(metadata, indent=4))
                
            print(f"Project saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"Save Error: {e}")
            return False

    @staticmethod
    def load_project(filepath, layer_manager):
        """
        Učitava .cph fajl (ZIP) i rekonstruiše slojeve u LayerManager.
        """
        try:
            with zipfile.ZipFile(filepath, 'r') as zf:
                # 1. Proveri i učitaj JSON
                if 'project.json' not in zf.namelist():
                    raise ValueError("Invalid project file: missing project.json")
                
                json_data = zf.read('project.json')
                metadata = json.loads(json_data)
                
                # Očisti trenutne slojeve u aplikaciji
                layer_manager.layers = []
                layer_manager.active_index = -1
                
                # 2. Rekonstruiši slojeve jedan po jedan
                for data in metadata:
                    img_file = data['image_file']
                    
                    # Čitamo sliku direktno iz ZIP-a u memoriju
                    img_data = zf.read(img_file)
                    
                    # Konvertuj bytes -> PIL Image
                    image = Image.open(io.BytesIO(img_data)).convert("RGBA")
                    
                    # Dodaj u manager
                    new_layer = layer_manager.add_layer(image, data['name'])
                    
                    # Vrati stara podešavanja
                    new_layer.visible = data.get('visible', True)
                    new_layer.opacity = data.get('opacity', 255)
            
            return True
            
        except Exception as e:
            print(f"Load Error: {e}")
            return False