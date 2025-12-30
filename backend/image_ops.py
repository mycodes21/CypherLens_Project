from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import numpy as np
import cv2  # OpenCV je obavezan za ovo
import ezdxf

class ImageOpsEngine:
    # --- STANDARD OPS ---
    @staticmethod
    def crop_image(image, crop_box):
        return image.crop(crop_box)

    @staticmethod
    def filter_grayscale(image):
        return ImageOps.grayscale(image)

    @staticmethod
    def filter_sepia(image):
        return ImageOps.colorize(ImageOps.grayscale(image), "#704214", "#C0C0C0")

    @staticmethod
    def rotate_image(image, angle):
        return image.rotate(angle, expand=True)

    @staticmethod
    def filter_blur(image, radius=2):
        return image.filter(ImageFilter.GaussianBlur(radius))

    @staticmethod
    def filter_sharpen(image):
        return image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    @staticmethod
    def filter_invert(image):
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgb = Image.merge('RGB', (r, g, b))
            inv = ImageOps.invert(rgb)
            r2, g2, b2 = inv.split()
            return Image.merge('RGBA', (r2, g2, b2, a))
        return ImageOps.invert(image)

    @staticmethod
    def adjust_brightness(image, factor):
        return ImageEnhance.Brightness(image).enhance(factor)

    @staticmethod
    def auto_enhance(image):
        return ImageOps.autocontrast(image.convert("RGB"), cutoff=2)
    
    # --- CNC / ENGINEERING ---
    @staticmethod
    def generate_cnc_heightmap(image):
        img = ImageOps.grayscale(image)
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        img = ImageOps.autocontrast(img, cutoff=1)
        return img.convert("RGB")

    @staticmethod
    def generate_normal_map(image):
        gray = ImageOps.grayscale(image)
        x_kernel = (-1, 0, 1, -2, 0, 2, -1, 0, 1)
        y_kernel = (-1, -2, -1, 0, 0, 0, 1, 2, 1)
        dx = gray.filter(ImageFilter.Kernel((3, 3), x_kernel, scale=1))
        dy = gray.filter(ImageFilter.Kernel((3, 3), y_kernel, scale=1))
        
        width, height = gray.size
        normal_map = Image.new("RGB", (width, height))
        pixels_x = dx.load()
        pixels_y = dy.load()
        pixels_out = normal_map.load()
        
        for y in range(height):
            for x in range(width):
                val_x = pixels_x[x, y] // 2 + 128
                val_y = pixels_y[x, y] // 2 + 128
                pixels_out[x, y] = (val_x, val_y, 255)
        return normal_map
    
    # ... (ostale metode ostaju iste) ...

    @staticmethod
    def apply_dithering(image):
        """
        Pretvara sliku u 1-bitnu (Crno-Belo) koristeći Floyd-Steinberg algoritam.
        Ovo je OBAVEZNO za lasersko graviranje fotografija.
        """
        # 1. Konvertuj u Grayscale
        gray = ImageOps.grayscale(image)
        
        # 2. Primeni Dithering
        dithered = gray.convert("1") # "1" mode je 1-bit pixel (dithering je automatski u PIL-u)
        
        # 3. Vrati u RGBA da bi se videlo u Layer sistemu
        return dithered.convert("RGBA")

    # --- VECTOR PREP (AŽURIRAN ZA v7.0) ---
    @staticmethod
    def generate_edge_map(image):
        """
        Koristi OpenCV Canny Edge Detection za savršene ivice.
        Rešava problem sa transparentnim slojevima.
        """
        # 1. Konvertuj PIL -> NumPy
        img_np = np.array(image)
        
        # 2. Proveri da li ima Alpha kanal (RGBA)
        if img_np.shape[2] == 4:
            # Izdvoj Alpha kanal
            alpha = img_np[:, :, 3]
            # Konvertuj u Grayscale
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGBA2GRAY)
            # Tamo gde je providno (alpha=0), stavi crnu boju da ne pravi ivice oko kvadrata
            gray[alpha == 0] = 0
        else:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # 3. Malo blura da smanjimo šum pre detekcije
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 4. Canny Edge Detection (Automatski pronalazi ivice)
        # 50 i 150 su pragovi osetljivosti.
        edges = cv2.Canny(blurred, 50, 150)

        # 5. Podebljaj ivice malo (Dilation) da se bolje vide
        kernel = np.ones((2,2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        # 6. Vrati nazad u PIL format (RGBA)
        # Rezultat je crno-bela slika (bela ivica, crna pozadina)
        return Image.fromarray(edges).convert("RGBA")
    
    # --- TOOLS ---
    @staticmethod
    def magic_erase(image, xy, tolerance=50):
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        ImageDraw.floodfill(image, xy, value=(0,0,0,0), thresh=tolerance)
        return image

    @staticmethod
    def add_text(image, xy, text, color, size, font_name="Arial"):
        draw = ImageDraw.Draw(image)
        font = None
        try:
            font = ImageFont.truetype(font_name, size)
        except:
            try:
                font = ImageFont.truetype(f"{font_name}.ttf", size)
            except:
                font = ImageFont.load_default()
        
        draw.text(xy, text, fill=color, font=font)
        return image

    # --- THRESHOLD & DXF ---
    @staticmethod
    def apply_threshold(image, threshold_value):
        """
        Binarizacija: Pretvara sliku u čisto CRNO i BELO.
        Ključno za pripremu za CNC sečenje/graviranje.
        """
        # 1. Konvertuj u Grayscale (sivo) da bi imali vrednosti 0-255
        gray = ImageOps.grayscale(image)
        
        # 2. Primeni prag (sve iznad praga je belo, ispod je crno)
        # threshold_value dolazi sa slajdera (0-255)
        binary = gray.point(lambda p: 255 if p > threshold_value else 0)
        
        # 3. FIX: Konvertuj u RGBA!
        # Layer Manager ne prihvata obične 'L' ili 'RGB' slike, mora imati Alpha kanal.
        return binary.convert("RGBA")

    @staticmethod
    def export_dxf(image, filepath):
        # Priprema za DXF export
        # Mora da radi sa OpenCV konturama
        cv_image = np.array(image.convert("L"))
        
        # Binarizacija
        _, binary = cv2.threshold(cv_image, 127, 255, cv2.THRESH_BINARY)
        
        # Pronalaženje kontura
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        doc = ezdxf.new()
        msp = doc.modelspace()
        
        count = 0
        height, width = binary.shape
        
        for contour in contours:
            if len(contour) < 3: continue
            points = []
            for point in contour:
                px, py = point[0]
                points.append((px, height - py)) 
            
            msp.add_lwpolyline(points, close=True, dxfattribs={'layer': 'CUT_PATH', 'color': 1})
            count += 1
            
        doc.saveas(filepath)
        return count