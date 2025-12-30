from tkinter import Menu, BooleanVar

class MainMenu:
    def __init__(self, parent):
        self.parent = parent
        self.menu_bar = Menu(parent)
        parent.config(menu=self.menu_bar)

        # --- VARIJABLE ZA TOGGLE MENIJE ---
        # Ove promenljive pamte da li je nešto čekirano ili ne
        self.view_toolbar_var = BooleanVar(value=True)
        self.view_props_var = BooleanVar(value=True)
        self.view_filters_var = BooleanVar(value=False)
        self.view_layers_var = BooleanVar(value=True) # <--- OVO JE FALILO i pravilo grešku!

        self._setup_file_menu()
        self._setup_edit_menu()
        self._setup_view_menu()

    def _setup_file_menu(self):
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        file_menu.add_command(label="New Project...", command=self.parent.open_new_project_dialog)
        file_menu.add_command(label="Open Project...", command=self.parent.open_project_logic)
        file_menu.add_command(label="Save Project", command=self.parent.save_project_logic)
        file_menu.add_separator()
        file_menu.add_command(label="Import Image...", command=self.parent.load_image)
        file_menu.add_command(label="Export Final Image...", command=self.parent.export_image_logic)
        file_menu.add_command(label="Export DXF...", command=self.parent.run_dxf_export)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.parent.destroy)

    def _setup_edit_menu(self):
        edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.parent.run_undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.parent.run_redo)

    def _setup_view_menu(self):
        view_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

        view_menu.add_checkbutton(
            label="Sidebar visibility   ", 
            onvalue=True, offvalue=False, 
            variable=self.view_toolbar_var, 
            command=self.parent.toggle_sidebar_visibility
        )
        
        view_menu.add_checkbutton(
            label="Show Properties", 
            onvalue=True, offvalue=False, 
            variable=self.view_props_var, 
            command=self.parent.toggle_properties
        )
        
        view_menu.add_checkbutton(
            label="Show Filters", 
            onvalue=True, offvalue=False, 
            variable=self.view_filters_var, 
            command=self.parent.toggle_filters
        )
        
        # Ovo je linija koja je pucala jer 'view_layers_var' nije bio definisan
        view_menu.add_checkbutton(
            label="Show Layers", 
            onvalue=True, offvalue=False, 
            variable=self.view_layers_var, 
            command=self.parent.toggle_layers
        )