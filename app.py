from flask import Flask, render_template, request
import calendar
from datetime import datetime

app = Flask(__name__)

# Calcular días laborales
def calcular_dias_laborales(mes):
    ano = 2025
    dias_laborales = 0

    # Recorrer los días laborales del mes
    for dia in range(1, calendar.monthrange(ano, mes)[1] + 1):
        fecha = datetime(ano, mes, dia)

        if fecha.weekday() < 5:
            dias_laborales += 1
    return dias_laborales

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            mes = int(request.form['mes'])
            dias_restados = int(request.form['dias_restados'])

            if mes < 1 or mes > 12:
                raise ValueError("El mes debe estar entre 1 y 12")

            dias_laborales = calcular_dias_laborales(mes)
            dias_laborales_restados = dias_laborales - dias_restados
            if dias_laborales_restados < 0:
                raise ValueError("Los días laborales restados no pueden ser mayores que los días laborales totales.")

            porcentaje_dias = dias_laborales_restados * 0.40
            horas_laborales = dias_laborales_restados * 8
            porcentaje_horas = horas_laborales * 0.40

            return render_template('index.html', resultado=True, dias_laborales=dias_laborales,
                                   dias_laborales_restados=dias_laborales_restados,
                                   porcentaje_dias=porcentaje_dias, porcentaje_horas=porcentaje_horas)
        except ValueError as error:
            return render_template('index.html', error=str(error))

    return render_template('index.html', resultado=False)

if __name__ == '__main__':
    app.run(debug=True)
