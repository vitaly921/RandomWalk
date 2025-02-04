import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk, SOLID
import matplotlib.animation as animation

import random_walk
from random_walk import RandomWalk


def build_graphs():
    """Функция для выбора способа отображения линейных и точечных графиков для дальнейшего построения"""
    # По умолчанию выбран статический способ отображения
    if mode_var.get() == 'static':
        build_static_graph()
    # Иначе выбирается анимированный способ отображения
    else:
        build_animation()


def build_static_graph():
    """Функция построения графиков в виде статического изображения"""
    # Закрытие всех активных окон
    plt.close('all')
    # Сохранение в виде целого числа кол-ва точек от пользователя
    count_points = int(count_points_entry.get())
    # Сохранение в виде целого числа максимальной длины шага от пользователя
    max_step = int(max_step_entry.get())

    # Создание экземпляра с регулируемой длиной списка координат точек
    rw = RandomWalk(count_points, max_step)
    # Заполнение списка координатами
    rw.fill_walk()

    # Создание списка длиной количества точек
    point_numbers = list(range(rw.num_points))
    # Определение расстояния между первой и последней точками
    distance = math.sqrt((rw.x_values[-1] - rw.x_values[0]) ** 2 + (rw.y_values[-1] - rw.y_values[0]) ** 2)

    # Если выбран точечный график
    if points_var.get():
        # Задание размера окна графика точек блуждания
        plt.figure(figsize=(9, 5))
        # Создание точечной диаграммы с вычисленными точками для X,Y
        plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Greys, edgecolors='none', s=20)

        # Отрисовка увеличенных начальной и конечной точек блуждания
        plt.scatter(0, 0, c='green', edgecolors='none', s=100)
        plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100)
        # Отрисовка линии между начальной и конечной точками
        plt.plot([0, rw.x_values[-1]], [0, rw.y_values[-1]], c='red', linestyle='--', linewidth=3,
             label='Line between points')
        # Отрисовка информации о расстоянии между начальной и конечной точками
        plt.text(0.5, -0.1, f'Расстояние между точками блуждания: {distance:.2f}', fontsize=12, ha='center',
                 va='center', transform=plt.gca().transAxes)

    # Если выбран линейный график
    if line_var.get():
        # Задание размера окна графика линии блуждания
        plt.figure(figsize=(9, 5))
        # Создание линейной диаграммы с вычисленными точками для X, Y
        plt.plot(rw.x_values, rw.y_values, c='gray', linewidth = 1, zorder =1)

        # Отрисовка увеличенных начальной и конечной точек блуждания
        plt.scatter(0, 0, c='green', edgecolors='none', s=100, zorder =2)
        plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100, zorder =2)
        # Отрисовка линии между начальной и конечной точками
        plt.plot([0, rw.x_values[-1]], [0, rw.y_values[-1]], c='red', linestyle='--', linewidth=3,
                 label='Line between points')
        # Отрисовка информации о расстоянии между начальной и конечной точками
        plt.text(0.5, -0.1, f'Расстояние между точками блуждания: {distance:.2f}', fontsize=12, ha='center',
                 va='center', transform=plt.gca().transAxes)

    # Отображение графиков независимо от выбора
    plt.show()

    # Удаление осей X,Y
    #plt.axes().get_xaxis().set_visible(False)
    #plt.axes().get_yaxis().set_visible(False)


def build_animation():
    """Функция построения графиков в виде анимации"""
    # Закрытие всех активных окон
    plt.close('all')
    # Сохранение в виде целого числа кол-ва точек от пользователя
    count_points = int(count_points_entry.get())
    # Сохранение в виде целого числа максимальной длины шага от пользователя
    max_step = int(max_step_entry.get())
    # Создание экземпляра с регулируемой длиной списка координат точек
    rw = RandomWalk(count_points, max_step)
    # Заполнение списка координатами
    rw.fill_walk()

    # Если выбрана анимация линий
    if line_var.get():
        # Создание окна графика и осей
        fig, ax = plt.subplots(figsize=(8, 6))
        # Установка границ осей
        ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)
        # Создание начальной точки и линии
        point, = ax.plot(rw.x_values[0], rw.y_values[0], 'ro')
        line, = ax.plot([], [], 'b-')

        def init_line():
            """Функция инициализации"""
            # Установка пустых кадров для линий и точки
            line.set_data([],[])
            point.set_data([], [])
            # Возврат кортежей с объектами линий и точки
            return line, point,

        def update_line(frame):
            """Функция обновления"""
            # Обновление вида линии от начала и до текущего кадра
            line.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
            # Обновление вида точки на текущем кадре
            point.set_data(rw.x_values[frame], rw.y_values[frame])
            # Возврат кортежей с объектами линий и точки
            return line, point,

        # Управление анимацией
        animation_line = animation.FuncAnimation(fig, update_line, frames=len(rw.x_values), init_func=init_line, blit=
                                                 True, interval=0)
        # Установка заголовка для окна с анимацией
        plt.title("Анимация линий")

    # Если выбрана анимация точек
    if points_var.get():
        # Создание окна графика и осей
        fig, ax = plt.subplots(figsize=(8, 6))
        # Установка границ осей
        ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)
        # Создание начальной точки
        points, = ax.plot([], [], 'ro', markersize=1)

        def init_points():
            """Функция инициализации"""
            # Установка пустых кадров для точек
            points.set_data([],[])
            return points,

        def update_points(frame):
            """Функция обновления"""
            # Обновление вида точек от начала и до текущего кадра
            points.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
            return points,
        # Управление анимацией
        animation_points = animation.FuncAnimation(fig, update_points, frames = len(rw.x_values),
                                                   init_func=init_points, blit=True, interval=0)
        # Установка заголовка для окна с анимацией
        plt.title('Анимация точек')

    # Отображение выбранных окон
    plt.show()


def update_button_state(event="<Key>"):
    """"""
    # Проверяем, выбран ли хотя бы один чекбокс
    checkbox_selected = line_var.get() or points_var.get()
    try:
        count_points = int(count_points_entry.get())
        entry_valid = count_points > 0
    except ValueError:
        entry_valid = False

    if checkbox_selected and entry_valid:
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)


def update_settings():
    """"""
    for key in frames:
        frames[key].pack_forget()
        labels[key].pack_forget()

    is_static = (mode_var.get()=="static")
    is_points = points_var.get()
    is_lines = line_var.get()

    # Определяем нужный ключ для выбора фрейма
    key = ('static' if is_static else 'animation')
    key += ('_points' if is_points else '') + ('_lines' if is_lines else '')

    if key in frames:
        print('Here')
        labels[key].pack(anchor="nw", pady=(10, 0))  # Показываем заголовок
        frames[key].pack(anchor="nw", fill="x", padx=5)  # Показываем фрейм


root = tk.Tk()
root.title("Случайное блуждание")
root.geometry("500x750+100+100")
root.resizable(False, False)

ttk.Label(root, text='Settings Random Walk', font=("Arial", 14)).pack(pady=2)

ttk.Label(root, text='Задание числовых данных', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

button = ttk.Button(root, text = "Create New", command=build_graphs, state=tk.DISABLED)
button.pack(side='bottom', pady=10)

ttk.Label(frame, text='Count points:').pack(side="left", padx=5)
count_points_entry = ttk.Entry(frame)
count_points_entry.pack(side="left", padx=5)


ttk.Label(frame, text='Max step:').pack(side="left", padx=5)
max_step_entry = ttk.Entry(frame)
max_step_entry.pack(anchor="nw")



ttk.Label(root, text='Вид графика', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)


line_var = tk.BooleanVar(value=True)
points_var = tk.BooleanVar(value=True)
line_var.trace_add("write", lambda *args: update_settings())
points_var.trace_add("write", lambda *args: update_settings())

line_check = ttk.Checkbutton(frame, text='Graphic line', variable= line_var, command=update_button_state)
line_check.pack(side="left", padx=5)
points_check = ttk.Checkbutton(frame, text='Graphic points', variable=points_var, command=update_button_state)
points_check.pack(side="left", padx=5)


ttk.Label(root, text='Способ отображения', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

mode_var = tk.StringVar(value='static')
mode_var.trace_add("write", lambda *args:update_settings())

#
static_radio = ttk.Radiobutton(frame, text="Static", variable=mode_var, value='static')
static_radio.pack(side="left", padx=5)

animation_radio = ttk.Radiobutton(frame, text='Animation', variable=mode_var, value='animation')
animation_radio.pack(side="left", padx=5)

count_points_entry.bind_all("<Key>", update_button_state)




# --- Создание фреймов и заголовков ---
frames = {}
labels = {}

def create_settings_frame(title, has_points=True, has_lines=True):
    """Функция создания динамических фреймов дополнительной настройки вида графиков"""

    label = ttk.Label(root, text=title, font=("Arial", 8))
    label.pack(pady=(10, 0))

    frame = ttk.Frame(root, borderwidth=1, relief=SOLID, padding=[8, 10])

    def toggle_colormap():
        """"""
        if colormap_var.get():
            colormap_combobox.config(state="readonly")
            color_combobox.config(state="disabled")
        else:
            colormap_combobox.config(state="disabled")
            color_combobox.config(state="normal")

    if has_points:

        colormap_var = tk.BooleanVar(value=False)
        colormap_check = ttk.Checkbutton(frame, text="Colormap", variable=colormap_var, command=toggle_colormap)
        colormap_check.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Выбор карты: ").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        colormap_combobox = ttk.Combobox(frame, values=['Jet', 'Blues', 'Viridis', 'Plasma'], state='disabled',
                                         width=10)
        colormap_combobox.grid(row=1, column=1, sticky="w")

        ttk.Label(frame, text="Цвет точек: ").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        color_combobox = ttk.Combobox(frame, values=['red', 'blue', 'black'], state="readonly", width=7)
        color_combobox.grid(row=1, column=3, sticky="w")

        ttk.Label(frame, text="Размер точек: ").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        #ttk.Entry(frame, width=10).grid(row=2, column=1, sticky="w")
        point_count = tk.Spinbox(frame, from_=1, to=20, width=10)
        point_count.grid(row=2, column=1, sticky="w")
        #point_count.set(1)









    if has_lines:
        ttk.Label(frame, text="Цвет линий: ").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(frame, width=10).grid(row=3, column=1, sticky="w")
        ttk.Label(frame, text="Ширина линий: ").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(frame, width=10).grid(row=4, column=1, sticky="w")

    return label, frame


# Добавляем все возможные комбинации в словари `frames` и `labels`
options = [
    ("static_points", "Настройки статических точек", True, False),
    ("static_lines", "Настройки статических линий", False, True),
    ("static_points_lines", "Настройки статических точек и линий", True, True),
    ("animation_points", "Настройки анимационных точек", True, False),
    ("animation_lines", "Настройки анимационных линий", False, True),
    ("animation_points_lines", "Настройки анимационных точек и линий", True, True),
]

for key, title, has_points, has_lines in options:
    labels[key], frames[key] = create_settings_frame(title, has_points, has_lines)

update_settings()

root.mainloop()

