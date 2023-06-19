Шаг 1: Установка зависимостей

Убедитесь, что у вас установлен Python версии 3.x.
Откройте командную строку или терминал.
Выполните следующую команду для установки необходимых пакетов:


```
pip install flask pytesseract pillow
```

Шаг 2: Создание проекта

- Создайте новую папку для вашего проекта.
- В этой папке создайте файл app.py.
  
Шаг 3: Кодирование приложения Flask

- Откройте файл app.py в текстовом редакторе или интегрированной среде разработки (IDE).
- Скопируйте следующий код в файл app.py:

```
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

```

Шаг 4: Создание шаблонов HTML

- В папке проекта создайте папку templates.
- В папке templates создайте файл index.html со следующим содержимым:

```
<!DOCTYPE html>
<html>
  <head>
    <title>OCR Web Interface</title>
  </head>
  <body>
    <h1>OCR Web Interface</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <input type="submit" value="Upload">
    </form>
  </body>
</html>

```

В папке templates создайте файл result.html со следующим содержимым:



```
<!DOCTYPE html>
<html>
  <head>
    <title>OCR Result</title>
  </head>
  <body>
    <h1>OCR Result</h1>
    <p>{{ text }}</p>
  </body>
</html>

```

Шаг 5: Запуск приложения

В командной строке или терминале перейдите в папку с вашим проектом.
Выполните следующую команду для запуска приложения:


```
python app.py

```

Шаг 6: Использование веб-интерфейса

Откройте веб-браузер и перейдите по адресу http://localhost:5000/.
Вы увидите главную страницу с формой загрузки изображения.
Выберите изображение для загрузки и нажмите кнопку "Upload".
После загрузки изображения будет выполнено распознавание текста с помощью Tesseract, и результат распознавания будет отображен на странице с результатом.
