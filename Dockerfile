# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos requeridos al contenedor
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto al contenedor
COPY . .

# Expone el puerto en el que correrá Flask (por defecto, 5000)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]