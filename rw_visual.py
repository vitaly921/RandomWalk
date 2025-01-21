import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk
import matplotlib.animation as animation

import random_walk
from random_walk import RandomWalk

# Задание бесконечного цикла
#while True:
def build_graphs():
    """"""
    if mode_var.get() == 'static':
        build_static_graph()
    else:
        build_animation()


def build_static_graph():
    """"""
    plt.close('all')
    # Создание экземпляра с регулируемой длин ой списка координат точек
    rw = RandomWalk(5000)
    # Заполнение списка координатами
    rw.fill_walk()
    # Сохранение списка длиной кол-ва точек
    point_numbers = list(range(rw.num_points))

    if points_var.get():
        # Задание размера окна графика точек
        plt.figure(figsize=(9, 5))
        # Создание точечной диаграммы с вычисленными точками для X,Y
        plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Greys, edgecolors='none', s=20)
        # Отрисовка увеличенных начальной и конечной точек блуждания
        plt.scatter(0, 0, c='green', edgecolors='none', s=100)
        plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100)
        plt.plot([0, rw.x_values[-1]], [0, rw.y_values[-1]], c='red', linestyle='--', linewidth=3,
             label='Line between points')
        #plt.show()

    if line_var.get():
        # Задание размера окна графика линии блуждания
        plt.figure(figsize=(9, 5))
        # Создание линейной диаграммы с вычисленными точками для X, Y
        plt.plot(rw.x_values, rw.y_values, c='gray', linewidth = 1, zorder =1)
        # Отрисовка увеличенных начальной и конечной точек блуждания
        plt.scatter(0, 0, c='green', edgecolors='none', s=100, zorder =2)
        plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100, zorder =2)
        plt.plot([0, rw.x_values[-1]], [0, rw.y_values[-1]], c='red', linestyle='--', linewidth=3,
                 label='Line between points')

        distance = math.sqrt((rw.x_values[-1]-rw.x_values[0])**2 + (rw.y_values[-1]-rw.y_values[0])**2)
        print(distance)
        plt.text(0.5, -0.1, f'Расстояние между точками блуждания: {distance:.2f}', fontsize=12, ha='center',
                 va='center', transform=plt.gca().transAxes)

    # Удаление осей X,Y
    #plt.axes().get_xaxis().set_visible(False)
    #plt.axes().get_yaxis().set_visible(False)

    # Отображение графиков
    plt.show()

    ## Ожидание ответа от пользователя на отрисовку следующего графика
    #keep_running = input("Make another walk? (y/n): ")
    ## Проверка условия продолжения работы программы и выхода из цикла
    #if keep_running == 'n':
    #    break


def build_animation():
    """"""
    plt.close('all')
    rw = RandomWalk(5000)
    rw.fill_walk()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
    ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)

    if line_var.get():
        point, = ax.plot(rw.x_values[0], rw.y_values[0], 'bo')
        line, = ax.plot([],[], 'b-')
    if points_var.get():
        points, = ax.plot([], [], 'ro', markersize=1)

    def init():
        """"""
        if line_var.get():
            point.set_data([],[])
            line.set_data([],[])
        if points_var.get():
            points.set_data([],[])
        return (point, line, points) if line_var.get() and points_var.get() else (line,) if line_var.get() else (points,)

    def update(frame):
        """"""
        if line_var.get():
            point.set_data(rw.x_values[frame], rw.y_values[frame])
            line.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
        if points_var.get():
            points.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
        return (point, line, points) if line_var.get() and points_var.get() else (line,) if line_var.get() else (points,)

    ani = animation.FuncAnimation(fig, update, frames = len(rw.x_values), init_func=init, blit=True, interval=0)
    plt.title('Animation random walk')
    plt.show()

def update_button_state():
    """"""
    if line_var.get() or points_var.get():
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Случайное блуждание")
root.geometry("400x450+100+100")
root.resizable(False, False)

line_var = tk.BooleanVar(value=True)
points_var = tk.BooleanVar(value=True)

line_check = ttk.Checkbutton(root, text='Graphic line', variable= line_var, command=update_button_state)
line_check.pack(pady=5)
points_check = ttk.Checkbutton(root, text='Graphic points', variable=points_var, command=update_button_state)
points_check.pack(pady=10)

mode_var = tk.StringVar(value='static')
#
static_radio = ttk.Radiobutton(root, text="Static", variable=mode_var, value='static')
static_radio.pack(pady=5)

animation_radio = ttk.Radiobutton(root, text='Animation', variable=mode_var, value='animation')
animation_radio.pack(pady=5)

button = ttk.Button(root, text = "Create New", command=build_graphs, state=tk.NORMAL)
button.pack(side='bottom', pady=10)


root.mainloop()

