from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)

def colorize_and_style_transfer(grayscale_image_path, style):
    # Load grayscale image
    gray_img = cv2.imread(grayscale_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Simple colorization simulation (using OpenCV)
    colorized_image = cv2.merge([gray_img, np.zeros(gray_img.shape, dtype='uint8'), np.zeros(gray_img.shape, dtype='uint8')])
    
    # Apply style transfer (using a simple blend as a placeholder)
    style_image = cv2.imread(f'styles/{style}.jpg')
    style_image = cv2.resize(style_image, (colorized_image.shape[1], colorized_image.shape[0]))

    # Blend colorized image with style
    styled_image = cv2.addWeighted(colorized_image, 0.7, style_image, 0.3, 0)
    
    return styled_image

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['image']
    style = request.form['style']
    
    # Save the uploaded image
    file_path = 'uploaded_image.jpg'
    file.save(file_path)
    
    # Colorize and apply style
    result_image = colorize_and_style_transfer(file_path, style)
    
    # Save result
    result_path = 'result_image.jpg'
    cv2.imwrite(result_path, result_image)

    return send_file(result_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
