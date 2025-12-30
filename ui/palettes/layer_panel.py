import customtkinter as ctk
from PIL import Image, ImageTk
from .base_palette import BasePalette

class LayerPanel(BasePalette):
    def __init__(self, parent, app_instance=None): # <--- PRIMAMO app_instance
        # <--- PROSLEĐUJEMO app_instance DALJE U SUPER
        super().__init__(parent, title="Layers", width=250, height=300, app_instance=app_instance) 
        self.row_frames = {} 
        self.setup_content()

    # ... (OSTATAK FAJLA OSTAJE ISTI - update_list, setup_content itd.) ...
    # Kopiraj ostatak fajla kakav je bio, samo zameni __init__ metod.
    
    def setup_content(self):
        # --- BUTTONS ---
        ctrl_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=40)
        ctrl_frame.pack(fill="x", side="bottom", pady=5)
        
        btn_add = ctk.CTkButton(ctrl_frame, text="+", width=30, command=self.parent.add_blank_layer)
        btn_add.pack(side="left", padx=2)
        
        btn_del = ctk.CTkButton(ctrl_frame, text="-", width=30, fg_color="#FF5555", hover_color="#AA0000", command=self.parent.delete_layer)
        btn_del.pack(side="left", padx=2)
        
        btn_up = ctk.CTkButton(ctrl_frame, text="▲", width=30, command=self.parent.layer_up)
        btn_up.pack(side="left", padx=2)
        
        btn_down = ctk.CTkButton(ctrl_frame, text="▼", width=30, command=self.parent.layer_down)
        btn_down.pack(side="left", padx=2)

        # --- SCROLL LIST ---
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#111")
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.refresh_layer_list()

    def refresh_layer_list(self):
        # Očisti listu
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.row_frames = {}

        if not hasattr(self.parent, 'layer_manager'): return

        layers = self.parent.layer_manager.layers
        active_idx = self.parent.layer_manager.active_index
        
        # Crtamo listu obrnuto (Top layer first)
        for i in range(len(layers) - 1, -1, -1):
            layer = layers[i]
            is_active = (i == active_idx)
            
            row_color = "#2B3642" if is_active else "transparent"
            text_color = "#66FCF1" if is_active else "gray"
            
            row = ctk.CTkFrame(self.scroll_frame, fg_color=row_color, height=35, corner_radius=5)
            row.pack(fill="x", pady=1)
            
            # Click event na ceo red da selektuje
            row.bind("<Button-1>", lambda e, idx=i: self.parent.select_layer(idx))
            
            # Visibility Toggle
            vis_text = "👁️" if layer.visible else "🚫"
            vis_btn = ctk.CTkButton(row, text=vis_text, width=25, height=25, fg_color="transparent", 
                                    text_color="white", hover_color="#444",
                                    command=lambda idx=i: self.parent.toggle_layer_visibility(idx))
            vis_btn.pack(side="left", padx=2)
            
            # Name Label
            lbl = ctk.CTkLabel(row, text=layer.name, text_color=text_color, font=("Arial", 12))
            lbl.pack(side="left", padx=5)
            lbl.bind("<Button-1>", lambda e, idx=i: self.parent.select_layer(idx))
            
            self.row_frames[i] = row