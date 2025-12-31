import customtkinter as ctk

class PropertiesPanel(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, width=250, fg_color="#2b2b2b", corner_radius=0)
        self.app = app_instance
        
        # Naslov
        self.title_label = ctk.CTkLabel(self, text="PROPERTIES", font=("Arial", 14, "bold"), text_color="#66FCF1")
        self.title_label.pack(pady=10)
        
        # Kontejner za promenljivi sadržaj
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Reference na widgete (da bi main_window mogao da čita vrednosti)
        self.entry_text = None
        self.combo_font = None
        self.slider_size = None
        self.lbl_measure_result = None
        self.fill_var = ctk.BooleanVar(value=False) # Za oblike (punjenje)

    def reset_panel(self):
        """Briše sve widgete iz content_frame-a."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_for_tool(self, tool_name):
        """Glavni switch - odlučuje šta se prikazuje na osnovu alata."""
        self.reset_panel()
        self.title_label.configure(text=tool_name.upper() + " OPTIONS")

        if tool_name == "text":
            self._show_text_options()
        elif tool_name in ["crop", "rect", "circle", "line"]:
            self._show_shape_options(tool_name)
        elif tool_name == "ruler":
            self._show_ruler_options()
        elif tool_name in ["adj_brightness", "adj_contrast", "adj_blur", "adj_sharpen", "adj_threshold"]:
            self.show_adjustment_sliders(tool_name.replace("adj_", ""))
        else:
            # Default: Prikazi Layer Properties
            self.show_layer_properties()

    # --- SPECIFIČNI PRIKAZI ---

    def _show_text_options(self):
        ctk.CTkLabel(self.content_frame, text="Text Content:").pack(anchor="w")
        self.entry_text = ctk.CTkEntry(self.content_frame, placeholder_text="Type here...")
        self.entry_text.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.content_frame, text="Font Size:").pack(anchor="w", pady=(10,0))
        self.slider_size = ctk.CTkSlider(self.content_frame, from_=10, to=200, number_of_steps=190)
        self.slider_size.set(50)
        self.slider_size.pack(fill="x", pady=5)

        ctk.CTkLabel(self.content_frame, text="Font:").pack(anchor="w")
        self.combo_font = ctk.CTkComboBox(self.content_frame, values=["Arial", "Times New Roman", "Courier", "Verdana"])
        self.combo_font.pack(fill="x", pady=5)

        # Apply dugme (inicijalno sakriveno, main_window ga prikazuje kad klikneš na platno)
        self.btn_apply = ctk.CTkButton(self.content_frame, text="Apply Text", fg_color="#66FCF1", text_color="black",
                                       command=self.app.apply_shape_to_image)
        self.btn_apply.pack(pady=20)
        self.btn_apply.pack_forget() # Sakrij dok ne klikne na platno

    def _show_shape_options(self, tool_name):
        ctk.CTkLabel(self.content_frame, text="Line Width / Border:").pack(anchor="w")
        self.slider_size = ctk.CTkSlider(self.content_frame, from_=1, to=50)
        self.slider_size.set(5)
        self.slider_size.pack(fill="x", pady=5)

        if tool_name in ["rect", "circle"]:
            chk = ctk.CTkCheckBox(self.content_frame, text="Fill Shape", variable=self.fill_var)
            chk.pack(pady=10, anchor="w")

        self.btn_apply = ctk.CTkButton(self.content_frame, text="Apply", fg_color="#66FCF1", text_color="black",
                                       command=self.app.apply_shape_to_image)
        self.btn_apply.pack(pady=20)
        self.btn_apply.pack_forget() # Sakrij dok ne nacrta

    def _show_ruler_options(self):
        ctk.CTkLabel(self.content_frame, text="Measurement:", font=("Arial", 12)).pack(anchor="w", pady=10)
        self.lbl_measure_result = ctk.CTkLabel(self.content_frame, text="0.0 px", font=("Consolas", 20, "bold"), text_color="#66FCF1")
        self.lbl_measure_result.pack(pady=10)
        
        self.lbl_calib_info = ctk.CTkLabel(self.content_frame, text="Scale: 1.0", text_color="gray")
        self.lbl_calib_info.pack()

        ctk.CTkButton(self.content_frame, text="Calibrate (Set MM)", command=self.app.calibrate_ruler).pack(pady=20)

    def show_adjustment_sliders(self, adj_type):
        self.reset_panel()
        self.title_label.configure(text=adj_type.upper())
        
        # Mapiranje funkcija i opsega
        cmd = None
        min_v, max_v, start_v = 0, 100, 50

        if adj_type == "brightness":
            min_v, max_v, start_v = 0.5, 2.0, 1.0
            cmd = self.app.apply_brightness
        elif adj_type == "contrast":
            min_v, max_v, start_v = 0.5, 2.0, 1.0
            cmd = self.app.apply_contrast
        elif adj_type == "blur":
            min_v, max_v, start_v = 0, 10, 0
            # Moramo dodati metodu u main_window za blur preview ako ne postoji
            cmd = lambda v: self.app.update_adjustment_preview(v) 
        elif adj_type == "sharpen":
            min_v, max_v, start_v = 0, 10, 0
            cmd = lambda v: self.app.update_adjustment_preview(v)

        ctk.CTkLabel(self.content_frame, text="Intensity:").pack(anchor="w")
        slider = ctk.CTkSlider(self.content_frame, from_=min_v, to=max_v, number_of_steps=100, command=cmd)
        slider.set(start_v)
        slider.pack(fill="x", pady=10)

        ctk.CTkButton(self.content_frame, text="Apply", fg_color="#66FCF1", text_color="black",
                      command=self.app.apply_image_adjustments).pack(pady=10)
        
        ctk.CTkButton(self.content_frame, text="Cancel", fg_color="transparent", border_width=1,
                      command=lambda: self.app.set_active_tool("move")).pack(pady=5)

    def show_layer_properties(self):
        self.reset_panel()
        self.title_label.configure(text="LAYER PROPERTIES")
        
        active_layer = None
        if hasattr(self.app, 'get_active_layer'):
            active_layer = self.app.get_active_layer()
        
        if not active_layer:
            ctk.CTkLabel(self.content_frame, text="No layer selected", text_color="gray").pack(pady=20)
            return

        self._add_slider("Opacity", 0, 255, active_layer.opacity, 
                         lambda val: self.app.update_layer_property("opacity", val))
        self._add_slider("Scale", 0.1, 3.0, active_layer.scale, 
                         lambda val: self.app.update_layer_property("scale", val))
        self._add_slider("Rotation", -180, 180, active_layer.rotation, 
                         lambda val: self.app.update_layer_property("rotation", val))
        
        ctk.CTkButton(self.content_frame, text="🗑️ Delete Layer", fg_color="#ff4444", hover_color="#cc0000",
                      command=self.app.delete_layer).pack(pady=20)

    def _add_slider(self, label_text, min_val, max_val, current_val, command):
        ctk.CTkLabel(self.content_frame, text=label_text).pack(anchor="w", pady=(5, 0))
        slider = ctk.CTkSlider(self.content_frame, from_=min_val, to=max_val, number_of_steps=100, command=command)
        slider.set(current_val)
        slider.pack(fill="x", pady=5)

    # Helperi za prikaz/sakrivanje apply dugmeta
    def show_apply_btn(self):
        if hasattr(self, 'btn_apply'): self.btn_apply.pack(pady=20)
    def hide_apply_btn(self):
        if hasattr(self, 'btn_apply'): self.btn_apply.pack_forget()