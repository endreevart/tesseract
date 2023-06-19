From flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pytesseract
import os
from PIL import Image
from PyPDF2 import PdfReader
import pandas as pd
import re
import cv2

app = Flask(__name__)

# Путь для загрузки файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Разрешенные типы файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    # Загрузка изображения и применение предварительной обработки
    image = cv2.imread(image_path)

    # Применение методов предварительной обработки (примеры)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Преобразование в оттенки серого
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # Бинаризация

    return image

def extract_text_from_image(image_path):
    # Распознавание текста в изображении с помощью pytesseract
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang='rus+eng')
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

def create_table_from_text(text):
    # Разделение текста на строки и столбцы
    rows = text.split('\n')
    table_data = [row.split('\t') for row in rows]

    # Преобразование данных в DataFrame
    df = pd.DataFrame(table_data[1:], columns=table_data[0])

    return df

def bold_numbers_in_text(text):
    # Регулярное выражение для поиска чисел
    pattern = r'\b\d+\b'

    # Поиск чисел в тексте и обрамление их тегами <b></b> для жирного шрифта
    bold_text = re.sub(pattern, lambda match: f"<b>{match.group()}</b>", text)

    return bold_text

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

        # Преобразование текста в таблицу
        table = create_table_from_text(text)
        markup_text = bold_numbers_in_text(text)  # Добавлено создание разметки текста

        return render_template('result.html', table=table.to_html(index=False, classes='table'), markup_text=markup_text)  # Включение разметки текста в передачу шаблону
    else:
        return 'Invalid file type'

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        edited_text = request.form['edited_text']
        # Здесь можно выполнить обработку отредактированного текста
        table = create_table_from_text(edited_text)
        markup_text = bold_numbers_in_text(edited_text)  # Добавлено создание разметки текста

        return render_template('result.html', table=table.to_html(index=False, classes='table'), markup_text=markup_text)  # Включение разметки текста в передачу шаблону

    return render_template('result.html')

if __name__ == '__main__':
    # Создание папки "uploads", если она не существует
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
