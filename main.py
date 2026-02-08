import os
import pdfplumber
import re
from datetime import datetime
import pandas as pd

# -------------------------------
# Función para leer un voucher individual
def leer_voucher(ruta_pdf):
    with pdfplumber.open(ruta_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"

    texto_upper = texto.upper()

    # -------------------------------
    # Monto en soles (solo el número)
    monto_match = re.search(r"TOTAL:\s*S/\s*(\d+(?:\.\d{2})?)", texto_upper)
    monto = float(monto_match.group(1)) if monto_match else None

    # -------------------------------
    # Tipo de operación
    tipo = None
    if "VISA CREDIT" in texto_upper:
        tipo = "Crédito"
    elif "VISA DEBIT" in texto_upper:
        tipo = "Débito"
    elif "YAPE" in texto_upper:
        tipo = "Yape"
    elif "PLIN" in texto_upper:
        tipo = "Plin"

    # -------------------------------
    # Fecha y hora
    fecha, hora = None, None
    dt = None  # datetime final

    if "BILLETERA" in texto_upper:
        billetera_match = re.search(r"(\d{2}[A-Z]{3}\d{2})\s+(\d{2}:\d{2})", texto_upper)
        if billetera_match:
            fecha_str, hora_str = billetera_match.groups()
            try:
                dt = datetime.strptime(fecha_str + " " + hora_str, "%d%b%y %H:%M")
                fecha = dt.strftime("%Y-%m-%d")
                hora = dt.strftime("%H:%M")
            except ValueError:
                fecha, hora = fecha_str, hora_str
    else:
        normal_match = re.search(r"FECHA:(\d{2}/\d{2}/\d{2})\s+HORA:(\d{2}:\d{2})", texto_upper)
        if normal_match:
            fecha_str, hora_str = normal_match.groups()
            try:
                dt = datetime.strptime(fecha_str + " " + hora_str, "%d/%m/%y %H:%M")
                fecha = dt.strftime("%Y-%m-%d")
                hora = dt.strftime("%H:%M")
            except ValueError:
                fecha, hora = fecha_str, hora_str

    # -------------------------------
    return {
        "archivo": os.path.basename(ruta_pdf),
        "monto": monto,
        "tipo": tipo,
        "fecha": fecha,
        "hora": hora,
        "datetime": dt
    }

# -------------------------------
# Carpeta donde están los PDFs
carpeta = "vouchers"

# Lista para guardar los datos de todos los vouchers
datos = []

for archivo in os.listdir(carpeta):
    if archivo.lower().endswith(".pdf"):
        ruta = os.path.join(carpeta, archivo)
        info = leer_voucher(ruta)
        datos.append(info)

# -------------------------------
# Crear DataFrame
df = pd.DataFrame(datos)

# Mostrar resultado
print(df)

# Opcional: guardar a CSV
df.to_csv("vouchers.csv", index=False)
