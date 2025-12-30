import customtkinter as ctk
from tkinter import filedialog, Canvas, messagebox, simpledialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math 
import time

# UI Components
from .menu_bar import MainMenu
from .splash_screen import SplashScreen
from .dialogs.coffee_modal import CoffeeModal
from .layout.ribbon import Ribbon
from .layout.sidebar import Sidebar 
from .dialogs.new_project import NewProjectDialog

# Palettes
from .palettes.properties import PropertiesPanel 
from .palettes.filters import FilterBox
from .palettes.layer_panel import LayerPanel

# Backend
from backend.ai_engine import AIEngine
from backend.image_ops import ImageOpsEngine
from backend.project_manager import ProjectManager
from backend.layer_manager import LayerManager
from backend.gcode_engine import GCodeEngine

COLOR_BG = "#0B0C10"
COLOR_ACCENT = "#66FCF1"

class CypherLensApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. PRIPREMA (Dok je prozor sakriven)
        self.withdraw() # Sakrij glavni prozor
        self.title("CypherLens v10.0 - Enterprise Edition")
        self.configure(fg_color=COLOR_BG)
        ctk.set_appearance_mode("Dark")
        
        # Inicijalizacija podataka PRE layouta
        self._init_data()
        
        # Menu Bar
        self.menu = MainMenu(self)

        # Layout (Build UI in memory)
        print("Building UI layout...")
        self._setup_layout()
        
        if self.properties: 
            self.properties.update_for_tool(self.current_tool)
            
        self._setup_bindings()

        # 2. POKRETANJE SPLASH EKRANA (Non-blocking)
        self.splash = SplashScreen(self)
        self.splash.lift()
        self.splash.attributes('-topmost', True)
        
        # 3. OSMATRAČ: Čekaj da se splash ugasi, pa prikaži glavni prozor
        self.monitor_splash()

    def _init_data(self):
        """Inicijalizuje sve promenljive pre UI-a."""
        self.layer_manager = LayerManager()
        self.composite_image = None 
        self.tk_image = None
        self.preview_source_image = None 
        self.px_to_mm_scale = None 
        
        # Zoom & Pan
        self.zoom_level = 1.0; self.zoom_min = 0.1; self.zoom_max = 20.0
        self.pan_offset_x = 0; self.pan_offset_y = 0
        self.last_pan_x = 0; self.last_pan_y = 0
        
        # Tools
        self.current_tool = "move"; self.tool_color = "#FF0000"
        self.start_x = 0; self.start_y = 0; self.temp_item_id = None; self.is_moving_shape = False
        self.ruler_text_id = None
        
        # History
        self.history = []; self.redo_stack = []
        
        # UI References placeholders
        self.properties = None; self.filterbox = None; self.layerbox = None

    def monitor_splash(self):
        """Proverava svakih 100ms da li je splash ekran još uvek živ."""
        if self.splash.winfo_exists():
            # Ako splash postoji, čekaj još malo
            self.after(100, self.monitor_splash)
        else:
            # Splash je gotov! Prikaži glavni prozor.
            self.finish_loading()

    def finish_loading(self):
        """Prikazuje glavni prozor i pokreće Coffee Modal."""
        self.deiconify()
        self.state("zoomed") 
        # Forsiraj osvežavanje ekrana
        self.update()
        
        # Pokreni Coffee Modal sa malim zakašnjenjem
        self.after(1500, lambda: CoffeeModal(self))

    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Ribbon
        self.grid_rowconfigure(1, weight=1) # Body
        self.grid_rowconfigure(2, weight=0) # Status
        
        # Ribbon
        self.ribbon = Ribbon(self, self)
        self.ribbon.grid(row=0, column=0, sticky="new")
        
        # Body Frame
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 0)) # Sklonio sam padding da vidim da li to pravi problem
        
        # Sidebar (Pack Right)
        self.sidebar_container = Sidebar(self.body_frame, self)
        self.sidebar_container.pack(side="right", fill="y")
        
        # Canvas Container (Pack Left)
        self.canvas_container = ctk.CTkFrame(self.body_frame, fg_color="#111")
        self.canvas_container.pack(side="left", fill="both", expand=True)
        
        self.canvas = Canvas(self.canvas_container, bg="#111111", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Status Bar
        self.statusbar = ctk.CTkFrame(self, height=25, fg_color="#1F1F1F", corner_radius=0)
        self.statusbar.grid(row=2, column=0, sticky="ew")
        
        self.lbl_status_coords = ctk.CTkLabel(self.statusbar, text="X:0 Y:0", font=("Consolas", 11), width=100)
        self.lbl_status_coords.pack(side="left", padx=5)
        
        self.lbl_status_info = ctk.CTkLabel(self.statusbar, text="Ready", font=("Arial", 11), text_color="gray")
        self.lbl_status_info.pack(side="left", fill="x", expand=True)
        
        self.lbl_status_zoom = ctk.CTkLabel(self.statusbar, text="100%", width=50)
        self.lbl_status_zoom.pack(side="right")

    def _setup_bindings(self):
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel) 
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)
        self.canvas.bind("<Motion>", self.on_mouse_move_global)
        
        self.bind("<Control-z>", lambda e: self.run_undo())
        self.bind("<Control-y>", lambda e: self.run_redo())
        self.bind("<Return>", lambda e: self.apply_shape_to_image()) 
        self.bind("<Escape>", lambda e: self.set_active_tool("move"))
        
        self.bind("m", lambda e: self.set_active_tool("move"))
        self.bind("t", lambda e: self.set_active_tool("text"))
        self.bind("r", lambda e: self.set_active_tool("ruler"))
        self.bind("b", lambda e: self.set_active_tool("brush"))
        self.bind("c", lambda e: self.set_active_tool("crop"))
        self.bind("l", lambda e: self.set_active_tool("line"))

    # --- STATUS BAR ---
    def on_mouse_move_global(self, event):
        if not self.composite_image: return
        p = self.map_coords(event.x, event.y)
        if p:
            x, y = p
            w, h = self.composite_image.size
            if 0 <= x < w and 0 <= y < h:
                coord_text = f"X:{x*self.px_to_mm_scale:.1f} Y:{y*self.px_to_mm_scale:.1f} mm" if self.px_to_mm_scale else f"X:{x} Y:{y} px"
                self.lbl_status_coords.configure(text=coord_text)
            else:
                self.lbl_status_coords.configure(text="Out")

    def update_status(self, text): self.lbl_status_info.configure(text=text)

    # --- LAYER MANAGEMENT ---
    def refresh_layers_ui(self):
        if self.layerbox: self.layerbox.refresh_layer_list()
        self._update_canvas()

    def add_blank_layer(self):
        self.save_state()
        w, h = 1920, 1080
        if self.layer_manager.layers: w, h = self.layer_manager.layers[0].image.size
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.layer_manager.add_layer(img, "New Layer")
        self.refresh_layers_ui(); self.update_status("Added layer")

    def delete_layer(self):
        self.save_state()
        self.layer_manager.delete_active_layer()
        self.refresh_layers_ui(); self.update_status("Deleted layer")

    def layer_up(self): self.save_state(); self.layer_manager.move_layer_up(); self.refresh_layers_ui()
    def layer_down(self): self.save_state(); self.layer_manager.move_layer_down(); self.refresh_layers_ui()
    def select_layer(self, index): self.layer_manager.active_index = index; self.refresh_layers_ui()
    def toggle_layer_visibility(self, index): self.save_state(); layer = self.layer_manager.layers[index]; layer.visible = not layer.visible; self.refresh_layers_ui()

    def get_active_image(self):
        layer = self.layer_manager.get_active_layer()
        if not layer: self.update_status("No active layer!"); return None
        return layer.image

    def set_active_image(self, new_img):
        layer = self.layer_manager.get_active_layer()
        if layer: layer.image = new_img; self._update_canvas()

    def _update_canvas(self):
        self.canvas.delete("all")
        self.composite_image = self.layer_manager.render_composite()
        if not self.composite_image: return
        cw = self.canvas.winfo_width(); ch = self.canvas.winfo_height()
        img_w, img_h = self.composite_image.size
        new_w = int(img_w * self.zoom_level); new_h = int(img_h * self.zoom_level)
        resample_mode = Image.Resampling.LANCZOS if self.zoom_level <= 2.0 else Image.Resampling.NEAREST
        self.tk_image = ImageTk.PhotoImage(self.composite_image.resize((new_w, new_h), resample_mode))
        self.canvas.create_image((cw//2)+self.pan_offset_x, (ch//2)+self.pan_offset_y, image=self.tk_image, anchor="center")
        self.lbl_status_zoom.configure(text=f"{int(self.zoom_level*100)}%")

    # --- HISTORY ---
    def save_state(self):
        self.history.append(self.layer_manager.get_state_snapshot())
        if len(self.history) > 20: self.history.pop(0)
        self.redo_stack.clear(); self.update_status("State saved")

    def run_undo(self):
        if not self.history: return
        self.redo_stack.append(self.layer_manager.get_state_snapshot())
        self.layer_manager.restore_state_from_snapshot(self.history.pop())
        self.refresh_layers_ui(); self.update_status("Undo")

    def run_redo(self):
        if not self.redo_stack: return
        self.history.append(self.layer_manager.get_state_snapshot())
        self.layer_manager.restore_state_from_snapshot(self.redo_stack.pop())
        self.refresh_layers_ui(); self.update_status("Redo")

    # --- MOUSE EVENTS ---
    def on_mouse_down(self, event):
        img = self.get_active_image()
        if not img: return
        self.start_x = event.x; self.start_y = event.y

        if self.current_tool == "ruler":
            if self.temp_item_id: self.canvas.delete(self.temp_item_id)
            if self.ruler_text_id: self.canvas.delete(self.ruler_text_id)
            self.temp_item_id = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="#FF00FF", width=2, dash=(4, 4))
            return

        if self.current_tool == "magic":
            self.save_state(); p = self.map_coords(event.x, event.y)
            if p:
                try: tol = int(self.properties.slider_size.get()); new_img = ImageOpsEngine.magic_erase(img, p, tolerance=tol); self.set_active_image(new_img)
                except: pass
            return

        if self.current_tool == "text":
            if self.temp_item_id: self.apply_shape_to_image(); return
            self.temp_item_id = self.canvas.create_text(event.x, event.y, text="Type here...", fill=self.tool_color, font=("Arial", 50, "bold"), anchor="center")
            self.properties.show_apply_btn(); self.properties.entry_text.focus_set(); self.is_moving_shape = True; return

        if self.temp_item_id and self.current_tool in ["rect", "circle", "line", "crop", "text"]:
            bbox = self.canvas.bbox(self.temp_item_id); margin = 20 if self.current_tool == "text" else 5
            if bbox and (bbox[0]-margin <= event.x <= bbox[2]+margin) and (bbox[1]-margin <= event.y <= bbox[3]+margin): self.is_moving_shape = True; return
            else: self.apply_shape_to_image()

        if self.current_tool == "move": self.last_pan_x = event.x; self.last_pan_y = event.y
        elif self.current_tool in ["brush", "pencil"]: self.save_state(); self.last_draw_x = event.x; self.last_draw_y = event.y
        elif self.current_tool in ["rect", "circle", "line", "crop"]:
            if self.temp_item_id: self.canvas.delete(self.temp_item_id); self.temp_item_id = None; self.properties.hide_apply_btn()

    def on_mouse_drag(self, event):
        img = self.get_active_image()
        self.on_mouse_move_global(event)
        if not img: return

        if self.current_tool == "ruler" and self.temp_item_id:
            self.canvas.coords(self.temp_item_id, self.start_x, self.start_y, event.x, event.y)
            p1 = self.map_coords(self.start_x, self.start_y); p2 = self.map_coords(event.x, event.y)
            if p1 and p2:
                dist_px = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                text_str = f"{dist_px * self.px_to_mm_scale:.2f} mm" if self.px_to_mm_scale else f"{dist_px:.1f} px"
                if self.properties: self.properties.lbl_measure_result.configure(text=text_str)
                if self.ruler_text_id: self.canvas.delete(self.ruler_text_id)
                self.ruler_text_id = self.canvas.create_text(event.x+15, event.y+15, text=text_str, fill="#FF00FF", font=("Arial", 12, "bold"), anchor="w")
            return

        if self.is_moving_shape and self.temp_item_id:
            dx = event.x - self.start_x; dy = event.y - self.start_y; self.canvas.move(self.temp_item_id, dx, dy); self.start_x = event.x; self.start_y = event.y; return

        if self.current_tool == "move":
            dx = event.x - self.last_pan_x; dy = event.y - self.last_pan_y; self.pan_offset_x += dx; self.pan_offset_y += dy; self.last_pan_x = event.x; self.last_pan_y = event.y; self._update_canvas()

        elif self.current_tool in ["brush", "pencil"]:
            if not self.properties: return
            try: size = self.properties.slider_size.get()
            except: size = 5
            brush_shape = self.properties.combo_shape.get()
            if brush_shape == "Round": self.canvas.create_oval(event.x-size/2, event.y-size/2, event.x+size/2, event.y+size/2, fill=self.tool_color, outline=self.tool_color)
            else: self.canvas.create_rectangle(event.x-size/2, event.y-size/2, event.x+size/2, event.y+size/2, fill=self.tool_color, outline=self.tool_color)
            p = self.map_coords(event.x, event.y)
            if p:
                draw = ImageDraw.Draw(img); real_size = size / self.zoom_level
                if brush_shape == "Round": draw.ellipse([p[0]-real_size/2, p[1]-real_size/2, p[0]+real_size/2, p[1]+real_size/2], fill=self.tool_color)
                else: draw.rectangle([p[0]-real_size/2, p[1]-real_size/2, p[0]+real_size/2, p[1]+real_size/2], fill=self.tool_color)
            self.last_draw_x = event.x; self.last_draw_y = event.y

        elif self.current_tool in ["rect", "circle", "line", "crop"]:
            if self.temp_item_id: self.canvas.delete(self.temp_item_id)
            outline_c = self.tool_color; 
            if self.current_tool == "crop": outline_c = "#66FCF1"
            if self.current_tool in ["rect", "crop"]: self.temp_item_id = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=outline_c, width=2)
            elif self.current_tool == "circle": self.temp_item_id = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=outline_c, width=2)
            elif self.current_tool == "line": self.temp_item_id = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=outline_c, width=2)

    def on_mouse_up(self, event):
        self.is_moving_shape = False
        if self.current_tool == "ruler": pass
        elif self.current_tool in ["brush", "pencil"]: self._update_canvas()
        elif self.current_tool in ["rect", "circle", "line", "crop", "text"] and self.temp_item_id:
            if self.properties: self.properties.show_apply_btn()

    def apply_shape_to_image(self):
        if not self.temp_item_id: return
        img = self.get_active_image()
        if not img: return
        self.save_state(); coords = self.canvas.coords(self.temp_item_id)
        if not coords: return
        
        if self.current_tool == "text":
            cx, cy = coords[0], coords[1]; p = self.map_coords(cx, cy)
            if p:
                text = self.properties.entry_text.get(); font_n = self.properties.combo_font.get()
                try: size = int(self.properties.slider_size.get() / self.zoom_level)
                except: size=20
                new_img = ImageOpsEngine.add_text(img, p, text, self.tool_color, size, font_n); self.set_active_image(new_img)
        elif len(coords) == 4:
            x1, y1, x2, y2 = coords; p1 = self.map_coords(x1, y1); p2 = self.map_coords(x2, y2)
            if p1 and p2:
                if self.current_tool == "crop":
                    new_img = ImageOpsEngine.crop_image(img, (min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1]))); self.set_active_image(new_img); self.reset_view()
                else:
                    draw = ImageDraw.Draw(img)
                    try: width = int(self.properties.slider_size.get() / self.zoom_level)
                    except: width = 5
                    fill = self.tool_color if (hasattr(self.properties, 'fill_var') and self.properties.fill_var.get()) else None; outline = self.tool_color
                    if self.current_tool == "line": draw.line([p1, p2], fill=outline, width=width)
                    else:
                        rect_coords = [min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1])]
                        if self.current_tool == "rect": draw.rectangle(rect_coords, fill=fill, outline=outline, width=width)
                        elif self.current_tool == "circle": draw.ellipse(rect_coords, fill=fill, outline=outline, width=width)
                    self.set_active_image(img)
        self.canvas.delete(self.temp_item_id); self.temp_item_id = None; 
        if self.properties: self.properties.hide_apply_btn()
        self._update_canvas()

    # --- HELPERS ---
    def set_active_tool(self, tool_name):
        if self.temp_item_id: self.apply_shape_to_image()
        if self.ruler_text_id: self.canvas.delete(self.ruler_text_id); self.ruler_text_id = None
        if self.preview_source_image: self.apply_adjustment() 
        self.current_tool = tool_name
        self.update_status(f"Tool: {tool_name.upper()}")
        
        img = self.get_active_image()
        if tool_name in ["adj_brightness", "adj_blur", "adj_sharpen", "adj_threshold"] and img: self.preview_source_image = img.copy()
        else: self.preview_source_image = None

        if self.properties: self.properties.update_for_tool(tool_name)
        
        if tool_name == "move": self.canvas.config(cursor="fleur")
        elif tool_name == "magic": self.canvas.config(cursor="spider")
        elif tool_name == "text": self.canvas.config(cursor="xterm")
        elif tool_name == "ruler": self.canvas.config(cursor="crosshair")
        elif tool_name in ["brush", "pencil"]: self.canvas.config(cursor="pencil")
        elif tool_name in ["rect", "circle", "line", "crop"]: self.canvas.config(cursor="crosshair")
        else: self.canvas.config(cursor="arrow")
        
        if tool_name == "remove_bg": self.run_remove_bg()
        elif tool_name == "save": self.save_project_logic()

    def update_adjustment_preview(self, value):
        if not self.preview_source_image: return
        val = float(value)
        if self.current_tool == "adj_brightness":
            factor = 1.0 + (val / 100.0); self.set_active_image(ImageOpsEngine.adjust_brightness(self.preview_source_image, factor))
        elif self.current_tool == "adj_blur":
            if val == 0: self.set_active_image(self.preview_source_image.copy())
            else: self.set_active_image(ImageOpsEngine.filter_blur(self.preview_source_image, radius=val))
        elif self.current_tool == "adj_sharpen":
             if val > 0: self.set_active_image(ImageOpsEngine.filter_sharpen(self.preview_source_image))
             else: self.set_active_image(self.preview_source_image.copy())
        elif self.current_tool == "adj_threshold":
            self.set_active_image(ImageOpsEngine.apply_threshold(self.preview_source_image, val))
        self._update_canvas()

    def apply_adjustment(self):
        if self.preview_source_image:
            self.save_state(); self.preview_source_image = None; self.set_active_tool("move")
            # Toolbar is technically gone, but this is safe logic

    # --- LOADING & SAVING ---
    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            img = Image.open(path).convert("RGBA")
            if not self.layer_manager.layers: self.layer_manager.add_layer(img, "Background")
            else: self.layer_manager.add_layer(img, f"Imported {len(self.layer_manager.layers)}")
            self.history.clear(); self.reset_view(); self.refresh_layers_ui(); self.update_status("Image loaded")

    def set_new_project(self, img):
        self.layer_manager = LayerManager(); self.layer_manager.add_layer(img, "Background")
        self.history.clear(); self.reset_view(); self.refresh_layers_ui(); self.update_status("New project created")

    def export_image_logic(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
        if filepath:
            final = self.layer_manager.render_composite()
            final.save(filepath); messagebox.showinfo("Export", "Saved!"); self.update_status(f"Exported to {filepath}")

    def open_new_project_dialog(self): NewProjectDialog(self)
   # --- PROJECT MANAGEMENT ---
    
    def save_project_logic(self):
        """Čuva ceo projekat sa svim slojevima."""
        if not self.layer_manager.layers:
            messagebox.showwarning("Empty", "Nothing to save!")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".cph", 
            filetypes=[("CypherLens Project", "*.cph")]
        )
        
        if filepath:
            self.configure(cursor="watch")
            self.update()
            success = ProjectManager.save_project(self.layer_manager, filepath)
            self.configure(cursor="arrow")
            
            if success:
                messagebox.showinfo("Success", "Project saved successfully!")
                self.update_status(f"Saved: {filepath}")
            else:
                messagebox.showerror("Error", "Failed to save project.")

    def open_project_logic(self):
        """Otvara postojeći projekat."""
        filepath = filedialog.askopenfilename(
            filetypes=[("CypherLens Project", "*.cph")]
        )
        
        if filepath:
            self.configure(cursor="watch")
            self.update()
            
            # Resetujemo istoriju jer učitavamo novi projekat
            self.history.clear()
            self.redo_stack.clear()
            
            success = ProjectManager.load_project(filepath, self.layer_manager)
            self.configure(cursor="arrow")
            
            if success:
                self.refresh_layers_ui()
                self.reset_view()
                messagebox.showinfo("Success", "Project loaded!")
                self.update_status(f"Loaded: {filepath}")
            else:
                messagebox.showerror("Error", "Failed to load project.")

    # --- FILTERS ---
    def run_remove_bg(self):
        img = self.get_active_image()
        if img:
            self.save_state()
            self.configure(cursor="watch")
            self.update()
            try:
                n = AIEngine.remove_background(img)
                if n:
                    self.set_active_image(n)
                    self.update_status("BG Removed")
            except:
                pass
            finally:
                self.configure(cursor="arrow")

    def run_cnc_heightmap(self):
        img = self.get_active_image()
        if img:
            self.save_state()
            self.configure(cursor="watch")
            self.update()
            try:
                d = AIEngine.generate_depth_map(img)
                if d:
                    self.set_active_image(d)
                    messagebox.showinfo("AI Depth", "Generated!")
                    self.update_status("Heightmap created")
            except:
                self.run_undo()
            finally:
                self.configure(cursor="arrow")
    def run_vector_prep(self):
        img = self.get_active_image()
        if img: self.save_state(); self.set_active_image(ImageOpsEngine.generate_edge_map(img)); self.update_status("Edges extracted")
    def run_normal_map(self):
        img = self.get_active_image()
        if img: self.save_state(); self.set_active_image(ImageOpsEngine.generate_normal_map(img))
    def run_rotate_left(self): img = self.get_active_image(); (self.save_state(), self.set_active_image(ImageOpsEngine.rotate_image(img, 90))) if img else None
    def run_filter_bw(self): img = self.get_active_image(); (self.save_state(), self.set_active_image(ImageOpsEngine.filter_grayscale(img).convert("RGBA"))) if img else None
    def run_filter_sepia(self): img = self.get_active_image(); (self.save_state(), self.set_active_image(ImageOpsEngine.filter_sepia(img).convert("RGBA"))) if img else None
    def run_filter_invert(self): img = self.get_active_image(); (self.save_state(), self.set_active_image(ImageOpsEngine.filter_invert(img).convert("RGBA"))) if img else None
    def run_auto_enhance(self): img = self.get_active_image(); (self.save_state(), self.set_active_image(ImageOpsEngine.auto_enhance(img).convert("RGBA"))) if img else None
    
    def run_halftone(self):
        img = self.get_active_image()
        if img: self.save_state(); self.set_active_image(ImageOpsEngine.apply_dithering(img)); messagebox.showinfo("Halftone", "Dithered!"); self.update_status("Halftone applied")

    def run_gcode_gen(self):
        img = self.get_active_image()
        if not img: messagebox.showwarning("Warning", "No active layer!"); return
        filepath = filedialog.asksaveasfilename(defaultextension=".nc", filetypes=[("G-Code", "*.nc")])
        if filepath:
            self.configure(cursor="watch"); self.update()
            pixel_res = self.px_to_mm_scale if self.px_to_mm_scale else 0.1
            try: GCodeEngine.generate_raster_gcode(img, filepath, pixel_size=pixel_res); messagebox.showinfo("Success", "G-Code Saved!")
            except Exception as e: messagebox.showerror("Error", str(e))
            finally: self.configure(cursor="arrow")

    def run_dxf_export(self):
        img = self.get_active_image()
        if not img: 
            messagebox.showwarning("Warning", "No image to vectorize!")
            return
            
        # Pitaj korisnika gde da sačuva
        filepath = filedialog.asksaveasfilename(
            defaultextension=".dxf", 
            filetypes=[("DXF Drawing", "*.dxf")],
            title="Export Vectors for CNC/Laser"
        )
        
        if filepath:
            self.configure(cursor="watch")
            self.update()
            try:
                # Pozivamo novu funkciju iz ImageOpsEngine
                count = ImageOpsEngine.export_dxf_vectors(img, filepath)
                
                if count > 0:
                    messagebox.showinfo("Success", f"Vectorization Complete!\nExported {count} contours to DXF.")
                    self.update_status(f"DXF Saved: {count} paths")
                else:
                    messagebox.showwarning("Warning", "No contours found! Try adjusting brightness/contrast first.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Vectorization failed: {str(e)}")
                print(e)
            finally:
                self.configure(cursor="arrow")

    def calibrate_ruler(self):
        if not self.temp_item_id or self.current_tool != "ruler": messagebox.showwarning("Calib", "Draw line first!"); return
        coords = self.canvas.coords(self.temp_item_id)
        if not coords: return
        p1 = self.map_coords(coords[0], coords[1]); p2 = self.map_coords(coords[2], coords[3])
        dist_px = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        if dist_px < 5: messagebox.showwarning("Error", "Too short!"); return
        dialog = ctk.CTkInputDialog(text=f"Px: {dist_px:.1f}\nReal MM:", title="Calibrate")
        val = dialog.get_input()
        if val and val.replace('.', '', 1).isdigit():
            mm = float(val)
            if mm > 0: self.px_to_mm_scale = mm / dist_px; self.properties.lbl_calib_info.configure(text=f"1px = {self.px_to_mm_scale:.4f}mm"); messagebox.showinfo("OK", "Calibrated!")

    # --- UTILS ---
    def map_coords(self, cx, cy):
        if not self.tk_image or not self.composite_image: return None
        cw = self.canvas.winfo_width(); ch = self.canvas.winfo_height()
        center_x = (cw // 2) + self.pan_offset_x; center_y = (ch // 2) + self.pan_offset_y
        img_disp_w = self.tk_image.width(); img_disp_h = self.tk_image.height()
        top_left_x = center_x - (img_disp_w // 2); top_left_y = center_y - (img_disp_h // 2)
        rel_x = cx - top_left_x; rel_y = cy - top_left_y
        real_x = int(rel_x / self.zoom_level); real_y = int(rel_y / self.zoom_level)
        return (real_x, real_y)
    
    def on_mouse_wheel(self, event):
        if not self.composite_image: return
        if event.num == 5 or event.delta < 0: factor = 0.9
        else: factor = 1.1
        self.zoom_level *= factor; 
        if self.zoom_level < self.zoom_min: self.zoom_level = self.zoom_min
        if self.zoom_level > self.zoom_max: self.zoom_level = self.zoom_max
        self._update_canvas()

    def reset_view(self): 
        self.pan_offset_x = 0; self.pan_offset_y = 0; self._update_canvas()
    def toggle_toolbar(self): (self.toolbar.deiconify() if self.menu.view_toolbar_var.get() else self.toolbar.withdraw()) if self.toolbar else None
    def toggle_properties(self): (self.properties.deiconify() if self.menu.view_props_var.get() else self.properties.withdraw()) if self.properties else None
    def toggle_filters(self): (self.filterbox.deiconify() if self.menu.view_filters_var.get() else self.filterbox.withdraw()) if self.filterbox else None
    def toggle_layers(self): (self.layerbox.deiconify() if self.menu.view_layers_var.get() else self.layerbox.withdraw()) if self.layerbox else None
    def run_filter_blur(self): pass
    def run_filter_sharpen(self): pass
    def apply_brightness_step(self): pass
    def on_text_type(self, event):
        if self.current_tool == "text" and self.temp_item_id: self.canvas.itemconfig(self.temp_item_id, text=self.properties.entry_text.get() or "Type...")
    def on_text_size_change(self, value):
        if self.current_tool == "text" and self.temp_item_id: self.canvas.itemconfig(self.temp_item_id, font=(self.properties.combo_font.get(), int(float(value)), "bold"))
    def on_font_change(self, font_name):
        if self.current_tool == "text" and self.temp_item_id: 
            try: self.canvas.itemconfig(self.temp_item_id, font=(font_name, int(self.properties.slider_size.get()), "bold"))
            except: pass

            # --- VIEW CONTROL LOGIC (DODATAK ZA VIEW TAB) ---

    def view_zoom_in(self):
        """Povećava zoom za 20%."""
        if not self.composite_image: return
        self.zoom_level *= 1.2
        if self.zoom_level > self.zoom_max: self.zoom_level = self.zoom_max
        self._update_canvas()

    def view_zoom_out(self):
        """Smanjuje zoom za 20%."""
        if not self.composite_image: return
        self.zoom_level *= 0.8
        if self.zoom_level < self.zoom_min: self.zoom_level = self.zoom_min
        self._update_canvas()

    def view_zoom_100(self):
        """Vraća prikaz na 100% (Realna veličina)."""
        if not self.composite_image: return
        self.zoom_level = 1.0
        self._update_canvas()
        self.update_status("Zoom: 100%")

    def view_fit_screen(self):
        """Resetuje pan i zoom (Fit to Screen)."""
        self.reset_view()
        self.update_status("View Reset")

    def toggle_sidebar_visibility(self):
        """Prikazuje ili sakriva desni panel (Sidebar)."""
        if self.sidebar_container.winfo_viewable():
            self.sidebar_container.pack_forget() # Sakrij
            self.update_status("Sidebar Hidden")
        else:
            self.sidebar_container.pack(side="right", fill="y") # Prikaži
            self.update_status("Sidebar Visible")
            
    def toggle_fullscreen(self):
        """Menja između Fullscreen i Windowed moda."""
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
        else:
            self.attributes("-fullscreen", True)