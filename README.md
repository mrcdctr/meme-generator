# Meme Generator App

A Python-based meme generator app that allows users to create memes with custom text on top and bottom of images. The app provides both a web-based interface (using Flask) and a graphical user interface (GUI) (using Tkinter) for flexibility.

## Features

- Upload images and add custom text at the top and bottom.
- Dynamically adjust text size to fit the image.
- Supports common image formats (PNG, JPG, JPEG).
- Web interface powered by Flask.
- Desktop GUI interface powered by Tkinter.
- Saves generated memes in a local directory.

## Requirements

- Python 3.7+
- Dependencies:
  - Flask
  - Pillow (PIL)
  - Tkinter (included with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mrcdctr/meme-generator.git
   cd meme-generator
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows, use venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have a font file (e.g., `arial.ttf`) in the project directory. If not, download or specify the path to an available font on your system.

## Usage

### Run the Web Interface

1. Start the Flask app:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
http://127.0.0.1:5000
   ```

3. Upload an image, enter top and bottom text, and generate your meme!

### Run the GUI Interface

1. Simply execute the script:
   ```bash
   python app.py
   ```

2. The GUI will launch, allowing you to browse for images, add text, and create memes.

## Directory Structure

```
.
├── app.py            # Main application file
├── requirements.txt  # List of Python dependencies
├── static/           # Static files (uploads and memes)
│   ├── uploads/      # Uploaded images
│   └── memes/        # Generated memes
├── templates/        # HTML templates for Flask
└── README.md         # Project documentation
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or encounter bugs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy creating memes!
