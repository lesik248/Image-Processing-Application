from flask import Flask, render_template, request, redirect, url_for
import os
import cv2 as cv
from io import BytesIO
import base64

app = Flask(__name__) # original inage in color is displayed incorrectly

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tif', 'bmp', 'pcx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename): # Проверка расширения файла
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ImageProcessor:
    
    # Инициализация процессора изображения. Загружает изображение с указанного пути.
    def __init__(self, image_path):
        self.image = cv.imread(image_path)

    # конвертирует изображение OpenCV в Base64 для встройки в HTML
    def convert_to_base64(self, cv_image):
        """Convert an OpenCV image to a Base64 string."""
        _, buffer = cv.imencode('.png', cv_image)  # Ensure the input is RGB
        if not _:
            raise ValueError("Image encoding failed.")
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/png;base64,{encoded_image}"


    # Возвращает исходное изображение в формате RGB (для отображения в браузере).
    def original_image(self):
        #rgb_image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB) 
        return self.convert_to_base64(self.image)
    
    def global_threshold(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        return self.convert_to_base64(thresh)

    def adaptive_threshold(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2) #бинаризация
        return self.convert_to_base64(thresh)

    # Повышает контраст изображения с использованием выравнивания гистограммы.
    def linear_contrast(self):
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        equalized = cv.equalizeHist(gray) 
        return self.convert_to_base64(equalized)

    # Поэлементные операции
    def negative(self):
        """Calculate the negative of the image."""
        negative = 255 - self.image  # Directly calculate negative without color conversion
        return self.convert_to_base64(negative)

    # Умножает значения пикселей на указанную константу, усиливая яркость.
    def multiply_by_constant(self, constant=2):
        """Multiply the image by a constant value to enhance brightness."""
        result = cv.multiply(self.image, (constant, constant, constant))  # Multiply each channel directly
        return self.convert_to_base64(result)

    # Возводит значения пикселей в квадрат, нормализует их и возвращает результат.
    def power_of_2(self):
        """Raise pixel values to the power of 2 for each color channel."""
        float_image = self.image.astype('float32')
        powered = cv.pow(float_image, 2)
        normalized = cv.normalize(powered, None, 0, 255, cv.NORM_MINMAX)  # Normalize to [0, 255]
        return self.convert_to_base64(normalized.astype('uint8'))  # Convert back to uint8


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and display the upload page."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request", 400

        file = request.files['file']

        if file.filename == '':
            return "No selected file", 400

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('process', file_name=file.filename))

    return render_template('upload.html')


@app.route('/process/<file_name>', methods=['GET', 'POST'])
def process(file_name):
    """Process the uploaded image and display the results."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    if not os.path.exists(file_path):
        return "File not found", 404

    processor = ImageProcessor(file_path)

    # Default processing method (could be updated after button selection)
    if request.method == 'POST':
        method = request.form['method']
        if method == 'global_threshold':
            processed_image = processor.global_threshold()
        elif method == 'adaptive_threshold':
            processed_image = processor.adaptive_threshold()
        elif method == 'negative':
            processed_image = processor.negative()
        elif method == 'linear_contrast':
            processed_image = processor.linear_contrast()
        elif method == 'multiply_by_constant':
            processed_image = processor.multiply_by_constant()
        elif method == 'power_of_2':
            processed_image = processor.power_of_2()
        else:
            processed_image = processor.original_image()

        return render_template('process.html', 
                               original_image=processor.original_image(),
                               processed_image=processed_image,
                               file_name=file_name)

    # Default display (no method selected)
    return render_template('process.html', 
                           original_image=processor.original_image(),
                           processed_image=None,
                           file_name=file_name)



if __name__ == '__main__':
    app.run(debug=True)
