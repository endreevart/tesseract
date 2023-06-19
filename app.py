from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pytesseract
import os
from PIL import Image
from PyPDF2 import PdfReader

app = Flask(__name__)

# Путь для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Разрешенные типы файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if filename.lower().endswith('.pdf'):
            # Обработка PDF файла
            # Распознавание текста в PDF
            text = extract_text_from_pdf(file_path)
        else:
            # Обработка изображения
            # Распознавание текста в изображении
            text = extract_text_from_image(file_path)
        # Удаление загруженного файла после обработки
        os.remove(file_path)
        return render_template('result.html', text=text)
    else:
        return 'Invalid file type'

def extract_text_from_image(image_path):
    # Распознавание текста в изображении с помощью pytesseract
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='rus')
    return text

def extract_text_from_pdf(pdf_path):
    # Распознавание текста в PDF с помощью PyPDF2 и pytesseract
    text = ''
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text
    return text

if __name__ == '__main__':
    # Создание папки "uploads", если она не существует
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
