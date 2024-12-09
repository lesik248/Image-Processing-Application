
# Image Processing Flask App

This is a Flask-based web application that allows users to upload an image and apply various image processing techniques. The application supports multiple operations like global thresholding, adaptive thresholding, contrast enhancement, and more. It processes images using the OpenCV library and displays the results dynamically.

## Features

- **Upload an image**: Upload images in various formats (PNG, JPG, JPEG, GIF, TIF, BMP, PCX).
- **Image Processing**: Apply different image processing techniques to the uploaded image:
  - Global Thresholding
  - Adaptive Thresholding
  - Linear Contrast Enhancement
  - Negative Image
  - Brightness Enhancement (Multiply by constant)
  - Power of 2 enhancement
- **Display processed images**: View the original image and the processed results.

## Requirements

Before running the application, ensure that you have the following installed:

- Python 3.x
- Flask
- OpenCV
- Other dependencies:
  - `opencv-python`
  - `numpy`

## How to Use

1. **Start the application**:
    - Clone the repository to your local machine.
    - Navigate to the project directory and run the app using the following command:

    ```bash
    python app.py
    ```

2. **Upload an image**:
    - Open the app in your browser (default address: `http://127.0.0.1:5000/`).
    - Click the "Choose File" button to upload an image from your computer.
  
3. **Process the image**:
    - After the image is uploaded, you will be redirected to a page where you can choose an image processing method:
      - **Global Thresholding**
      - **Adaptive Thresholding**
      - **Linear Contrast**
      - **Negative**
      - **Multiply by Constant**
      - **Power of 2**
    - The processed image will be displayed below the original image.

## Directory Structure

- **app.py**: The main Flask application file.
- **templates/**: Contains the HTML templates for the application.
  - `upload.html`: The page where users can upload images.
  - `process.html`: The page to view and select processing methods for the uploaded image.
- **static/**: Contains static files like CSS and JavaScript for the application.

## File Formats Supported

- PNG
- JPG
- JPEG
- GIF
- TIF
- BMP
- PCX


