import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template
app = Flask(__name__)

plt.style.use('seaborn-whitegrid')
fig, xy = plt.subplots()

#Dane wejściowe
const = 1e-12
h = 1.0e-24  # krok
Vx0 = 1.0e7  # prędkość cząstki uciekającej z punktu O wzdłuż osi OX
Vy0 = 0  # prędkość cząstki uciekającej z punktu O wzdłuż osi OY
q = 1.6e-19  # ładunek izotopowy
ma = 1.661e-27  # masa atomowa (1 unit)
x0 = -const  # początek współrzędnej X
k = 1 / (4 * math.pi * 8.85e-12) # stała elektrostatyczna
m = 4 * ma # masa cząsteczkowa helu
q1 = 79 * q # ładunek jądra złota
q2 = 2 * q # ładunek jądra helu

def getYY(qa, qb, r1, r2, mass): # obliczanie siły Coulomba
    return k * qa * qb / (math.sqrt(r1 ** 2 + r2 ** 2)) ** 2 / mass

@app.route('/') # dekorator Flask
def simulation_run():
    params = [] # pusta lista na wygenerowanie trajektorii cząsteczek helu
    for i in range(-5, 6, 1): # określanie zakresu pojawiania się trajektorii cząsteczek na osiach
        if i != 0:
            params.append(i*1e-14)
    for i in range(-50, 51, 10):
        if i != 0:
            params.append(i*1e-14)
    for i in range(-500, 501, 100):
        if i != 0:
            params.append(i*1e-14)

    for y0 in params: # obliczanie przebiegu trajektorii cząsteczek
        X = [x0]
        Y = [y0]
        x = x0 + h * Vx0 + h ** 2 / 2 * getYY(q1, q2, x0, y0, m) * x0 / math.sqrt(x0 ** 2 + y0 ** 2)
        y = y0 + h * Vy0 + h ** 2 / 2 * getYY(q1, q2, y0, y0, m) * y0 / math.sqrt(x0 ** 2 + y0 ** 2)

        Vx = Vx0 + getYY(q1, q2, x, y, m) * x / math.sqrt(x ** 2 + y ** 2) * h
        Vy = Vy0 + getYY(q1, q2, x, y, m) * y / math.sqrt(x ** 2 + y ** 2) * h

        prev_Vx = Vx0
        prev_Vy = Vy0

        prev_x = x0
        prev_y = y0

        while np.isfinite(y) and -const < x < const and -5*const < y < 5*const: # wyświetlanie obliczonych  trajektorii
            X.append(x)
            Y.append(y)

            constAx = getYY(q1, q2, x, y, m) * x / math.sqrt(x ** 2 + y ** 2)
            constAy = getYY(q1, q2, x, y, m) * y / math.sqrt(x ** 2 + y ** 2)

            # położenia na osi
            val1 = x
            x = h ** 2 * constAx + 2 * x - prev_x
            prev_x = val1

            val2 = y
            y = h ** 2 * constAy + 2 * y - prev_y
            prev_y = val2

            # prędkości cząstek poruszających wzdłuż osi
            val3 = Vx
            Vx = prev_Vx + constAx * h
            prev_Vx = val3

            val4 = Vy
            Vy = prev_Vy + constAy * h
            prev_Vy = val4

        plt.title("Symulacja cząstek") # tytuł symulacji, wyświetlany na górze wykresu
        plt.xlabel("X") # nazwa osi x
        plt.ylabel("Y") # nazwa osi y
        xy.xaxis.set_major_locator(ticker.MultipleLocator(const/10)) # generowanie punktów na osi x co 0.1
        xy.yaxis.set_major_locator(ticker.MultipleLocator(const/10)) # generowanie punktów na osi y co 0.1
        plt.grid(True) # wyświetlanie siatki
        xy.plot(X, Y) # wyświetlanie trajektorii cząsteczek helu

    xy.scatter(0, 0) # wyświetlanie atomu złota
    plt.xlim(-const, const) # skala osi x
    plt.ylim(-const, const) # skala osi y
    plt.savefig('./static/new_plot.png') # zapisywanie grafiki symulacji do pliku .png

    return render_template('index.html') # plik html wyświetlany wraz z symulacją dzięki Flask

if __name__ == "__main__":
    app.run(debug = True)
