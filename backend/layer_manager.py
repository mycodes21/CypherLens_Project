from PIL import Image, ImageEnhance, ImageChops

class Layer:
    def __init__(self, image, name):
        self.image = image
        self.name = name
        self.visible = True
        self.opacity = 255
        self.blend_mode = "Normal"
        # OVO JE FALILO: Koordinate sloja
        self.x = 0
        self.y = 0
        # Transformacije
        self.scale = 1.0
        self.rotation = 0

    def get_processed_image(self):
        """Vraća sliku sa primenjenim opacity, scale i rotation."""
        img = self.image.copy()
        
        # 1. Resize / Scale
        if self.scale != 1.0:
            w, h = img.size
            new_w = int(w * self.scale)
            new_h = int(h * self.scale)
            if new_w > 0 and new_h > 0:
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # 2. Rotation
        if self.rotation != 0:
            img = img.rotate(self.rotation, expand=True)

        # 3. Opacity
        if self.opacity < 255:
            # Alpha modifikacija
            alpha = img.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(self.opacity / 255.0)
            img.putalpha(alpha)
            
        return img

class LayerManager:
    def __init__(self):
        self.layers = []
        self.active_index = -1

    def add_layer(self, image, name="New Layer"):
        new_layer = Layer(image, name)
        self.layers.append(new_layer)
        self.active_index = len(self.layers) - 1

    def get_active_layer(self):
        if 0 <= self.active_index < len(self.layers):
            return self.layers[self.active_index]
        return None

    def delete_active_layer(self):
        if 0 <= self.active_index < len(self.layers):
            self.layers.pop(self.active_index)
            if self.active_index >= len(self.layers):
                self.active_index = len(self.layers) - 1

    def move_layer_up(self):
        idx = self.active_index
        if idx < len(self.layers) - 1:
            self.layers[idx], self.layers[idx+1] = self.layers[idx+1], self.layers[idx]
            self.active_index += 1

    def move_layer_down(self):
        idx = self.active_index
        if idx > 0:
            self.layers[idx], self.layers[idx-1] = self.layers[idx-1], self.layers[idx]
            self.active_index -= 1

    def render_composite(self):
        """Spaja sve slojeve u jednu sliku, poštujući njihove X, Y koordinate."""
        if not self.layers:
            return None

        # 1. Nađi dimenzije platna (Canvasa)
        # Obično uzimamo dimenzije prvog sloja (pozadine) ili neku fiksnu veličinu
        base_w, base_h = 1920, 1080 
        
        # Ako postoji prvi sloj, uzmi njegove dimenzije kao osnovu, ali pazi na skaliranje
        if self.layers:
            # Privremeno rešenje: Platno je veliko koliko i prvi sloj (Background)
            base_w, base_h = self.layers[0].image.size

        # Kreiraj prazno platno
        composite = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))

        for layer in self.layers:
            if layer.visible:
                img_to_paste = layer.get_processed_image()
                
                # OVDE JE BILA GREŠKA: Ranije smo lepili uvek na (0,0)
                # SADA: Lepimo na (layer.x, layer.y)
                
                # Moramo paziti da image paste ne pukne ako je van granica,
                # ali PIL obično handluje negativne koordinate tako što kropuje.
                
                # Za svaki slučaj, koristimo alpha_composite ili paste sa maskom
                try:
                    # Paste zahteva (x, y). Image.paste menja composite in-place.
                    # Koristimo img_to_paste kao masku da bi prozirnost radila.
                    composite.paste(img_to_paste, (layer.x, layer.y), img_to_paste)
                except Exception as e:
                    print(f"Error rendering layer {layer.name}: {e}")

        return composite

    # --- STATE MANAGEMENT (UNDO/REDO) ---
    def get_state_snapshot(self):
        # Vraća kopiju liste slojeva (deep copy je sigurniji, ali sporiji)
        # Ovde radimo jednostavnu kopiju stanja
        import copy
        return copy.deepcopy(self.layers)

    def restore_state_from_snapshot(self, snapshot):
        self.layers = snapshot
        # Provera indeksa
        if self.active_index >= len(self.layers):
            self.active_index = len(self.layers) - 1