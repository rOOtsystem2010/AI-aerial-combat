import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class Fighter:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.score = 0
        self.hit = False
        self.hit_location = None

    def move(self):
        self.x += random.uniform(-1, 1)
        self.y += random.uniform(-1, 1)

    def shoot(self, opponent):
        distance_squared = (self.x - opponent.x) ** 2 + (self.y - opponent.y) ** 2
        probability = 1 / (1 + distance_squared)
        if random.random() < probability:
            self.score += 1
            self.hit = True
            self.hit_location = (self.x, self.y)
        else:
            self.hit = False
            self.hit_location = None

    def plot_fighter(self, ax):
        ax.plot([self.x - 0.5, self.x + 0.5, self.x + 0.5, self.x - 0.5, self.x - 0.5],
                [self.y - 0.5, self.y - 0.5, self.y + 0.5, self.y + 0.5, self.y - 0.5],
                label=self.name)

        if self.hit:
            ax.text(self.hit_location[0], self.hit_location[1], '■', ha='center', va='center', color='red', fontsize=20)
            ax.text(self.hit_location[0], self.hit_location[1] - 1, "HIT", ha='center', va='center', color='red')


def update_visuals(ax, human_pilot, ai_pilot):
    ax.clear()
    human_pilot.plot_fighter(ax)
    ai_pilot.plot_fighter(ax)


def simulate_aerial_combat():
    human_pilot = Fighter("الطيار البشري", 0, 0)
    ai_pilot = Fighter("الطيار الذكاء الاصطناعي", 5, 5)

    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    winner = None

    try:
        for i in range(50):
            human_pilot.move()
            ai_pilot.move()

            human_pilot.shoot(ai_pilot)
            ai_pilot.shoot(human_pilot)

            update_visuals(ax, human_pilot, ai_pilot)

            canvas.draw()
            canvas.flush_events()

            root.update()
            root.after(100)

            if human_pilot.hit or ai_pilot.hit:
                winner = human_pilot if human_pilot.hit else ai_pilot
                break

    except KeyboardInterrupt:
        pass

    if winner:
        winner_text = "الفائز هو: {}".format(winner.name)
        hit_location_text = "إحداثيات الاصابة: ({}, {})".format(winner.hit_location[0], winner.hit_location[1])
        if winner.hit:
            distance = ((human_pilot.x - ai_pilot.x) ** 2 + (human_pilot.y - ai_pilot.y) ** 2) ** 0.5
            distance_text = "المسافة عن الاصابة: {:.2f}".format(distance)
        else:
            distance_text = ""
    else:
        winner_text = "لا يوجد فائز"
        hit_location_text = ""
        distance_text = ""

    winner_label.config(text=winner_text)
    hit_location_label.config(text=hit_location_text)
    distance_label.config(text=distance_text)


def restart_simulation():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("محاكاة القتال الجوي")


root = tk.Tk()
root.title("محاكاة القتال الجوي")

winner_label = tk.Label(root, text="")
winner_label.pack()

hit_location_label = tk.Label(root, text="")
hit_location_label.pack()

distance_label = tk.Label(root, text="")
distance_label.pack()

simulate_button = tk.Button(root, text="بدء المحاكاة", command=simulate_aerial_combat)
simulate_button.pack()

restart_button = tk.Button(root, text="إعادة التشغيل", command=restart_simulation)
restart_button.pack()

root.mainloop()
