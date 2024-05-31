from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Open the image file
        image = Image.open(file.stream)
        
        # Preprocessing the image
        image = image.convert('L')  # Convert to grayscale
        image = ImageOps.invert(image)  # Invert image colors
        image = image.filter(ImageFilter.MedianFilter())  # Apply median filter
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # Enhance contrast

        # Optional: Resize image to make text more clear for OCR
        basewidth = 1000
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
        
        # Use Tesseract to do OCR on the image with Russian language
        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(image, lang='rus', config=custom_config)
        print("Extracted text:", extracted_text)  # Debugging line
        response = {"message": "Text extracted successfully", "text": extracted_text}
    except Exception as e:
        print("Error:", str(e))  # Debugging line
        response = {"error": str(e)}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
