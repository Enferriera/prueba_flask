from flask import Flask,request
import requests
import json

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Reemplaza con tu propia API Key de OpenWeatherMap
API_KEY = '0a0364eccaef3de72949258e2e897e1f'

# Definir una ruta para la página principal
@app.route('/')
def home():
    return '''
        <h1>Menú Interactivo de Clima</h1>
        <p>Seleccione una opción:</p>
        <ul>
            <li><a href="/consultar_clima">Consultar Clima Actual</a></li>
            <li><a href="/pronostico_clima">Consultar Pronóstico del Clima</a></li>

            <!-- Opciones futuras comentadas -->
            <!--<li><a href="/cambiar_unidades">Cambiar Unidades de Medida</a></li>-->
            <!--<li><a href="/historial_consultas">Ver Historial de Consultas</a></li>-->
            <!--<li><a href="/temporal_recorrido">Temporal del Recorrido</a></li>-->
            <!--<li><a href="/cambio_ciudad">Cambiar Ciudad Actual</a></li>-->
            <!--<li><a href="/notificaciones">Activar/Desactivar Notificaciones</a></li>-->
        </ul>
    '''



@app.route('/consultar_clima', methods=['GET', 'POST'])
def consultar_clima():
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"


        res = requests.get(url)
        data = res.json()

        if res.status_code == 200:
                        # Obtener la información requerida
            temp = data["main"]["temp"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            humedad = data["main"]["humidity"]
            vel_viento = data["wind"]["speed"]
            latitud = data["coord"]["lat"]
            longitud = data["coord"]["lon"]
            descripcion = data["weather"][0]["description"]

            return f'''
                <div style="border: 2px solid #87CEEB; border-radius: 10px; padding: 20px; width: 300px; margin: auto; background-color: #f9f9f9;">
                    <h2>Clima en {ciudad.capitalize()}</h2>
                    <p><strong>Temperatura:</strong> {temp} °C</p>
                    <p><strong>Temperatura Mínima:</strong> {temp_min} °C</p>
                    <p><strong>Temperatura Máxima:</strong> {temp_max} °C</p>
                    <p><strong>Humedad:</strong> {humedad}%</p>
                    <p><strong>Velocidad del Viento:</strong> {vel_viento} m/s</p>
                    <p><strong>Latitud:</strong> {latitud}</p>
                    <p><strong>Longitud:</strong> {longitud}</p>
                    <p><strong>Descripción:</strong> {descripcion}</p>
                </div>
                <a href="/">Volver al Menú</a>
            '''
        else:
            return f'''
                <h1>Error</h1>
                <p>No se pudo obtener el clima para la ciudad: {ciudad}. Verifica el nombre e inténtalo nuevamente.</p>
                <a href="/">Volver al Menú</a>
            '''

    return '''
        <h1>Consultar Clima</h1>
        <form method="post">
            <label for="ciudad">Ingrese una ciudad:</label>
            <input type="text" name="ciudad" required>
            <input type="submit" value="Consultar">
        </form>
        <a href="/">Volver al Menú</a>
    '''

@app.route('/pronostico_clima', methods=['GET', 'POST'])
def pronostico_clima():
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
       
        res = requests.get(url)
        data = res.json()

        if res.status_code == 200:
            pronosticos = {}
            for item in data['list']:
                fecha_hora = item['dt_txt']
                fecha = fecha_hora.split(" ")[0]  # Extraer solo la fecha
                temp = item['main']['temp']
                temp_min = item['main']['temp_min']
                temp_max = item['main']['temp_max']
                humedad = item['main']['humidity']
                vel_viento = item['wind']['speed']
                descripcion = item['weather'][0]['description']

                # Formatear la información del pronóstico
                detalle_clima = (
                    f"Hora: {fecha_hora.split(' ')[1]} - "
                    f"Temperatura: {temp} °C - "
                    f"Temperatura Mínima: {temp_min} °C - "
                    f"Temperatura Máxima: {temp_max} °C - "
                    f"Humedad: {humedad}% - "
                    f"Velocidad del Viento: {vel_viento} m/s - "
                    f"Descripción: {descripcion}"
                )

                if fecha not in pronosticos:
                    pronosticos[fecha] = []
                pronosticos[fecha].append(detalle_clima)

            # Generar la tabla HTML
            tabla_pronostico = "<table border='1' style='border-collapse: collapse; width: 100%; border-color: #87CEEB;'>"
            tabla_pronostico += "<tr><th>Fecha</th><th>Detalles del Clima</th></tr>"

            for fecha, detalles in pronosticos.items():
                tabla_pronostico += f"<tr><td>{fecha}</td><td><ul>"
                for detalle in detalles:
                    tabla_pronostico += f"<li>{detalle}</li>"
                tabla_pronostico += "</ul></td></tr>"

            tabla_pronostico += "</table>"

            return f'''
                <h1>Pronóstico del Clima en {ciudad.capitalize()}</h1>
                {tabla_pronostico}
                <a href="/">Volver al Menú</a>
            '''
        else:
            return f'''
                <h1>Error</h1>
                <p>No se pudo obtener el pronóstico para la ciudad: {ciudad}. Por favor, inténtalo de nuevo más tarde.</p>
                <a href="/">Volver al Menú</a>
            '''

    return '''
        <h1>Consultar Pronóstico del Clima</h1>
        <form method="post">
            <label for="ciudad">Ingrese una ciudad:</label>
            <input type="text" name="ciudad" required>
            <input type="submit" value="Consultar">
        </form>
        <a href="/">Volver al Menú</a>
    '''

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

