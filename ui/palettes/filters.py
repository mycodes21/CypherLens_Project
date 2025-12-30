import customtkinter as ctk
from .base_palette import BasePalette

class FilterBox(BasePalette):
    def __init__(self, parent, app_instance=None): # <--- FIX
        super().__init__(parent, title="Filters", width=250, height=450, color_accent="#FF5555", app_instance=app_instance) # <--- FIX
        self.setup_content()

    def setup_content(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        # --- ENGINEERING / CNC ---
        self.add_section_label("ENGINEERING / CNC")
        self.create_filter_btn("⚙️ AI Heightmap (Depth)", self.parent.run_cnc_heightmap)
        self.create_filter_btn("📐 Vector Prep (Edges)", self.parent.run_vector_prep)
        self.create_filter_btn("🎚️ Manual Threshold", lambda: self.parent.set_active_tool("adj_threshold"))
        
        # NOVO: Halftoning
        self.create_filter_btn("🏁 Halftone (Dither)", self.parent.run_halftone)
        
        # NOVO: G-Code
        self.create_filter_btn("🤖 Generate G-Code (Raster)", self.parent.run_gcode_gen)
        
        self.create_filter_btn("💾 Export as .DXF", self.parent.run_dxf_export)
        
        self.add_section_label("COLOR GRADE")
        self.create_filter_btn("⚫ Black & White", self.parent.run_filter_bw)
        self.create_filter_btn("🟤 Sepia Vintage", self.parent.run_filter_sepia)
        self.add_section_label("ADJUSTMENTS (LIVE)")
        self.create_filter_btn("✨ Auto Magic Fix", self.parent.run_auto_enhance)
        self.create_filter_btn("☀️ Brightness / Exposure", lambda: self.parent.set_active_tool("adj_brightness"))
        self.add_section_label("EFFECTS (LIVE)")
        self.create_filter_btn("🌫️ Blur", lambda: self.parent.set_active_tool("adj_blur"))
        self.create_filter_btn("🔪 Sharpen", lambda: self.parent.set_active_tool("adj_sharpen"))
        self.add_section_label("TRANSFORM")
        self.create_filter_btn("🔄 Rotate 90°", self.parent.run_rotate_left)

    def add_section_label(self, text):
        ctk.CTkLabel(self.scroll_frame, text=text, font=("Arial", 11, "bold"), text_color="#66FCF1").pack(pady=(15, 5), anchor="w", padx=5)

    def create_filter_btn(self, text, cmd):
        btn = ctk.CTkButton(
            self.scroll_frame, text=text, font=("Arial", 12), 
            height=35, fg_color="#2B3642", hover_color="#FF5555", 
            anchor="w", command=cmd
        )
        btn.pack(fill="x", pady=2)