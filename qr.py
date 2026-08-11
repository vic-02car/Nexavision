import qrcode
from qrcode.image.pil import PilImage

url = "https://vic-02car.github.io/Nexavision/"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(
    image_factory=PilImage,
    fill_color="#00C853",
    back_color="#0A2540"
)

img.save("qrnexa.png")

print("QR creado correctamente")