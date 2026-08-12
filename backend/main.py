from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import cv2
import numpy as np

from pathlib import Path

import hashlib


app = FastAPI()


# ===================================
# CORS
# ===================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://vic-02car.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================
# CARPETA DE ROSTROS
# ===================================

CARPETA_ROSTROS = Path("rostros")

CARPETA_ROSTROS.mkdir(
    exist_ok=True
)


# ===================================
# DETECTOR OPENCV
# ===================================

detector = cv2.CascadeClassifier(

    cv2.data.haarcascades +

    "haarcascade_frontalface_default.xml"

)


# ===================================
# REGISTRO
# ===================================

@app.post("/registro")
async def registrar(

    nombre: str = Form(...),

    apellido: str = Form(...),

    correo: str = Form(...),

    telefono: str = Form(...),

    clave: str = Form(...),

    foto: UploadFile = File(...)

):


    # ===============================
    # LEER IMAGEN
    # ===============================

    contenido = await foto.read()


    array_imagen = np.frombuffer(
        contenido,
        dtype=np.uint8
    )


    imagen = cv2.imdecode(
        array_imagen,
        cv2.IMREAD_COLOR
    )


    if imagen is None:

        raise HTTPException(

            status_code=400,

            detail="La fotografía recibida no es válida."

        )


    # ===============================
    # CONVERTIR A GRIS
    # ===============================

    gris = cv2.cvtColor(

        imagen,

        cv2.COLOR_BGR2GRAY

    )


    # ===============================
    # DETECTAR ROSTROS
    # ===============================

    rostros = detector.detectMultiScale(

        gris,

        scaleFactor=1.1,

        minNeighbors=6,

        minSize=(100, 100)

    )


    if len(rostros) == 0:

        raise HTTPException(

            status_code=400,

            detail="No se detectó ningún rostro."

        )


    if len(rostros) > 1:

        raise HTTPException(

            status_code=400,

            detail="Debe aparecer solamente una persona en la fotografía."

        )


    # ===============================
    # RECORTAR ROSTRO
    # ===============================

    x, y, w, h = rostros[0]


    rostro = imagen[
        y:y+h,
        x:x+w
    ]


    # Normalizamos tamaño

    rostro = cv2.resize(

        rostro,

        (300, 300)

    )


    # ===============================
    # IDENTIFICADOR
    # ===============================

    identificador = hashlib.sha256(

        correo.encode()

    ).hexdigest()[:16]


    ruta = (
        CARPETA_ROSTROS /
        f"{identificador}.jpg"
    )


    # ===============================
    # GUARDAR ROSTRO
    # ===============================

    cv2.imwrite(

        str(ruta),

        rostro

    )


    # Aquí posteriormente insertaremos
    # nombre, correo, teléfono, contraseña
    # y ruta de rostro en MySQL.


    return {

        "ok": True,

        "mensaje": "Usuario y rostro registrados correctamente.",

        "usuario": {

            "nombre": nombre,

            "apellido": apellido,

            "correo": correo,

            "telefono": telefono

        }

    }