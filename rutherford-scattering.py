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
ma = 1.661e-27  # 1 masa ataomowu
x0 = -const  # początek współrzędnej X
k = 1 / (4 * math.pi * 8.85e-12)
m = 4 * ma
q1 = 79 * q
q2 = 2 * q

def getYY(qa, qb, r1, r2, mass):
    return k * qa * qb / (math.sqrt(r1 ** 2 + r2 ** 2)) ** 2 / mass

@app.route('/')
def simulation_run():
    params = []
    for i in range(-5, 6, 1):
        if i != 0:
            params.append(i*1e-14)
    for i in range(-50, 51, 10):
        if i != 0:
            params.append(i*1e-14)
    for i in range(-500, 501, 100):
        if i != 0:
            params.append(i*1e-14)
    for y0 in params:
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
        while np.isfinite(y) and -const < x < const and -5*const < y < 5*const:
            X.append(x)
            Y.append(y)

            constAx = getYY(q1, q2, x, y, m) * x / math.sqrt(x ** 2 + y ** 2)
            constAy = getYY(q1, q2, x, y, m) * y / math.sqrt(x ** 2 + y ** 2)

            val1 = x
            x = h ** 2 * constAx + 2 * x - prev_x
            prev_x = val1

            val2 = y
            y = h ** 2 * constAy + 2 * y - prev_y
            prev_y = val2

            val3 = Vx
            Vx = prev_Vx + constAx * h
            prev_Vx = val3

            val4 = Vy
            Vy = prev_Vy + constAy * h
            prev_Vy = val4

        plt.title("Symulacja cząstek")
        plt.xlabel("X")
        plt.ylabel("Y")
        xy.xaxis.set_major_locator(ticker.MultipleLocator(const/10))
        xy.yaxis.set_major_locator(ticker.MultipleLocator(const/10))
        plt.grid(True)
        xy.plot(X, Y)
    xy.scatter(0, 0)
    plt.xlim(-const, const)
    plt.ylim(-const, const)
    plt.savefig('./static/new_plot.png')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug = True)
