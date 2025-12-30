import customtkinter as ctk

class Ribbon(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, height=80, fg_color="#1a1a1a", corner_radius=0)
        self.app = app_instance
        
        # Tabs Container
        self.tabs = ctk.CTkTabview(self, height=70, fg_color="transparent", 
                                   segmented_button_selected_color="#66FCF1", 
                                   segmented_button_selected_hover_color="#55EBE0", 
                                   segmented_button_unselected_color="#333", 
                                   segmented_button_unselected_hover_color="#444", 
                                   text_color="black")
        self.tabs.pack(fill="both", padx=5, pady=0)
        
        # Define Tabs
        self.tabs.add("HOME")
        self.tabs.add("TOOLS")
        self.tabs.add("ENGINEERING")
        self.tabs.add("VIEW")
        
        # ==========================
        # TAB: HOME
        # ==========================
        self._add_ribbon_btn(self.tabs.tab("HOME"), "📂 Open Img", self.app.load_image)
        self._add_ribbon_btn(self.tabs.tab("HOME"), "📁 Open Project", self.app.open_project_logic)
        self._add_separator(self.tabs.tab("HOME"))
        self._add_ribbon_btn(self.tabs.tab("HOME"), "💾 Save Project", self.app.save_project_logic)
        self._add_ribbon_btn(self.tabs.tab("HOME"), "📤 Export Image", self.app.export_image_logic)
        
        # ==========================
        # TAB: TOOLS
        # ==========================
        self._add_ribbon_btn(self.tabs.tab("TOOLS"), "✋ Move", lambda: self.app.set_active_tool("move"))
        self._add_ribbon_btn(self.tabs.tab("TOOLS"), "📏 Ruler", lambda: self.app.set_active_tool("ruler"))
        self._add_ribbon_btn(self.tabs.tab("TOOLS"), "T Text", lambda: self.app.set_active_tool("text"))
        self._add_separator(self.tabs.tab("TOOLS"))
        self._add_ribbon_btn(self.tabs.tab("TOOLS"), "✂️ Crop", lambda: self.app.set_active_tool("crop"))
        self._add_ribbon_btn(self.tabs.tab("TOOLS"), "🪄 Magic", lambda: self.app.set_active_tool("magic"))
        
        # ==========================
        # TAB: ENGINEERING
        # ==========================
        self._add_ribbon_btn(self.tabs.tab("ENGINEERING"), "🤖 G-Code", self.app.run_gcode_gen)
        self._add_ribbon_btn(self.tabs.tab("ENGINEERING"), "📐 DXF Export", self.app.run_dxf_export)
        self._add_separator(self.tabs.tab("ENGINEERING"))
        self._add_ribbon_btn(self.tabs.tab("ENGINEERING"), "⚙️ Heightmap", self.app.run_cnc_heightmap)
        self._add_ribbon_btn(self.tabs.tab("ENGINEERING"), "🔲 Vector Prep", self.app.run_vector_prep)
        self._add_ribbon_btn(self.tabs.tab("ENGINEERING"), "🏁 Halftone", self.app.run_halftone)

        # ==========================
        # TAB: VIEW (SADA AKTIVAN!)
        # ==========================
        self._add_ribbon_btn(self.tabs.tab("VIEW"), "➕ Zoom In", self.app.view_zoom_in)
        self._add_ribbon_btn(self.tabs.tab("VIEW"), "➖ Zoom Out", self.app.view_zoom_out)
        self._add_ribbon_btn(self.tabs.tab("VIEW"), "🔍 100%", self.app.view_zoom_100)
        self._add_separator(self.tabs.tab("VIEW"))
        self._add_ribbon_btn(self.tabs.tab("VIEW"), "🔳 Fit Screen", self.app.view_fit_screen)
        self._add_ribbon_btn(self.tabs.tab("VIEW"), "📺 Fullscreen", self.app.toggle_fullscreen)
        self._add_separator(self.tabs.tab("VIEW"))
        self._add_ribbon_btn(self.tabs.tab("VIEW"), "👁️ Toggle Sidebar", self.app.toggle_sidebar_visibility)

    def _add_ribbon_btn(self, parent, text, command):
        btn = ctk.CTkButton(parent, text=text, width=80, height=30, 
                            fg_color="transparent", border_width=1, border_color="#444", 
                            text_color="white", hover_color="#66FCF1", 
                            anchor="center", command=command)
        btn.pack(side="left", padx=2, pady=5)

    def _add_separator(self, parent):
        # Mala vertikalna linija za razdvajanje grupa
        sep = ctk.CTkFrame(parent, width=2, height=20, fg_color="#333")
        sep.pack(side="left", padx=5, pady=10)  