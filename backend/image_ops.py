import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw, ImageFont
import ezdxf  # <--- NOVO: Za pravljenje vektorskih fajlova

class ImageOpsEngine:
    
    @staticmethod
    def adjust_brightness(image, factor):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def adjust_contrast(image, factor):
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    @staticmethod
    def filter_grayscale(image):
        return ImageOps.grayscale(image)
    
    @staticmethod
    def filter_sepia(image):
        width, height = image.size
        pixels = image.load() 
        for py in range(height):
            for px in range(width):
                r, g, b = image.getpixel((px, py))[:3]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255), 255)
        return image

    @staticmethod
    def filter_invert(image):
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted_image = ImageOps.invert(rgb_image)
            r2, g2, b2 = inverted_image.split()
            return Image.merge('RGBA', (r2, g2, b2, a))
        else:
            return ImageOps.invert(image)

    @staticmethod
    def filter_blur(image, radius=2):
        return image.filter(ImageFilter.GaussianBlur(radius))

    @staticmethod
    def filter_sharpen(image):
        return image.filter(ImageFilter.SHARPEN)

    @staticmethod
    def apply_threshold(image, threshold_value=128):
        """Pretvara sliku u čistu crno-belu (binarnu)"""
        grayscale = image.convert("L")
        # Sve iznad praga postaje belo (255), sve ispod crno (0)
        return grayscale.point(lambda x: 255 if x > threshold_value else 0, mode="1").convert("RGBA")

    @staticmethod
    def rotate_image(image, angle):
        return image.rotate(angle, expand=True)

    @staticmethod
    def auto_enhance(image):
        return ImageOps.autocontrast(image.convert("RGB")).convert("RGBA")

    @staticmethod
    def generate_edge_map(image):
        """Vraća vizuelni prikaz ivica (Raster)"""
        # Konverzija u OpenCV format
        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)
        # Canny algoritam
        edges = cv2.Canny(gray, 100, 200)
        # Vrati nazad u PIL
        return Image.fromarray(edges).convert("RGBA")

    @staticmethod
    def generate_normal_map(image):
        # Jednostavna simulacija normal map-a (sobel filteri)
        img_np = np.array(image.convert("L"))
        sobelx = cv2.Sobel(img_np, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(img_np, cv2.CV_64F, 0, 1, ksize=5)
        
        # Normalizacija
        sobelx = np.uint8(np.absolute(sobelx))
        sobely = np.uint8(np.absolute(sobely))
        
        # Spajanje u RGB (Blue kanal je Z-osa, obično bela/svetla)
        zeros = np.zeros_like(sobelx)
        normal_map = np.dstack((sobelx, sobely, np.full_like(sobelx, 255)))
        return Image.fromarray(normal_map).convert("RGBA")

    @staticmethod
    def apply_dithering(image):
        """Priprema za lasersko graviranje (Halftone)"""
        return image.convert("1").convert("RGBA")

    @staticmethod
    def magic_erase(image, point, tolerance=30):
        # Flood fill algoritam za brisanje pozadine (pojednostavljeno)
        # Za pravi 'magic wand' treba nam složeniji algoritam, 
        # ali ovde koristimo jednostavan pristup ili Rembg ako je dostupan.
        # Ovo je placeholder za jednostavnu logiku ako ne koristimo AI.
        return image # Za sada ne radimo manual magic erase bez NumPy trikova

    # --- VECTOR TOOLS ---
    
    @staticmethod
    def add_text(image, pos, text, color, size, font_name="Arial"):
        draw = ImageDraw.Draw(image)
        try:
            # Pokušaj da učitaš sistemski font
            font = ImageFont.truetype(f"{font_name}.ttf", size)
        except:
            # Fallback
            font = ImageFont.load_default()
            
        draw.text(pos, text, font=font, fill=color)
        return image

    @staticmethod
    def crop_image(image, box):
        return image.crop(box)

    @staticmethod
    def export_dxf_vectors(image, filepath):
        """
        Glavna zvezda: Pretvara sliku u Vektore (DXF) za sečenje!
        1. Pretvara u crno-belo
        2. Nalazi konture
        3. Crta te konture kao polilinije u DXF fajl
        """
        # 1. Priprema (OpenCV)
        img_np = np.array(image.convert("RGB")) # DXF ne mari za alpha kanal
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # Threshold (mora biti binarna slika da bi našao ivice)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # 2. Pronalaženje kontura (RETR_LIST daje sve konture, CHAIN_APPROX_SIMPLE smanjuje broj tačaka)
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0
            
        # 3. Pravljenje DXF fajla
        doc = ezdxf.new()
        msp = doc.modelspace()
        
        count = 0
        for contour in contours:
            # OpenCV vraća konture kao [ [[x,y]], [[x,y]]... ]
            # Treba nam lista (x, y)
            points = []
            for point in contour:
                x, y = point[0]
                # Y osa je obrnuta u slikama vs CAD-u, ali za početak ostavljamo ovako
                # Da bi bilo "uspravno" u CAD-u, često se radi: (x, -y)
                points.append((float(x), float(-y)))
            
            if len(points) > 1:
                # Dodajemo "LWPOLYLINE" (Lightweight Polyline) u DXF
                msp.add_lwpolyline(points, close=True, dxfattribs={'color': 7}) # Boja 7 je bela/crna
                count += 1
                
        doc.saveas(filepath)
        return count