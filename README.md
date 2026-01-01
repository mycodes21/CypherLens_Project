# 🔍 CypherLens – Industrial Image Engineering Suite

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/mycodes21)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

**CypherLens** is a specialized Python-based desktop application designed to bridge the gap between **Raster Images** and **CNC/Laser Manufacturing**.

Unlike standard photo editors, CypherLens focuses on converting images into machine-readable formats, extracting precise vectors, creating depth maps for 3D relief, and generating G-Code for laser engraving.

![App Screenshot](assets/screenshot_main.png)

---

## 🚀 Key Features

### 🛠️ Engineering Tools

- **Raster to G-Code:** Generate `.nc` files directly from images for Laser Raster Engraving.
- **DXF Export:** Convert image edges into `.dxf` vectors for CAD/CAM (AutoCAD, Fusion360, ArtCAM).
- **AI Depth Maps:** Generates high-quality 3D bas-relief heightmaps from 2D photos for CNC carving.
- **Ruler & Calibration:** Measure distances in pixels and calibrate the tool to real-world units (Millimeters).

### 🎨 Image Processing

- **Layer System:** Full support for multiple layers (images, text, shapes) with visibility and opacity controls.
- **Smart Background Removal:** AI-powered background removal (Rembg).
- **QR Code Generator:** Instantly create and insert QR codes into your projects.
- **Computer Vision Edges:** Advanced Canny Edge Detection for precise vector preparation.
- **Halftoning:** Dithering algorithms (Floyd-Steinberg) for preparing photos for laser engraving.

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

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mycodes21/CypherLens_Project.git](https://github.com/mycodes21/CypherLens_Project.git)
   cd CypherLens_Project
   ```
