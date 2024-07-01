from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta principal que muestra el formulario de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el formulario y calcular los precios
@app.route('/calcular', methods=['POST'])
def calcular():
    valor = float(request.form['valor_carga_cafe'])
    precio_kilo_alimentacion = float(request.form['precio_kilo_alimentacion'])
    precio_kilo_no_alimentacion = float(request.form['precio_kilo_no_alimentacion'])

    cafe_seco = float(request.form['cafe_seco'])
    cafe_verde = float(request.form['cafe_verde'])
    cafe_colorado = float(request.form['cafe_colorado'])

    porcentaje_seco = cafe_seco
    porcentaje_verde = cafe_verde * 0.92
    porcentaje_colorado = cafe_colorado * 0.35
    porcentaje_colorado_seco = porcentaje_colorado * 0.60

    valor_seco = valor / 125
    valor_verde = valor / 250
    valor_colorado = valor / 250

    Precio_seco = valor_seco * porcentaje_seco
    Precio_verde = valor_verde * porcentaje_verde
    Precio_colorado = valor_colorado * porcentaje_colorado
    Precio_total = Precio_seco + Precio_verde + Precio_colorado

    return render_template('resultado.html', Precio_seco=Precio_seco,
                           Precio_verde=Precio_verde,
                           Precio_colorado=Precio_colorado,
                           porcentaje_seco=porcentaje_seco,
                           porcentaje_verde=porcentaje_verde,
                           porcentaje_colorado=porcentaje_colorado,
                           porcentaje_colorado_seco=porcentaje_colorado_seco,
                           valor_seco=valor_seco,
                           valor_verde=valor_verde,
                           valor_colorado=valor_colorado,
                           Precio_total=Precio_total)

# Inicializar recolectores con al menos cinco registros por defecto
recolectores = [{'nombre': '', 'apellido': '', 'cantidad_recolectada': 0.0} for _ in range(5)]

# Ruta para mostrar la tabla de recolectores
@app.route('/tabla_recolectores')
def tabla_recolectores():
    return render_template('tabla_recolectores.html', recolectores=recolectores)

# Ruta para guardar los recolectores desde el formulario
@app.route('/guardar_recolectores', methods=['POST'])
def guardar_recolectores():
    global recolectores
    nombres = request.form.getlist('nombre[]')
    apellidos = request.form.getlist('apellido[]')
    cantidades_recolectadas = request.form.getlist('cantidad_recolectada[]')
    precio_alimentacion = float(request.form['precio_alimentacion'])
    precio_no_alimentacion = float(request.form['precio_no_alimentacion'])

    recolectores_temp = []
    recolector_counts = {}

    for i in range(len(nombres)):
        nombre = nombres[i].strip().lower()
        apellido = apellidos[i].strip().lower()
        cantidad_recolectada = float(cantidades_recolectadas[i]) if cantidades_recolectadas[i] else 0.0

        key = f"{nombre} {apellido}"
        if key in recolector_counts:
            recolector_counts[key] += 1
        else:
            recolector_counts[key] = 1

        if recolector_counts[key] > 5:
            error_message = f"No puede {nombres[i]} {apellidos[i]} tener más de cinco casillas. Por favor, utilizar solo 5 casillas por recolector."
            return render_template('tabla_recolectores.html', recolectores=recolectores, error_message=error_message)

        total_alimentacion = cantidad_recolectada * precio_alimentacion
        total_no_alimentacion = cantidad_recolectada * precio_no_alimentacion
        recolector = {
            'nombre': nombres[i],
            'apellido': apellidos[i],
            'cantidad_recolectada': cantidad_recolectada,
            'total_alimentacion': total_alimentacion,
            'total_no_alimentacion': total_no_alimentacion
        }
        recolectores_temp.append(recolector)

    recolectores = recolectores_temp
    return redirect(url_for('tabla_recolectores'))

# Ruta para borrar todos los registros de recolectores
@app.route('/borrar_registros', methods=['POST'])
def borrar_registros():
    global recolectores
    # Mantener las primeras cinco casillas en blanco
    recolectores = recolectores[:5]
    for recolector in recolectores:
        recolector['nombre'] = ''
        recolector['apellido'] = ''
        recolector['cantidad_recolectada'] = 0.0
        recolector['total_alimentacion'] = 0.0
        recolector['total_no_alimentacion'] = 0.0
    return redirect(url_for('ver_registros'))

# Ruta para agregar una casilla adicional de recolector
@app.route('/agregar_casilla', methods=['POST'])
def agregar_casilla():
    global recolectores
    recolectores.append({'nombre': '', 'apellido': '', 'cantidad_recolectada': 0.0})
    return redirect(url_for('tabla_recolectores'))

# Ruta para eliminar la última casilla de recolector
@app.route('/eliminar_casilla', methods=['POST'])
def eliminar_casilla():
    global recolectores
    if len(recolectores) > 5:
        recolectores.pop()
    return redirect(url_for('tabla_recolectores'))

# Ruta para ver los registros guardados de los recolectores
@app.route('/ver_registros')
def ver_registros():
    global recolectores

    # Agrupar recolectores por nombre y apellido
    recolectores_agrupados = {}
    for recolector in recolectores:
        key = f"{recolector['nombre']} {recolector['apellido']}"
        if key not in recolectores_agrupados:
            recolectores_agrupados[key] = []
        recolectores_agrupados[key].append(recolector)

    # Calcular los totales
    total_alimentacion = sum(r['total_alimentacion'] for r in recolectores)
    total_no_alimentacion = sum(r['total_no_alimentacion'] for r in recolectores)

    return render_template('registros_guardados.html', 
                           recolectores_agrupados=recolectores_agrupados, 
                           total_alimentacion=total_alimentacion, 
                           total_no_alimentacion=total_no_alimentacion)

# Ejecutar la aplicación Flask si se ejecuta como script principal
app.run(debug=True)





