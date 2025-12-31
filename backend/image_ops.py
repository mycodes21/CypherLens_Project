import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import qrcode

class ImageOpsEngine:
    @staticmethod
    def generate_qr_code(text):
        try:
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            return img.convert("RGBA")
        except Exception as e:
            print(f"QR Error: {e}")
            return None

    @staticmethod
    def generate_normal_map_precise(image, strength=5.0):
        img_np = np.array(image.convert("L"))
        sobelx = cv2.Sobel(img_np, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img_np, cv2.CV_64F, 0, 1, ksize=3)
        sobelx = -sobelx * strength
        sobely = -sobely * strength
        z = np.ones_like(sobelx) * 255.0
        norm = np.sqrt(sobelx**2 + sobely**2 + z**2)
        normal_x = ((sobelx / norm) + 1) / 2 * 255
        normal_y = ((sobely / norm) + 1) / 2 * 255
        normal_z = ((z / norm) + 1) / 2 * 255
        return Image.fromarray(np.dstack((normal_x, normal_y, normal_z)).astype(np.uint8)).convert("RGBA")

    @staticmethod
    def save_16bit_tiff(image, filepath):
        try:
            arr = np.array(image.convert("L")).astype(np.uint16) * 257
            Image.fromarray(arr, mode='I;16').save(filepath)
            return True
        except Exception as e:
            print(f"TIFF Error: {e}")
            return False