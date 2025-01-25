import os
from flask import Flask, request, jsonify, render_template
from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, Label, Button, Entry, filedialog
from threading import Thread

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/memes"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_meme(image_path, top_text, bottom_text):
    try:
        # Open the image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # Load a font
        font_path = "arial.ttf"  # Ensure this font is available, or provide an alternative
        if not os.path.exists(font_path):
            raise FileNotFoundError("Font file not found. Please provide a valid 'arial.ttf' path.")

        font_size = int(img.width / 15)
        font = ImageFont.truetype(font_path, font_size)

        # Function to dynamically reduce font size to fit text within the image width
        def fit_text_within_width(text, font, max_width):
            while draw.textbbox((0, 0), text, font=font)[2] > max_width:
                font = ImageFont.truetype(font_path, font.size - 1)
            return font

        # Fit the top and bottom text within the image width
        font_top = fit_text_within_width(top_text, font, img.width - 20)
        font_bottom = fit_text_within_width(bottom_text, font, img.width - 20)

        # Calculate text positions
        top_text_size = draw.textbbox((0, 0), top_text, font=font_top)
        bottom_text_size = draw.textbbox((0, 0), bottom_text, font=font_bottom)

        top_text_position = ((img.width - (top_text_size[2] - top_text_size[0])) / 2, 10)
        bottom_text_position = ((img.width - (bottom_text_size[2] - bottom_text_size[0])) / 2, img.height - (bottom_text_size[3] - bottom_text_size[1]) - 10)

        # Add text to the image
        draw.text(top_text_position, top_text, font=font_top, fill="white", stroke_width=2, stroke_fill="black")
        draw.text(bottom_text_position, bottom_text, font=font_bottom, fill="white", stroke_width=2, stroke_fill="black")

        # Save the meme
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(image_path))
        img.save(output_path)
        return output_path

    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            top_text = request.form.get("top_text", "")
            bottom_text = request.form.get("bottom_text", "")

            if not top_text.strip() and not bottom_text.strip():
                return jsonify({"error": "Top and bottom text cannot both be empty."}), 400

            meme_path = generate_meme(file_path, top_text, bottom_text)

            if os.path.exists(meme_path):
                return jsonify({"meme_url": meme_path})
            else:
                return jsonify({"error": meme_path}), 500

        return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_server():
    app.run(debug=False, use_reloader=False)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_file.delete(0, 'end')
        entry_file.insert(0, file_path)

def create_meme_gui():
    file_path = entry_file.get()
    top_text = entry_top_text.get()
    bottom_text = entry_bottom_text.get()

    if not os.path.exists(file_path):
        label_status.config(text="Invalid file path!")
        return

    meme_path = generate_meme(file_path, top_text, bottom_text)
    if os.path.exists(meme_path):
        label_status.config(text=f"Meme created: {meme_path}")
    else:
        label_status.config(text=f"Error: {meme_path}")

# Start Flask server in a separate thread
server_thread = Thread(target=start_server, daemon=True)
server_thread.start()

# Create GUI
root = Tk()
root.title("Meme Generator")

Label(root, text="Image File:").grid(row=0, column=0, padx=5, pady=5)
entry_file = Entry(root, width=50)
entry_file.grid(row=0, column=1, padx=5, pady=5)
Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=5, pady=5)

Label(root, text="Top Text:").grid(row=1, column=0, padx=5, pady=5)
entry_top_text = Entry(root, width=50)
entry_top_text.grid(row=1, column=1, padx=5, pady=5)

Label(root, text="Bottom Text:").grid(row=2, column=0, padx=5, pady=5)
entry_bottom_text = Entry(root, width=50)
entry_bottom_text.grid(row=2, column=1, padx=5, pady=5)

Button(root, text="Create Meme", command=create_meme_gui).grid(row=3, column=0, columnspan=3, pady=10)

label_status = Label(root, text="")
label_status.grid(row=4, column=0, columnspan=3, pady=5)

root.mainloop()
