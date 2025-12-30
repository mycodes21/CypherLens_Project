# 🔍 CypherLens – Industrial Image Engineering Suite

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/mycodes21)

**CypherLens** is a specialized Python-based desktop application designed to bridge the gap between **Raster Images** and **CNC/Laser Manufacturing**.

Unlike standard photo editors, CypherLens focuses on converting images into machine-readable formats, extracting precise vectors, creating depth maps for 3D relief, and generating G-Code for laser engraving.

---

## 🚀 Key Features

### 🛠️ Engineering Tools

- **Raster to G-Code:** Generate `.nc` files directly from images for Laser Raster Engraving.
- **DXF Export:** Convert image edges into `.dxf` vectors for CAD/CAM (AutoCAD, Fusion360, ArtCAM).
- **AI Depth Maps:** Uses the "Depth Anything" AI model to generate high-quality 3D bas-relief heightmaps from 2D photos.
- **Ruler & Calibration:** Measure distances in pixels and calibrate the tool to real-world units (Millimeters).

### 🎨 Image Processing

- **Layer System:** Full support for multiple layers (images, text, shapes) with visibility and opacity controls.
- **Smart Background Removal:** AI-powered background removal (Rembg).
- **Computer Vision Edges:** Advanced Canny Edge Detection for precise vector preparation.
- **Halftoning:** Dithering algorithms (Floyd-Steinberg) for preparing photos for laser engraving.
- **Manual Thresholding:** Precise binary control for contour extraction.

### 🖥️ User Experience

- **Modern UI:** Dark-themed interface built with `CustomTkinter`.
- **Live Preview:** Real-time adjustments for brightness, blur, sharpen, and threshold.
- **History System:** Robust Undo/Redo functionality for layer operations.
- **Interactive Canvas:** Pan, Zoom (up to 1000%), and draggable elements.
- **Status Bar:** Real-time coordinates (mm/px) and RGB color picker.

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- PIP (Python Package Installer)

### Setup

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/mycodes21/CypherLens_Project.git](https://github.com/mycodes21/CypherLens_Project.git)
    cd CypherLens_Project
    ```

2.  **Create a Virtual Environment (Optional but recommended):**

    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: The first run might take a minute to download AI models for Depth Estimation and Background Removal)._

4.  **Run the App:**
    ```bash
    python main.py
    ```

---

## 🎮 Controls & Shortcuts

| Key        | Tool / Action | Description                                     |
| :--------- | :------------ | :---------------------------------------------- |
| **M**      | Move / Pan    | Drag to move canvas.                            |
| **T**      | Text Tool     | Click to add text overlay.                      |
| **R**      | Ruler         | Measure distance (requires calibration for MM). |
| **B**      | Brush         | Simple drawing tool.                            |
| **C**      | Crop          | Crop the active layer.                          |
| **L**      | Line          | Draw straight lines.                            |
| **Esc**    | Cancel        | Switch back to Move tool.                       |
| **Ctrl+Z** | Undo          | Revert last change.                             |
| **Ctrl+Y** | Redo          | Re-apply last change.                           |
| **Scroll** | Zoom          | Zoom In/Out on cursor.                          |

---

## 🏗️ Project Structure

- `main.py` - Entry point of the application.
- `ui/` - User Interface components (Windows, Palettes, Dialogs).
- `backend/` - Core logic engines:
  - `layer_manager.py`: Handles the stack of images and history.
  - `ai_engine.py`: Wrappers for Transformers and Rembg models.
  - `image_ops.py`: OpenCV and PIL manipulations.
  - `gcode_engine.py`: Raster to G-Code conversion logic.

---

## 🔮 Roadmap

- [ ] **UI Polish:** Modernizing icons and spacing.
- [ ] **Vectorization:** Trace Bitmap to SVG (Potrace integration).
- [ ] **Standalone Executable:** .EXE packaging for easy distribution.

---

**License:** MIT License  
**Author:** [NN MACHINING & Engineering](https://github.com/mycodes21)

☕ **Support the project:** [Buy me a coffee](https://buymeacoffee.com/mycodes21)
