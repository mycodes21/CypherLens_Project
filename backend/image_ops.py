from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import math

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
        return ImageOps.grayscale(image).convert("RGBA")

    @staticmethod
    def filter_sepia(image):
        # Jednostavna sepia konverzija
        width, height = image.size
        pixels = image.load()
        new_img = image.copy()
        
        # Ako je slika prevelika, ovo može biti sporo u Python-u, 
        # ali za sada je ok. Za brže rešenje koristi se numpy.
        gray = ImageOps.grayscale(image)
        gray = ImageOps.colorize(gray, "#704214", "#C0C0C0")
        return gray.convert("RGBA")

    @staticmethod
    def filter_blur(image, radius=2):
        return image.filter(ImageFilter.GaussianBlur(radius))

    @staticmethod
    def filter_sharpen(image):
        return image.filter(ImageFilter.SHARPEN)

    @staticmethod
    def apply_threshold(image, threshold=128):
        # Konvertuj u sivo pa primeni prag
        gray = image.convert("L")
        return gray.point(lambda p: 255 if p > threshold else 0).convert("RGBA")

    @staticmethod
    def auto_enhance(image):
        return ImageOps.autocontrast(image.convert("RGB")).convert("RGBA")

    @staticmethod
    def rotate_image(image, angle):
        return image.rotate(angle, expand=True)

    @staticmethod
    def crop_image(image, box):
        # box = (left, top, right, bottom)
        return image.crop(box)

    @staticmethod
    def magic_erase(image, point, tolerance=30):
        # Ovo je kompleksna funkcija (flood fill). 
        # Za sada vraćamo istu sliku da program ne puca.
        # Kasnije možemo ubaciti pravi algoritam.
        print(f"Magic erase at {point} with tol {tolerance}")
        return image

    @staticmethod
    def add_text(image, position, text, color, size, font_name="Arial"):
        draw = ImageDraw.Draw(image)
        try:
            # Pokušaj da učitaš font, ako ne može, koristi default
            font = ImageFont.truetype(font_name + ".ttf", size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", size)
            except:
                font = ImageFont.load_default()
        
        draw.text(position, text, fill=color, font=font)
        return image

    @staticmethod
    def generate_qr_code(text, size=400):
        try:
            import qrcode
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            return img.convert("RGBA").resize((size, size))
        except ImportError:
            print("QRCode module not installed. Run: pip install qrcode")
            return Image.new("RGBA", (size, size), (255, 0, 0, 255))

    @staticmethod
    def generate_edge_map(image):
        return image.filter(ImageFilter.FIND_EDGES).convert("RGBA")

    @staticmethod
    def apply_dithering(image):
        return image.convert("1").convert("RGBA")

    @staticmethod
    def export_dxf_vectors(image, filepath):
        # Placeholder za DXF export
        print(f"Exporting DXF to {filepath}")
        return 1 # Vraća broj putanja

    @staticmethod
    def generate_normal_map_precise(img, strength=5.0):
        # Placeholder
        return img.convert("RGB")

    @staticmethod
    def save_16bit_tiff(img, path):
        img.save(path)