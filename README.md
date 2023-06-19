Шаг 1: Установка зависимостей

Убедитесь, что у вас установлен Python версии 3.x.
Откройте командную строку или терминал.
Выполните следующую команду для установки необходимых пакетов:


```
pip install Flask
pip install pytesseract
pip install Pillow
pip install PyPDF2
```
Для поддержки русского языка вам также понадобятся дополнительные данные языка для pytesseract. Вот команда для установки данных русского языка:

```
pip install pytesseract[rus]

```

Шаг 2: Создание шаблонов HTML
Создайте два файла шаблонов HTML: index.html и result.html. 
Создайте папку с именем templates в том же каталоге, где находится app.py, и поместите эти файлы внутрь папки templates. 
Вот примеры содержимого этих файлов (код остается таким же):

index.html


```
<!DOCTYPE html>
<html>
<head>
    <title>Upload File</title>
</head>
<body>
    <h1>Upload File</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>


```
  
result.html


```
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
</head>
<body>
    <h1>Result</h1>
    <pre>{{ text }}</pre>
</body>
</html>


```



