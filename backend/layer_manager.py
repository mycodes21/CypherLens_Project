from PIL import Image, ImageEnhance
import copy

class Layer:
    def __init__(self, name, image, visible=True, opacity=1.0):
        self.name = name
        self.image = image  # PIL Image (RGBA)
        self.visible = visible
        self.opacity = opacity 

    def copy(self):
        """Vraća potpunu kopiju ovog sloja."""
        # image.copy() je ključno!
        return Layer(self.name, self.image.copy(), self.visible, self.opacity)

class LayerManager:
    def __init__(self):
        self.layers = [] 
        self.active_index = -1

    def add_layer(self, image, name=None):
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        if name is None:
            name = f"Layer {len(self.layers) + 1}"
            
        new_layer = Layer(name, image)
        self.layers.append(new_layer)
        self.active_index = len(self.layers) - 1 
        return new_layer

    def get_active_layer(self):
        if 0 <= self.active_index < len(self.layers):
            return self.layers[self.active_index]
        return None

    def delete_active_layer(self):
        if 0 <= self.active_index < len(self.layers):
            del self.layers[self.active_index]
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

    def render_composite(self, bg_size=(1920, 1080)):
        if not self.layers:
            return Image.new("RGBA", bg_size, (20, 20, 20, 255))

        base_size = self.layers[0].image.size
        composite = Image.new("RGBA", base_size, (0, 0, 0, 0))

        for layer in self.layers:
            if layer.visible:
                img_to_paste = layer.image
                if layer.opacity < 1.0:
                    alpha = img_to_paste.split()[3]
                    alpha = ImageEnhance.Brightness(alpha).enhance(layer.opacity)
                    img_to_paste.putalpha(alpha)
                composite.alpha_composite(img_to_paste, (0, 0))
        
        return composite

    # --- NOVO: STATE MANAGEMENT (HISTORY) ---
    def get_state_snapshot(self):
        """
        Vraća objekat koji sadrži sve podatke o trenutnom stanju.
        Koristi se za Undo stack.
        """
        snapshot = {
            "active_index": self.active_index,
            # Pravimo novu listu sa kopijama slojeva
            "layers": [layer.copy() for layer in self.layers]
        }
        return snapshot

    def restore_state_from_snapshot(self, snapshot):
        """
        Vraća stanje menadžera na osnovu snapshota.
        """
        self.active_index = snapshot["active_index"]
        # Ponovo, moramo kopirati da ne bi delili reference sa istorijom
        self.layers = [layer.copy() for layer in snapshot["layers"]]