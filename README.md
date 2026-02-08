# Voucher Reader IZIPAY

Este proyecto permite **leer vouchers de Izipay** en formato PDF y extraer información clave de manera automática.

Actualmente soporta:

- **Visa Crédito**
- **Visa Débito**
- **Billeteras digitales**:
  - Yape
  - Plin

El script extrae:

- Monto (en soles)  
- Tipo de operación (Crédito, Débito, Yape, Plin)  
- Fecha y hora del voucher  
- Genera un DataFrame con toda la información de **todos los PDFs en una carpeta**  

---

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/TU-USUARIO/voucher-reader.git
cd voucher-reader
