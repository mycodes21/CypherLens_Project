import customtkinter as ctk
# Apsolutni importi
from ui.palettes.properties import PropertiesPanel
from ui.palettes.layer_panel import LayerPanel
from ui.palettes.filters import FilterBox

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, width=320, fg_color="#151515", corner_radius=0)
        self.app = app_instance
        self.pack_propagate(False) 
        
        # =================================================
        # 1. PROPERTIES (GORE - 25% Visine)
        # =================================================
        self.frame_props = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_props.pack(side="top", fill="both", expand=True, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_props, text="TOOL PROPERTIES", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", pady=2)
        
        self.properties = PropertiesPanel(self.frame_props, app_instance=self.app)
        self.properties.pack(fill="both", expand=True)

        self._add_separator()

        # =================================================
        # 2. FILTERS (SREDINA - 40% Visine)
        # =================================================
        self.frame_filters = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filters.pack(side="top", fill="both", expand=True, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_filters, text="FILTERS & FX", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", pady=2)
        
        self.filterbox = FilterBox(self.frame_filters, app_instance=self.app)
        self.filterbox.pack(fill="both", expand=True)

        self._add_separator()

        # =================================================
        # 3. LAYERS (DOLE - 35% Visine)
        # =================================================
        self.frame_layers = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_layers.pack(side="bottom", fill="both", expand=True, padx=5, pady=2)
        
        ctk.CTkLabel(self.frame_layers, text="LAYERS", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", pady=2)
        
        self.layerbox = LayerPanel(self.frame_layers, app_instance=self.app)
        self.layerbox.pack(fill="both", expand=True)

        # Connect to App
        self.app.properties = self.properties
        self.app.layerbox = self.layerbox
        self.app.filterbox = self.filterbox

    def _add_separator(self):
        ctk.CTkFrame(self, height=2, fg_color="#222").pack(fill="x", padx=10, pady=5)