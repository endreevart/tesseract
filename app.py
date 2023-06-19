from flask import Flask, render_template, request
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Получаем изображение из запроса
    image_file = request.files['image']
    image = Image.open(image_file)

    # Применяем Tesseract для распознавания текста
    text = pytesseract.image_to_string(image)

    return render_template('result.html', text=text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
