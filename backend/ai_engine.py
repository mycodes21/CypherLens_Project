from rembg import remove
from PIL import Image, ImageOps # <--- Dodali smo ImageOps
from transformers import pipeline 
import torch

class AIEngine:
    _depth_pipe = None

    @staticmethod
    def remove_background(image):
        try:
            # Rembg očekuje i vraća RGBA
            return remove(image)
        except Exception as e:
            print(f"BG Removal Error: {e}")
            return None

    @staticmethod
    def generate_depth_map(image):
        """
        Kreira Heightmap.
        FIX v7.1: Dodat Auto-Contrast i konverzija u RGBA da se ne bi dobilo 'crnilo'.
        """
        try:
            if AIEngine._depth_pipe is None:
                print("Loading AI Depth Model...")
                # Određujemo uređaj (GPU ako može, inače CPU)
                device = 0 if torch.cuda.is_available() else -1
                AIEngine._depth_pipe = pipeline(
                    task="depth-estimation", 
                    model="LiheYoung/depth-anything-small-hf",
                    device=device
                )
            
            print("Analyzing depth...")
            # Pipeline vraća dict
            result = AIEngine._depth_pipe(image)
            depth_map = result["depth"]
            
            # --- KLJUČNA POPRAVKA ZA V7.0 ---
            
            # 1. Osiguraj da je slika u Grayscale modu (L)
            if depth_map.mode != 'L':
                depth_map = depth_map.convert('L')
                
            # 2. AUTO-CONTRAST (Ovo rešava "crnilo" i vraća detalje)
            # Razvlači histogram tako da najniža tačka bude 0 (crno), a najviša 255 (belo)
            depth_map = ImageOps.autocontrast(depth_map)
            
            # 3. Konvertuj u RGBA jer LayerManager to zahteva
            # (Inače bi transparentnost mogla da brljavi)
            return depth_map.convert("RGBA")
            
        except Exception as e:
            print(f"AI Depth Error: {e}")
            return None