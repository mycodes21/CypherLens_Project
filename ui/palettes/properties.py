import customtkinter as ctk
from .base_palette import BasePalette

class PropertiesPanel(BasePalette):
    def __init__(self, parent, app_instance=None): # <--- FIX
        super().__init__(parent, title="Properties", width=250, height=200, app_instance=app_instance) # <--- FIX
        self.tool_frame = None
        self.current_tool_name = ""
        self.setup_common_ui()

    # ... (Ostatak fajla isti, samo __init__ menjamo) ...
    # Kopiraj ostatak fajla ako ga nemaš, ali bitan je samo ovaj __init__
    
    def setup_common_ui(self):
        # Placeholder
        self.lbl_title = ctk.CTkLabel(self.content_frame, text="No Tool Selected", font=("Arial", 14, "bold"), text_color="gray")
        self.lbl_title.pack(pady=10)
        
        self.dynamic_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.dynamic_frame.pack(fill="both", expand=True)
        
        # Apply dugme (skriveno po defaultu)
        self.btn_apply = ctk.CTkButton(self.content_frame, text="✅ Apply Shape", fg_color="#2CC985", hover_color="#229966", 
                                       command=lambda: self.parent.apply_shape_to_image())
        
    def show_apply_btn(self):
        self.btn_apply.pack(side="bottom", fill="x", pady=10)
        
    def hide_apply_btn(self):
        self.btn_apply.pack_forget()

    def update_for_tool(self, tool_name):
        # Očisti dynamic frame
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
            
        self.current_tool_name = tool_name
        self.lbl_title.configure(text=tool_name.upper().replace("_", " "))
        self.hide_apply_btn()

        if tool_name == "ruler":
            self.build_ruler_props()
        elif tool_name == "text":
            self.build_text_props()
        elif tool_name in ["brush", "pencil", "rect", "circle", "line"]:
            self.build_brush_props()
        elif tool_name == "magic":
            self.build_magic_props()
        elif tool_name.startswith("adj_"):
            self.build_adjustment_props(tool_name)
    
    # --- BUILDERS ---
    def build_ruler_props(self):
        ctk.CTkLabel(self.dynamic_frame, text="Measured Distance:", text_color="gray").pack(pady=5)
        self.lbl_measure_result = ctk.CTkLabel(self.dynamic_frame, text="0.0 px", font=("Arial", 24, "bold"), text_color="#66FCF1")
        self.lbl_measure_result.pack(pady=5)
        
        ctk.CTkButton(self.dynamic_frame, text="Calibrate (Set MM)", command=self.parent.calibrate_ruler).pack(pady=10)
        self.lbl_calib_info = ctk.CTkLabel(self.dynamic_frame, text="Not Calibrated", font=("Arial", 10), text_color="gray")
        self.lbl_calib_info.pack()

    def build_text_props(self):
        ctk.CTkLabel(self.dynamic_frame, text="Text Content:").pack(anchor="w")
        self.entry_text = ctk.CTkEntry(self.dynamic_frame)
        self.entry_text.pack(fill="x", pady=5)
        self.entry_text.bind("<KeyRelease>", self.parent.on_text_type)
        
        ctk.CTkLabel(self.dynamic_frame, text="Font Size:").pack(anchor="w")
        self.slider_size = ctk.CTkSlider(self.dynamic_frame, from_=10, to=200, command=self.parent.on_text_size_change)
        self.slider_size.set(50)
        self.slider_size.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.dynamic_frame, text="Font Family:").pack(anchor="w")
        self.combo_font = ctk.CTkComboBox(self.dynamic_frame, values=["Arial", "Times New Roman", "Courier New", "Verdana"], command=self.parent.on_font_change)
        self.combo_font.set("Arial")
        self.combo_font.pack(fill="x", pady=5)

    def build_brush_props(self):
        ctk.CTkLabel(self.dynamic_frame, text="Size / Thickness:").pack(anchor="w")
        self.slider_size = ctk.CTkSlider(self.dynamic_frame, from_=1, to=50)
        self.slider_size.set(5)
        self.slider_size.pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.dynamic_frame, text="Shape:").pack(anchor="w")
        self.combo_shape = ctk.CTkComboBox(self.dynamic_frame, values=["Round", "Square"])
        self.combo_shape.pack(fill="x", pady=5)
        
        if self.current_tool_name in ["rect", "circle"]:
            self.fill_var = ctk.BooleanVar(value=False)
            ctk.CTkCheckBox(self.dynamic_frame, text="Fill Shape", variable=self.fill_var).pack(pady=10, anchor="w")

    def build_magic_props(self):
        ctk.CTkLabel(self.dynamic_frame, text="Tolerance (0-100):").pack(anchor="w")
        self.slider_size = ctk.CTkSlider(self.dynamic_frame, from_=0, to=100)
        self.slider_size.set(50)
        self.slider_size.pack(fill="x", pady=5)
        ctk.CTkLabel(self.dynamic_frame, text="Click on color to erase it.", text_color="gray", font=("Arial", 10)).pack(pady=5)

    def build_adjustment_props(self, tool):
        ctk.CTkLabel(self.dynamic_frame, text="Intensity / Level:").pack(anchor="w")
        
        from_v, to_v = 0, 100
        default = 0
        if tool == "adj_threshold": from_v, to_v, default = 0, 255, 128
        
        sl = ctk.CTkSlider(self.dynamic_frame, from_=from_v, to=to_v, command=self.parent.update_adjustment_preview)
        sl.set(default)
        sl.pack(fill="x", pady=10)
        
        ctk.CTkButton(self.dynamic_frame, text="Apply Adjustment", fg_color="#2CC985", command=self.parent.apply_adjustment).pack(pady=10)