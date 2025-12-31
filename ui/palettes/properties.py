import customtkinter as ctk

class PropertiesPanel(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, width=250, fg_color="#2b2b2b", corner_radius=0)
        self.app = app_instance
        
        # Naslov
        self.title_label = ctk.CTkLabel(self, text="PROPERTIES", font=("Arial", 14, "bold"), text_color="#66FCF1")
        self.title_label.pack(pady=10)
        
        # Kontejner
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def update_for_tool(self, tool_name):
        """Kada se promeni alat, vrati na prikaz sloja."""
        self.show_layer_properties()

    def update_properties(self):
        """Osveži prikaz."""
        self.show_layer_properties()

    def show_layer_properties(self):
        """Prikaz standardnih opcija (Scale, Rotate)."""
        self.reset_panel()
        self.title_label.configure(text="LAYER PROPERTIES")
        
        active_layer = None
        if hasattr(self.app, 'get_active_layer'):
            active_layer = self.app.get_active_layer()
        
        if not active_layer:
            ctk.CTkLabel(self.content_frame, text="No layer selected", text_color="gray").pack(pady=20)
            return

        # Slajderi
        self._add_slider("Opacity", 0, 255, active_layer.get('opacity', 255), 
                         lambda val: self.app.update_layer_property("opacity", val))
        self._add_slider("Scale", 0.1, 3.0, active_layer.get('scale', 1.0), 
                         lambda val: self.app.update_layer_property("scale", val))
        self._add_slider("Rotation", -180, 180, active_layer.get('rotation', 0), 
                         lambda val: self.app.update_layer_property("rotation", val))
        
        # Delete dugme
        ctk.CTkButton(self.content_frame, text="🗑️ Delete Layer", fg_color="#ff4444", hover_color="#cc0000",
                      command=self.app.delete_active_layer).pack(pady=20)

    def show_adjustment_sliders(self, adjustment_type):
        """Prikaz slajdera za Brightness/Contrast."""
        self.reset_panel()
        self.title_label.configure(text=adjustment_type.upper())

        if adjustment_type == "brightness":
            self._add_slider("Brightness", 0.5, 2.0, 1.0, lambda val: self.app.apply_brightness(val))
            self._add_slider("Contrast", 0.5, 2.0, 1.0, lambda val: self.app.apply_contrast(val))
            
            ctk.CTkButton(self.content_frame, text="Apply", fg_color="#66FCF1", text_color="black",
                          command=self.app.apply_image_adjustments).pack(pady=10)
        
        ctk.CTkButton(self.content_frame, text="Cancel", fg_color="transparent", border_width=1,
                      command=self.show_layer_properties).pack(pady=5)

    def reset_panel(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _add_slider(self, label_text, min_val, max_val, current_val, command):
        ctk.CTkLabel(self.content_frame, text=label_text).pack(anchor="w", pady=(5, 0))
        slider = ctk.CTkSlider(self.content_frame, from_=min_val, to=max_val, number_of_steps=100, command=command)
        slider.set(current_val)
        slider.pack(fill="x", pady=5)