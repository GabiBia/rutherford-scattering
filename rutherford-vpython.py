from vpython import *

Alphas = [] # pusta lista na wygenerowane cząstki
dt = 0.1 # krok (1/dt - szybkość animacji)
k = 2e-5 # stała siły elektrycznej; kontroluje siłę interakcji


def particle_definition(charge,radius): # definicja atomu złota
    return sphere(pos=vector(0,0,0),color=color.yellow,charge=charge,radius=radius)

def simulation_run(Gold): # symulacja
    while (len(Alphas)<500): # animacja do momentu wystrzelenia ustalonej liczby cząstek alfa
        rate(1/dt) # szybkość animacji

        r = random() # losowy moment wystrzelenia cząstki alfa
        if (r < 0.1): # 10% szansa na strzał
            x = -1.0
            y = 2*random() - 1
            z = 2*random() - 1
            # Tworzenie cząsteczki alfa i dodawanie jej do listy.
            Alphas.append(simple_sphere(pos=vector(x,y,z),velocity=vector(0.1,0,0),charge=2,mass=4,radius=0.01,color=color.red,make_trail=True))

        for a in Alphas: # Iterowanie po cząstkach Alfa
            a.force = k*a.charge*Gold.charge/mag(a.pos)**2 * hat(a.pos)
            a.velocity += a.force/a.mass*dt
            a.pos += a.velocity*dt
            if (mag(a.pos) > sqrt(3)):
                a.velocity = vector(0,0,0)

def main(): # wywołanie gotowej symulacji
    Gold = particle_definition(79,0.1)
    simulation_run(Gold)

if __name__ == "__main__":
    main()
