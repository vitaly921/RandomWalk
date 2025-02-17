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
    """Функция построения линейных и точечных графиков в виде изображения"""
    # Закрытие всех активных окон
    plt.close('all')
    # Сохранение в виде целого числа кол-ва точек от пользователя
    count_points = int(count_points_entry.get())
    # Сохранение в виде целого числа максимальной длины шага от пользователя
    max_step = int(max_step_entry.get())
    # Объявление глобальной переменной размера точек
    global points_size_var

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
        # Задание размера окна для точечного графика
        plt.figure(figsize=(9, 5))

        # Получение пользовательского значения размера точек
        size_points = int(points_size_var.get())
        # --- Разделение на цветовую карту и обычный цвет и их выбор пользователем
        # Создание точечной диаграммы с вычисленными точками для X,Y
        plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Greys, edgecolors='none', s=size_points)

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
        # Задание размера окна для линейного графика
        plt.figure(figsize=(9, 5))
        # ---Получение пользовательского значения ширины линии
        # ---Получение пользовательского значения цвета линии
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
    global points_size_var

    # Переменная для хранения состояния чек-бокса повторения анимации
    repeat_animation = repeat_var.get()

    # Если выбрана анимация линий
    if line_var.get():
        # Создание окна графика и осей
        fig, ax = plt.subplots(figsize=(8, 6))
        # Установка границ осей
        ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)

        # Создание начальной точки и линии
        current_point_for_lines, = ax.plot(rw.x_values[0], rw.y_values[0], 'ro')
        line, = ax.plot([], [], 'b-')

        def init_line():
            """Функция инициализации"""
            # Установка пустых кадров для линий и точки
            line.set_data([],[])
            current_point_for_lines.set_data([], [])
            # Возврат кортежей с объектами линий и точки
            return line, current_point_for_lines,

        def update_line(frame):
            """Функция обновления"""
            # Обновление вида линии от начала и до текущего кадра
            line.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
            # Обновление вида точки на текущем кадре
            current_point_for_lines.set_data(rw.x_values[frame], rw.y_values[frame])
            # Возврат кортежей с объектами линий и точки
            return line, current_point_for_lines,

        # Управление анимацией
        animation_line = animation.FuncAnimation(fig, update_line, frames=len(rw.x_values), init_func=init_line, blit=
                                                 True, interval=0, repeat=repeat_animation)
        # Установка заголовка для окна с анимацией
        plt.title("Анимация линий")

    # Если выбрана анимация точек
    if points_var.get():
        size_points = int(points_size_var.get())
        # Создание окна графика и осей
        fig, ax = plt.subplots(figsize=(8, 6))
        # Установка границ осей
        ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)
        # Создание начальных точек
        #points, = ax.plot([], [], 'ro', markersize=(size_points**0.5))
        points = ax.scatter([], [], s=size_points, color='blue')
        current_point, = ax.plot(rw.x_values[0], rw.y_values[0], 'ro')

        def init_points():
            """Функция инициализации"""
            # Установка пустых кадров для точек
            points.set_offsets([])
            current_point.set_data([], [])
            return points, current_point,

        def update_points(frame):
            """Функция обновления"""
            # Обновление вида точек от начала и до текущего кадра
            points.set_offsets([[x, y] for x, y in zip(rw.x_values[:frame+1], rw.y_values[:frame+1])])
            # Обновление вида точки на текущем кадре
            current_point.set_data(rw.x_values[frame], rw.y_values[frame])
            return points, current_point,
        # Управление анимацией
        animation_points = animation.FuncAnimation(fig, update_points, frames = len(rw.x_values),
                                                   init_func=init_points, blit=True, interval=0, repeat=repeat_animation)
        # Установка заголовка для окна с анимацией
        plt.title('Анимация точек')

    # Отображение выбранных окон
    plt.show()


def validate_count_points(input_value):
    """Проверка ввода значений в поле count points окна настроек"""
    if input_value == "":  # Разрешаем пустое поле
        return True
    if input_value.isdigit():
        num = int(input_value)
        if 0 <= num <= 5000:
            return True
    return False


def validate_max_step(input_value):
    """Проверка ввода значений в поле max_step окна настроек"""
    if input_value == "":  # Разрешаем пустое поле
        return True
    if input_value.isdigit():
        num = int(input_value)
        if 0 <= num <= 30:
            return True
    return False


def update_button_state(event="<Key>"):
    """Функция для обновления состояния кнопки Create New (активно/неактивна) в зависимости от условий"""
    # Проверяем, выбран ли хотя бы один чекбокс
    checkbox_selected = line_var.get() or points_var.get()
    # Проверка на введенное число в строке Count points
    try:
        count_points = int(count_points_entry.get())
        entry_valid_count_points = 0 < count_points < 5001
    except ValueError:
        entry_valid_count_points = False

    # Проверка на введенное число в строке Max step
    try:
        max_step = int(max_step_entry.get())
        entry_valid_max_step = 0 < max_step < 31
    except ValueError:
        entry_valid_max_step = False
    # Если выбран хотя бы один чек-окс и введенное число в нужном диапазоне
    if checkbox_selected and entry_valid_count_points and entry_valid_max_step:
        # Кнопка для построения графиков активна
        button.config(state=tk.NORMAL)
    else:
        # Кнопка для построения графиков не активна
        button.config(state=tk.DISABLED)


def update_settings_frame():
    """Функция обновления фреймов с настройками в зависимости от выбора пользователя"""
    # Скрытие старых фреймов и заголовков по умолчанию
    for key in frames:
        frames[key].pack_forget()
        labels[key].pack_forget()

    # Создание флага состояния для кнопки Static (выбран ли пользователем этот RadioButton)
    is_static = (mode_var.get()=="static")
    # Создание флага состояния для чек-бокса Graphic points (выбран ли пользователем этот CheckButton)
    is_points = points_var.get()
    # Создание флага состояния для чек-бокса Graphic line (выбран ли пользователем этот CheckButton)
    is_lines = line_var.get()

    # Определяем нужный ключ для выбора вида динамического фрейма с дополнительными настройками
    key = ('static' if is_static else 'animation')
    key += ('_points' if is_points else '') + ('_lines' if is_lines else '')

    if key in frames:
        labels[key].pack(anchor="nw", pady=(10, 0))  # Показываем заголовок
        frames[key].pack(anchor="nw", fill="x", padx=5)  # Показываем фрейм


def create_settings_frames(title, is_animation=False, has_points=True, has_lines=True):
    """Функция создания динамических фреймов для дополнительной настройки графиков"""

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

    print(f"Creating frame: {title}, is_animation={is_animation}")

    if is_animation:
        #print(is_animation)
        global repeat_var
        repeat_check = ttk.Checkbutton(frame, text="Repeating", variable=repeat_var)
        repeat_check.grid(row=0, column=0, sticky='w', padx=5, pady=2)

    if has_points:

        colormap_var = tk.BooleanVar(value=False)
        colormap_check = ttk.Checkbutton(frame, text="Colormap", variable=colormap_var, command=toggle_colormap)
        colormap_check.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        ttk.Label(frame, text="Выбор карты: ").grid(row=2, column=3, sticky="w", padx=5, pady=2)
        colormap_combobox = ttk.Combobox(frame, values=['Jet', 'Blues', 'Viridis', 'Plasma'], state='disabled',
                                         width=7)
        colormap_combobox.grid(row=2, column=4, sticky="w")

        ttk.Label(frame, text="Цвет точек: ").grid(row=2, column=5, sticky="w", padx=5, pady=2)
        color_combobox = ttk.Combobox(frame, values=['red', 'blue', 'black'], state="readonly", width=7)
        color_combobox.grid(row=2, column=6, sticky="w")

        global points_size_var
        ttk.Label(frame, text="Размер точек: ").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        #ttk.Entry(frame, width=10).grid(row=2, column=1, sticky="w")
        points_size = tk.Spinbox(frame, from_=1, to=20, width=5, textvariable=points_size_var)
        points_size.grid(row=2, column=1, sticky="w")
        #print(points_size.get())
        #point_count.set(1)


    if has_lines:
        #print('Hi')
        ttk.Label(frame, text="Цвет линий: ").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(frame, width=10).grid(row=3, column=1, sticky="w")
        ttk.Label(frame, text="Ширина линий: ").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(frame, width=10).grid(row=4, column=1, sticky="w")

    return label, frame


# Создание главного окна
root = tk.Tk()
root.title("Случайное блуждание")
root.geometry("500x750+100+100")
root.resizable(False, False)

# Создание пустых словарей фреймов с дополнительными настройками и заголовков для них
frames = {}
labels = {}

# Создание списка с возможными комбинациями фреймов и заголовков в зависимости от состояния заданного пользователем
options = [
    ("static_points", "Настройки статических точек", False, True, False),
    ("static_lines", "Настройки статических линий", False, False, True),
    ("static_points_lines", "Настройки статических точек и линий", False, True, True),
    ("animation_points", "Настройки анимационных точек", True, True, False),
    ("animation_lines", "Настройки анимационных линий", True, False, True),
    ("animation_points_lines", "Настройки анимационных точек и линий", True, True, True),
]

# Добавляем все возможные комбинации в словари `frames` и `labels` и вызываем функцию для создания всех возможных
# комбинаций фреймов
for key, title, is_animation, has_points, has_lines in options:
    labels[key], frames[key] = create_settings_frames(title, is_animation, has_points, has_lines)

repeat_var = tk.BooleanVar(value=False)
points_size_var = tk.IntVar(value=5)



# Создание надписи на главном окне
ttk.Label(root, text='Settings Random Walk', font=("Arial", 14)).pack(pady=2)


# Блок создания фрейма для наполнения числовыми данными
#-----------------------------------------------------------------------------------------------------------------------
ttk.Label(root, text='Задание числовых данных', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

# Создание команды для валидации значений для поля Count points
vcmd = (root.register(validate_count_points), '%P')
# Создание строки Count points
ttk.Label(frame, text='Count points:').grid(row=0, column=0, sticky='w', padx=5, pady=2)
# Создание поля Counts points для ввода пользователем значения
count_points_entry = ttk.Entry(frame, width=10, validate='key', validatecommand=vcmd)
count_points_entry.grid(row=0, column=1, sticky='w', padx=2, pady=2)

# Создание команды для валидации значений для поля Max step
vcmd = (root.register(validate_max_step), '%P')
# Создание строки Max step
ttk.Label(frame, text='Max step:').grid(row=0, column=2, sticky='w', padx=5, pady=2)
# Создание поля Max step для ввода пользователем значения
max_step_entry = ttk.Entry(frame, width=5, validate='key', validatecommand=vcmd)
max_step_entry.grid(row=0, column=3, sticky='w', padx=5, pady=2)


# Блок создания фрейма для выбора вида графика
#-----------------------------------------------------------------------------------------------------------------------
ttk.Label(root, text='Вид графика', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

# Переменные-флаги в значении True (выбраны по умолчанию два вида представления)
line_var = tk.BooleanVar(value=True)
points_var = tk.BooleanVar(value=True)

# Отслеживание изменения в переменных и при их возникновении вызов лямбда-функции для создания дополнительных
# динамических фреймов с настройками в зависимости от вида графика
line_var.trace_add("write", lambda *args: update_settings_frame())
points_var.trace_add("write", lambda *args: update_settings_frame())

# Создание кнопок для выбора вида графика и их привязка к переменным и командам
line_check = ttk.Checkbutton(frame, text='Graphic line', variable= line_var, command=update_button_state)
line_check.grid(row=0, column=0, sticky='w', padx=5, pady=2)
points_check = ttk.Checkbutton(frame, text='Graphic points', variable=points_var, command=update_button_state)
points_check.grid(row=0, column=1, sticky='w', padx=5, pady=2)


# Создание кнопки для начала построения графиков
button = ttk.Button(root, text = "Create New", command=build_graphs, state=tk.DISABLED)
button.pack(side='bottom', pady=10)




ttk.Label(root, text='Способ отображения', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

mode_var = tk.StringVar(value='static')
mode_var.trace_add("write", lambda *args:update_settings_frame())

#
static_radio = ttk.Radiobutton(frame, text="Static", variable=mode_var, value='static')
static_radio.grid(row=0, column=0, sticky='w', padx=5, pady=2)

animation_radio = ttk.Radiobutton(frame, text='Animation', variable=mode_var, value='animation')
animation_radio.grid(row=0, column=1, sticky='w', padx=5, pady=2)

count_points_entry.bind_all("<Key>", update_button_state)



# Динамическое отображение нужного дополнительного фрейма в зависимости от выбора пользователя
update_settings_frame()

root.mainloop()

