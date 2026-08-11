import qrcode
input='import qrcode'
input='https://vic-02car.github.io/Nexavision/' #esto es lo que se guardara en el QRCode
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(input)
qr.make(fit=True)
img=qr.make_image(fill='Black',back_color='white') # señalamos que el relleno sea negro 
#y el fondo blanco
img.save('qrnexa.png') #se genera este archivo QRCode