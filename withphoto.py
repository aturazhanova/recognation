from flask import Flask, request, jsonify
import os
from PIL import Image
from shiftlab_ocr.doc2text.crop import Crop
from shiftlab_ocr.doc2text.recognition import Recognizer
from shiftlab_ocr.doc2text.segmentation import Detector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

class Reader:
    def __init__(self, yolo_path="doc2text/yolov5", detector_weights="doc2text/weights/weights.pt", recognizer_weights="doc2text/weights/ocr_transformer_4h2l_simple_conv_64x256.pt"):
        self.recognizer = Recognizer()
        self.recognizer.load_model(recognizer_weights)
        self.detector = Detector(yolo_path, detector_weights)

    def doc2text(self, image_path):
        text = ''
        image = Image.open(image_path)
        boxes = self.detector.run(image_path)
        crops = []
        for box in boxes:
            cropped = image.crop((box[0], box[1], box[2], box[3]))
            crops.append(Crop([[box[0], box[1]], [box[2], box[3]]], img=cropped))
        crops = sorted(crops)
        for crop in crops:
            cropped_rgb = crop.img.convert("RGB")
            text += self.recognizer.run(cropped_rgb) + ' '
        
        return text, crops

reader = Reader()



@app.route('/extract-text', methods=['POST'])
def extract_text():
    print('reading file')
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Ensure the /tmp directory exists and is writable
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    file_path = os.path.join(tmp_dir, file.filename)
    file.save(file_path)

    try:
        text, crops = reader.doc2text(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(file_path)

    return jsonify({'text': text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
