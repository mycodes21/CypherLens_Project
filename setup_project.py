import os

# Ime glavnog foldera
root_dir = "CypherLens_Project"

# Struktura foldera i fajlova
folders = [
    "assets",
    "backend",
    "ui",
    "ui/palettes"
]

files = {
    "main.py": "# Ulazna tačka aplikacije\nfrom ui.main_window import CypherLensApp\n\nif __name__ == '__main__':\n    app = CypherLensApp()\n    app.mainloop()",
    "requirements.txt": "customtkinter\npillow\nrembg\nonnxruntime",
    "README.md": "# CypherLens v2.0\nOpen Source AI Image Tool",
    
    # Backend fajlovi
    "backend/__init__.py": "",
    "backend/ai_engine.py": "# Ovde ide rembg logika i upscale",
    "backend/image_ops.py": "# Ovde ide crop, resize, save logika",
    
    # UI fajlovi
    "ui/__init__.py": "",
    "ui/main_window.py": "# Glavni prozor (Sidebar + Canvas)",
    "ui/menu_bar.py": "# File, Edit, View meniji",
    
    # Palete
    "ui/palettes/__init__.py": "",
    "ui/palettes/base_palette.py": "# Osnovna klasa za Grip Bar i Dragging logiku",
    "ui/palettes/tools.py": "# ToolBox klasa",
    "ui/palettes/filters.py": "# FilterBox klasa",
}

def create_structure():
    # 1. Kreiranje glavnog foldera
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        print(f"✅ Napravljen folder: {root_dir}")
    else:
        print(f"⚠️ Folder {root_dir} već postoji!")

    # 2. Kreiranje podfoldera
    for folder in folders:
        path = os.path.join(root_dir, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"   📂 Napravljen: {folder}")

    # 3. Kreiranje fajlova
    for file_path, content in files.items():
        full_path = os.path.join(root_dir, file_path)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   📄 Napravljen: {file_path}")
    
    print("\n🚀 GOTOVO! Projekat je spreman.")
    print(f"Sada otvori folder '{root_dir}' u svom editoru (VS Code/PyCharm).")

if __name__ == "__main__":
    create_structure()