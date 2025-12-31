import os
from PIL import Image

# NAPOMENA: Ovde NE importujemo torch, transformers ni rembg.
# To radimo unutar funkcija da bi se aplikacija palila brzo!

class AIEngine:
    
    _depth_pipe = None  # Cache za model

    @staticmethod
    def remove_background(image):
        """
        Uklanja pozadinu. Biblioteku učitava tek kad se pozove funkcija.
        """
        print("Initializing Rembg...")
        try:
            # IMPORTUJEMO SAMO KAD TREBA
            from rembg import remove 
            return remove(image)
        except ImportError:
            print("Error: 'rembg' library not installed.")
            return None
        except Exception as e:
            print(f"AI BG Error: {e}")
            return None

    @classmethod
    def generate_depth_map(cls, image):
        """
        Generiše Heightmap i primenjuje CLAHE za pojačavanje lokalnih detalja (nos, oči).
        """
        print("Initializing Depth AI...")
        
        # Provera biblioteka
        try:
            from transformers import pipeline
            import torch
            import numpy as np # Treba nam numpy za matematiku
            import cv2         # Treba nam OpenCV za CLAHE
        except ImportError:
            print("Missing libraries. Using grayscale fallback.")
            return image.convert("L")

        try:
            # Učitavanje modela
            if cls._depth_pipe is None:
                print("Loading AI Model...")
                device = 0 if torch.cuda.is_available() else -1
                cls._depth_pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf", device=device)
            
            # 1. Generiši RAW depth mapu
            result = cls._depth_pipe(image)
            depth_image = result["depth"] # Ovo je PIL slika
            
            # --- POJAČAVANJE DETALJA (CLAHE) ---
            
            # Konvertuj u numpy array (grayscale)
            img_np = np.array(depth_image.convert("L"))
            
            # Definiši CLAHE (Contrast Limited Adaptive Histogram Equalization)
            # clipLimit: Koliko jako da pojača kontrast (2.0 do 4.0 je dobro)
            # tileGridSize: Veličina "prozora" koji gleda (8x8 je standard)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            
            # Primeni na sliku
            enhanced_img_np = clahe.apply(img_np)
            
            # Opciono: Malo blurovanja da uklonimo šum od pojačavanja
            # enhanced_img_np = cv2.GaussianBlur(enhanced_img_np, (3, 3), 0)

            # Vrati nazad u PIL format
            return Image.fromarray(enhanced_img_np).convert("RGBA")

        except Exception as e:
            print(f"Depth AI Error: {e}")
            return image.convert("L")