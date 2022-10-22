import pyqrcode

def generate_qr(id):
    qr = pyqrcode.create(id)
    _name = 'static/qr/qr_img_' + str(id) + '.png'
    qr.png(_name, scale = 8)
    return _name