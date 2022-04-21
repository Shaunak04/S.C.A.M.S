import pyqrcode
import cv2

def generate_qr(id):
    qr = pyqrcode.create(id)
    _name = 'templates\\qr\\qr_img_' + str(id) + '.png'
    image = cv2.imread('././'+_name)
    imageString = image.tostring()
    print(imageString)
    file_png = qr.png(_name, scale = 8)
    return _name, file_png