import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk, SOLID
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
from metrics import MetricCheckBox

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
    # Объявление глобальных переменных
    global points_size_var
    global line_size_var
    global points_colormap_var
    global points_color_var
    global colormap_var
    global line_color_var

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
        # Задание размера окна для точечного графика
        plt.figure(figsize=(9, 5))

        # Получение пользовательского значения размера точек
        size_points = int(points_size_var.get())
        # Получение пользовательского значения цветовой карты точек
        points_colormap = points_colormap_var.get()
        # Получение пользовательского значения цвета точек
        points_color = points_color_var.get()
        # Получение пользовательского значения чек-бокса цветовой карты
        colormap_mode = colormap_var.get()

        # Разделение на цветовую карту и обычный цвет и их выбор пользователем
        if colormap_mode:
            # Создание точечной диаграммы с вычисленными точками для X,Y с цветовой картой
            plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=points_colormap, edgecolors='none', s=size_points)
        else:
            # Создание точечной диаграммы с вычисленными точками для X,Y определенного цвета
            plt.scatter(rw.x_values, rw.y_values, c=points_color, edgecolors='none',
                        s=size_points)

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
        # Получение пользовательского значения ширины линии
        line_color = line_color_var.get()
        # Получение пользовательского значения цвета линии
        line_size = line_size_var.get()
        # Создание линейной диаграммы с вычисленными точками для X, Y
        plt.plot(rw.x_values, rw.y_values, c=line_color, linewidth = line_size, zorder =1)

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
    # Объявление глобальных переменных
    global points_size_var
    global line_size_var
    global colormap_var
    global points_colormap_var
    global points_color_var
    global line_color_var

    # Закрытие всех активных окон
    plt.close('all')
    # Сохранение в виде целого числа кол-ва точек от пользователя
    count_points = int(count_points_entry.get())
    # Сохранение в виде целого числа максимальной длины шага от пользователя
    max_step = int(max_step_entry.get())
    # Переменная для хранения состояния чек-бокса повторения анимации
    repeat_animation = repeat_var.get()
    # Создание экземпляра с регулируемой длиной списка координат точек
    rw = RandomWalk(count_points, max_step)
    # Заполнение списка координатами
    rw.fill_walk()

    # Если выбрана анимация линий
    if line_var.get():
        # Получение пользовательских значений цвета линии
        line_color = line_color_var.get()
        # Получение пользовательских значений ширины линии
        line_size = line_size_var.get()

        # Создание окна графика и осей
        fig, ax = plt.subplots(figsize=(8, 6))

        # Установка границ осей
        ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)

        # Создание начальной точки и линии
        current_point_for_lines, = ax.plot(rw.x_values[0], rw.y_values[0], 'ro')
        line, = ax.plot([], [], c=line_color, linewidth=line_size)
        # Отрисовка увеличенных начальной и конечной точек блуждания
        start_point_for_line = plt.scatter(0, 0, c='green', edgecolors='none', s=100, zorder=2)
        end_point_for_line = plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100, zorder=2)
        # Отрисовка линии между начальной и конечной точками
        distance_line, = ax.plot([],[], c='red', linestyle='--', linewidth=3,
                 label='Line between points')


        def init_line():
            """Функция инициализации"""
            # Установка пустых кадров для линий и точки
            line.set_data([],[])
            current_point_for_lines.set_data([], [])
            distance_line.set_data([], [])
            start_point_for_line.set_offsets(np.empty((0, 2)))
            end_point_for_line.set_offsets(np.empty((0, 2)))
            # Возврат кортежей с объектами линий и точки
            return line, current_point_for_lines, distance_line, start_point_for_line, end_point_for_line

        def create_update_line_function(repeat_animation):
            def update_line(frame):
                """Функция обновления"""
                # Обновление вида линии от начала и до текущего кадра
                line.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
                # Обновление вида точки на текущем кадре
                current_point_for_lines.set_data([rw.x_values[frame]], [rw.y_values[frame]])

                if not repeat_animation and frame == len(rw.x_values)-1:
                    distance_line.set_data([0, rw.x_values[-1]], [0, rw.y_values[-1]])
                    start_point_for_line.set_offsets([[0,0]])
                    end_point_for_line.set_offsets([[rw.x_values[-1], rw.y_values[-1]]])
                # Возврат кортежей с объектами линий и точки
                return line, current_point_for_lines, distance_line, start_point_for_line, end_point_for_line
            return update_line
        # Управление анимацией
        animation_line = animation.FuncAnimation(fig, create_update_line_function(repeat_animation), frames=len(rw.x_values), init_func=init_line, blit=
                                                 True, interval=0, repeat=repeat_animation)
        # Установка заголовка для окна с анимацией
        plt.title("Анимация линий")

    # Если выбрана анимация точек
    if points_var.get():
        # Получение пользовательского значения размера точек
        size_points = int(points_size_var.get())
        # Получение пользовательского значения чек-бокса цветовой карты
        colormap_mode = colormap_var.get()
        # Получение пользовательского значения цветовой карты точек
        points_colormap = points_colormap_var.get()
        # Получение пользовательского значения цвета точек
        points_color = points_color_var.get()

        # Создание списка длиной количества точек
        point_numbers = list(range(rw.num_points))
        # Создание окна графика и осей
        fig, ax = plt.subplots(figsize=(8, 6))
        # Установка границ осей
        ax.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)
        # Создание начальных точек
        #points, = ax.plot([], [], 'ro', markersize=(size_points**0.5))
        current_point, = ax.plot(rw.x_values[0], rw.y_values[0], 'ro')
        # Отрисовка увеличенных начальной и конечной точек блуждания
        start_point = plt.scatter(0, 0, c='green', edgecolors='none', s=100, zorder=2)
        end_point = plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100, zorder=2)
        # Отрисовка линии между начальной и конечной точками
        distance_line_for_points_graph, = ax.plot([],[], c='red', linestyle='--', linewidth=3,
                 label='Line between points')

        # Обработка случая отображения с цветовой картой
        if colormap_mode:
            points = ax.scatter([], [], c=[], s=size_points, cmap=points_colormap, norm=plt.Normalize(vmin=0, vmax=len(point_numbers)))
        # Обработка случая отображения без цветовой карты
        else:
            points = ax.scatter([], [], s=size_points, color=points_color)

        def init_points():
            """Функция инициализации"""
            # Установка пустых кадров для точек
            points.set_offsets([])
            # Для случая отображения с цветовой картой
            if colormap_mode:
                points.set_array([])
            current_point.set_data([], [])
            distance_line_for_points_graph.set_data([], [])
            start_point.set_offsets(np.empty((0, 2)))
            end_point.set_offsets(np.empty((0, 2)))
            return points, current_point, distance_line_for_points_graph, start_point, end_point

        def update_create_point_function(repeat_animation):
            def update_points(frame):
                """Функция обновления"""
                # Обновление вида точек от начала и до текущего кадра
                #points.set_offsets([[x, y] for x, y in zip(rw.x_values[:frame+1], rw.y_values[:frame+1])])
                points.set_offsets(np.column_stack((rw.x_values[:frame+1], rw.y_values[:frame+1])))
                # Для случая отображения с цветовой картой
                if colormap_mode:
                    points.set_array(np.array(point_numbers[:frame+1]))
                # Обновление вида точки на текущем кадре
                current_point.set_data([rw.x_values[frame]], [rw.y_values[frame]])

                if not repeat_animation and frame == len(rw.x_values)-1:
                    distance_line_for_points_graph.set_data([0, rw.x_values[-1]], [0, rw.y_values[-1]])
                    start_point.set_offsets([[0,0]])
                    end_point.set_offsets([[rw.x_values[-1], rw.y_values[-1]]])
                return points, current_point, distance_line_for_points_graph, start_point, end_point

            return update_points
            # Управление анимацией
        animation_points = animation.FuncAnimation(fig, update_create_point_function(repeat_animation), frames = len(rw.x_values),
                                                   init_func=init_points, blit=True, interval=0, repeat=repeat_animation)
        # Установка заголовка для окна с анимацией
        plt.title('Анимация точек')

    # Отображение выбранных окон
    plt.show()


def validate_count_points(input_value):
    """Валидация значений в поле count points окна настроек"""
    if input_value == "":  # Разрешаем пустое поле
        return True
    if input_value.isdigit(): # Для случая заполненного поля
        num = int(input_value)
        if 0 <= num <= 5000:  # Проверка диапазона
            return True
    return False


def validate_max_step(input_value):
    """Валидация значений в поле max_step окна настроек"""
    if input_value == "":  # Разрешаем пустое поле
        return True
    if input_value.isdigit(): # Для случая заполненного поля
        num = int(input_value)
        if 0 <= num <= 30:    # Проверка диапазона
            return True
    return False


def update_button_state(event="<Key>"):
    """Функция для обновления состояния кнопки Create New (активно/неактивна) в зависимости от условий"""
    # Проверяем, выбран ли хотя бы один чекбокс
    checkbox_selected = line_var.get() or points_var.get()
    # Проверка на введенное число в строке Count points
    try:
        # Получение числа введенного пользователем
        count_points = int(count_points_entry.get())
        # Проверка нахождения числа в диапазоне от 1 до 5000
        entry_valid_count_points = 0 < count_points < 5001
    except ValueError:
        # В случае нахождения числа за пределами диапазона флаг в положении False
        entry_valid_count_points = False

    # Проверка на введенное число в строке Max step
    try:
        # Получение числа введенного пользователем
        max_step = int(max_step_entry.get())
        # Проверка нахождения числа в диапазоне от 1 до 30
        entry_valid_max_step = 0 < max_step < 31
    except ValueError:
        # В случае нахождения числа за пределами диапазона флаг в положении False
        entry_valid_max_step = False

    # Если выбран хотя бы один чек-бокс и введенное число в нужном диапазоне
    if checkbox_selected and entry_valid_count_points and entry_valid_max_step:
        # Кнопка для построения графиков активна
        button.config(state=tk.NORMAL)
    else:
        # Кнопка для построения графиков не активна
        button.config(state=tk.DISABLED)


def update_settings_frame():
    """Функция подбора фреймов с настройками в зависимости от выбора пользователя"""
    # Скрытие старых фреймов и заголовков по умолчанию
    for key in frames:
        frames[key].pack_forget()
        labels[key].pack_forget()

    # Задание флага состояния для кнопки Static по-умолчанию
    is_static = (mode_var.get()=="static")
    # Обновление флага состояния для чек-бокса Graphic points (выбран ли пользователем этот CheckButton)
    is_points = points_var.get()
    # Обновление флага состояния для чек-бокса Graphic line (выбран ли пользователем этот CheckButton)
    is_lines = line_var.get()

    # Подбор ключа для выбора вида динамического фрейма с дополнительными настройками
    key = ('static' if is_static else 'animation')
    key += ('_points' if is_points else '') + ('_lines' if is_lines else '')

    if key in frames:
        labels[key].pack(anchor="nw", pady=(10, 0))      # Показываем заголовок
        frames[key].pack(anchor="nw", fill="x", padx=5)  # Показываем фрейм
        metrics_var.set(False)

    # Для случая выбора статичного отображения графика(-ов)
    if mode_var.get()=="static":
        # Кнопка повтора анимации неактивная
        repeat_check.config(state="disabled")
    else:
        # Кнопка повтора активна
        repeat_check.config(state="normal")


def create_settings_frames(title, metrics_label, metrics_frame, is_animation=False, has_points=True, has_lines=True):
    """Функция создания динамических фреймов для дополнительной настройки графиков"""
    # Импорт цветов
    colors = list(mcolors.CSS4_COLORS)
    # Импорт списка вариантов цветовых карт
    colormaps = plt.colormaps()

    # Создание заголовка фрейма
    label = ttk.Label(root, text=title, font=("Arial", 8))
    label.pack(pady=(10, 0))

    # Создание фрейма
    frame = ttk.Frame(root, borderwidth=1, relief=SOLID, padding=[8, 10])

    def toggle_colormap():
        """Обработка события выбора чек-бокса с цветовыми картами"""
        # Если чек-бокс выбран, то кнопка выбора цветовой карт активна, а выбора простого цвета НЕ активна
        if colormap_var.get():
            colormap_combobox.config(state="readonly")
            color_combobox.config(state="disabled")
        # Если чек-бокс НЕ выбран, то кнопка выбора цветовой карт НЕ активна, а выбора простого цвета активна
        else:
            colormap_combobox.config(state="disabled")
            color_combobox.config(state="normal")

    def toggle_metrics_frame():
        """Обработка события выбора чек-бокса с метриками"""
        # Если чек-бокс выбран, то отображается название и сам фрейм с метриками
        if metrics_var.get():
            metrics_label.pack(anchor='w', fill='x', pady=(10, 0))
            metrics_frame.pack(anchor="nw", fill="x", padx=5)
            # Становятся неактивны кнопки выбора графика и чек-боксы способов отображения
            line_check.config(state='disabled')
            points_check.config(state='disabled')
            static_radio.config(state='disabled')
            animation_radio.config(state='disabled')

        # Иначе фрейм с метриками скрыт
        else:
            metrics_frame.pack_forget()
            metrics_label.pack_forget()
            # Становятся активны кнопки выбора графика и чек-боксы способов отображения
            line_check.config(state='normal')
            points_check.config(state='normal')
            static_radio.config(state='normal')
            animation_radio.config(state='normal')

    # print(f"Creating frame: {title}, is_animation={is_animation}")

    #  Динамический фрейм для создания настроек анимации графиков
    # if is_animation:
    #     # Импорт переменной со значением для чек-бокса повтора анимации (по-умолчанию False)
    #     global repeat_var
    #     # Отрисовка чек-бокса повтора анимации в выбранной части фрейма
    #     repeat_check = ttk.Checkbutton(frame, text="Repeating", variable=repeat_var)
    #     repeat_check.grid(row=0, column=0, sticky='w', padx=5, pady=2)

    #  Динамический фрейм для создания настроек статического изображения графиков
    # if not is_animation:
    #     pass


    # Динамический фрейм для создания настроек точечного графика
    if has_points:
        # Создание чек-бокса выбора цветовой карты
        colormap_check = ttk.Checkbutton(frame, text="Colormap", variable=colormap_var, command=toggle_colormap)
        colormap_check.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        # Создание надписи для выбора цветовой карты
        ttk.Label(frame, text="Выбор карты: ").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        # Создание выпадающего списка с вариантами цветовых карт с привязкой к переменной points_colormap_var
        colormap_combobox = ttk.Combobox(frame, values=colormaps, state='disabled',
                                         width=7, textvariable=points_colormap_var)
        colormap_combobox.grid(row=1, column=3, sticky="w")

        # Создание надписи для выбора цвета точек
        ttk.Label(frame, text="Цвет точек: ").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        # Создание выпадающего списка с вариантами цвета точек
        color_combobox = ttk.Combobox(frame, values=colors, state="readonly", width=7, textvariable=points_color_var)
        color_combobox.grid(row=2, column=3, sticky="w")

        # Создание надписи для задания размера точек
        ttk.Label(frame, text="Размер точек: ").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        # Создание переключателя значений размера точек
        points_size = tk.Spinbox(frame, from_=1, to=100, width=5, state="readonly", textvariable=points_size_var)
        points_size.grid(row=2, column=1, sticky="w")
        #print(points_size.get())
        #point_count.set(1)

    # Динамический фрейм для создания настроек линейного графика
    if has_lines:
        # Создание надписи для цвета линии
        ttk.Label(frame, text="Цвет линий: ").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Combobox(frame, values=colors, width=7, state="readonly", textvariable=line_color_var).grid(row=3, column=1, sticky="w")

        # Создание надписи для ширины линии
        ttk.Label(frame, text="Ширина линий: ").grid(row=3, column=2, sticky="w", padx=5, pady=2)
        tk.Spinbox(frame, from_=1, to=20 ,width=5, state="readonly", textvariable=line_size_var).grid(row=3, column=3, sticky="w")

    # Создание чек-бокса с возможностью подсчёта метрик и со своим стилем
    style = ttk.Style()
    style.configure("Bold.TCheckbutton", font=("TLabel", 10, "bold"))
    check_metrics = ttk.Checkbutton(frame, text="Additional metrics", variable=metrics_var, command=toggle_metrics_frame, style="Bold.TCheckbutton")
    check_metrics.grid(row=4, column=0, sticky="w", padx=5, pady=2)

    #all_check_metrics = ttk.Checkbutton(frame, text="Check and show all metrics", variable=all_check_metrics_var, command=toggle_metrics_frame, style="Bold.TCheckbutton")
    #all_check_metrics.grid(row=4, column=1, sticky="e", padx=(0, 60))
    #all_check_metrics.config(state='disabled')

    # Возврат всех динамических фреймов
    return label, frame


def create_metrics_frame(parent):
    """Функция создания динамического окна с метриками"""
    # Создание надписи для окна с метриками
    label = ttk.Label(parent, text="Выбор дополнительных метрик", font=("Arial", 8))
    # Создание динамического фрейма для метрик
    frame = ttk.Frame(root, borderwidth=1, relief=SOLID, padding=[8, 10])
    # Создание переменной состояния для чек-бокса "Выбрать всё" для метрик
    all_check_metrics_var = tk.BooleanVar(value=False)

    # Создание списка с информацией о метриках:
    metrics_info = [
        ("Расстояние между точками", "distance", True),
        ("Максимальное расстояние между точками", "max_distance", True),
        ("Радиус блуждания","max_distance_from_start_radius", True),
        ("Центр масс","center_of_mass", True),
        ("Количество повторяющихся точек","repeat_points", True),
        ("Среднее направление движения","average_direction", True),
        ("Радиус охвата","convex_radius", True),
        ("Среднее расстояние от начальной точки","mean_distance_from_start", False),
        ("Максимальное удаление от начальной точки","max_distance_from_start_line", True),
        ("Количество пересечений с начальной точкой","start_point_crossings", False),
        ("Общее время движения","total_time", False),
        ("Соотношение перемещения к длине пути","displacement_to_path_ratio", False),
    ]

    # Создание пустого списка для объектов метрик
    metrics_object_list = []

    def on_any_metrics_toggle():
        """Функция проверки списка метрик"""
        # Проверка всех чек-боксов метрик
        all_enabled = all(metric.enabled_var.get() for metric in metrics_object_list)
        # Если все метрики выбраны, но чек-бокс "Выбрать все" не отмечен
        if all_enabled and not all_check_metrics_var.get():
            # Отмечаем чек-бокс "Выбрать всё"
            all_check_metrics_var.set(True)
        # Иначе если не все метрики выбраны, но чек-окс "Выбрать всё" отмечен
        elif not all_enabled and all_check_metrics_var.get():
            # Снимаем отметку с чек-бокса "Выбрать всё"
            all_check_metrics_var.set(False)

    # Для каждой метрики из списка
    for i, (label_text, key, show_flag) in enumerate(metrics_info):
        # Создание объекта метрики через класс
        metric = MetricCheckBox(frame, label_text, i, show_flag, on_toggle_callback=on_any_metrics_toggle)
        # Добавление объекта в список
        metrics_object_list.append(metric)


    def toggle_all_metrics():
        """Обработчик включения чек-бокса "Выбрать всё" """
        # Получение булевого значения переменной-состояния чек-бокса "Выбрать всё"
        all_selected = bool(all_check_metrics_var.get())
        #print("Toggle:", all_selected)
        # Для каждого объекта метрики из списка обновить состояние для чек-боксов
        for metric in metrics_object_list:
            metric.update_states(enable=all_selected, show=all_selected)


    # Создание чек-бокса "Выбрать всё" и задание его расположения
    all_check_metrics = ttk.Checkbutton(frame, text="Check all", command=toggle_all_metrics,variable=all_check_metrics_var, style="Bold.TCheckbutton")
    all_check_metrics.grid(row=len(metrics_info), column=0, sticky="e", columnspan=3, padx=55)

    return label, frame, list(metrics_object_list)


# Создание главного окна
root = tk.Tk()
root.title("Случайное блуждание")
root.geometry("500x780+100+100")
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

# ЗАДАНИЕ ЗНАЧЕНИЙ ПАРАМЕТРОВ ПО УМОЛЧАНИЮ
# Создание булевой переменной повтора анимации со значением False
repeat_var = tk.BooleanVar(value=False)
# Создание целочисленных переменных размера точек и ширины линии
points_size_var = tk.IntVar(value=5)
line_size_var = tk.IntVar(value=5)
# Создание строковой переменной со значением для цветовой карты точек
points_colormap_var = tk.StringVar(value="Greys")
# Создание строковых переменных со значением цвета точек и линии
points_color_var = tk.StringVar(value="blue")
line_color_var = tk.StringVar(value="blue")
# Создание целочисленной переменной со значением максимальной длины шага
max_step_var = tk.IntVar(value=5)
# Создание целочисленной переменной со значением кол-ва точек
count_points_var = tk.IntVar(value=500)
# Создание переменной для чек-бокса цветовой карты
colormap_var = tk.BooleanVar(value=False)

# Создание переменной для чек-бокса дополнительных метрик
metrics_var = tk.BooleanVar(value=False)

# Создание дополнительного окна с метриками с помощью функции
metrics_label, metrics_frame, metrics_list = create_metrics_frame(root)


# Добавляем все возможные комбинации в словари `frames` и `labels` и вызываем функцию для создания всех возможных
# комбинаций фреймов
for key, title, is_animation, has_points, has_lines in options:
    labels[key], frames[key] = create_settings_frames(title,metrics_label, metrics_frame, is_animation, has_points, has_lines)


# Создание надписи на главном окне
ttk.Label(root, text='Settings Random Walk', font=("Arial", 14)).pack(pady=2)

# Блок создания фрейма для наполнения числовыми данными
#-----------------------------------------------------------------------------------------------------------------------
# Создание надписи для фрейма
ttk.Label(root, text='Задание числовых данных', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

# Создание команды для валидации значений для поля Count points
vcmd = (root.register(validate_count_points), '%P')
# Создание строки Count points
ttk.Label(frame, text='Count points:').grid(row=0, column=0, sticky='w', padx=5, pady=2)
# Создание поля Counts points для ввода пользователем значения
count_points_entry = tk.Spinbox(frame, from_=1, to=5000, width=10, validate='key', validatecommand=vcmd, textvariable=count_points_var)
count_points_entry.grid(row=0, column=1, sticky='w', padx=2, pady=2)
# Привязка события нажатия клавиши в поле ввода Count Points для обновления состояния кнопки Create new
count_points_entry.bind_all("<Key>", update_button_state)

# Создание команды для валидации значений для поля Max step
vcmd = (root.register(validate_max_step), '%P')
# Создание строки Max step
ttk.Label(frame, text='Max step:').grid(row=0, column=2, sticky='w', padx=5, pady=2)
# Создание поля Max step для ввода пользователем значения
max_step_entry = tk.Spinbox(frame, from_=1, to=30, width=5, validate='key', validatecommand=vcmd, textvariable=max_step_var)
max_step_entry.grid(row=0, column=3, sticky='w', padx=5, pady=2)
# Привязка события нажатия клавиши в поле ввода Max Step для обновления состояния кнопки Create new
max_step_entry.bind_all("<Key>", update_button_state)


# Блок создания фрейма для выбора вида графика
#-----------------------------------------------------------------------------------------------------------------------
# Переменные-флаги в значении True (выбраны по умолчанию два вида представления)
line_var = tk.BooleanVar(value=False)
points_var = tk.BooleanVar(value=False)

# Отслеживание изменения в переменных и при их возникновении вызов лямбда-функции для создания дополнительных
# динамических фреймов с настройками в зависимости от вида графика
line_var.trace_add("write", lambda *args: update_settings_frame())
points_var.trace_add("write", lambda *args: update_settings_frame())

# Создание надписи для фрейма
ttk.Label(root, text='Вид графика', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

# Создание кнопок для выбора вида графика и их привязка к переменным и командам
line_check = ttk.Checkbutton(frame, text='Graphic line', variable= line_var, command=update_button_state)
line_check.grid(row=0, column=0, sticky='w', padx=5, pady=2)
points_check = ttk.Checkbutton(frame, text='Graphic points', variable=points_var, command=update_button_state)
points_check.grid(row=0, column=1, sticky='w', padx=5, pady=2)


# Блок создания фрейма для выбора способа отображения графика
#-----------------------------------------------------------------------------------------------------------------------
# Создание переменной со значением static
mode_var = tk.StringVar(value='static')
# Отслеживание изменения в переменной mode_var и при их возникновении вызов лямбда-функции
mode_var.trace_add("write", lambda *args:update_settings_frame())

# Создание надписи для фрейма
ttk.Label(root, text='Способ отображения', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
frame.pack(anchor="nw", fill="x", padx=5)

# Создание кнопки с текстом Static с привязкой к переменной mode_var
static_radio = ttk.Radiobutton(frame, text="Static", variable=mode_var, value='static')
static_radio.grid(row=0, column=0, sticky='w', padx=5, pady=2)
# Создание кнопки с текстом Animation с привязкой к переменной mode_var
animation_radio = ttk.Radiobutton(frame, text='Animation', variable=mode_var, value='animation')
animation_radio.grid(row=0, column=1, sticky='w', padx=5, pady=2)

# Отрисовка чек-бокса повтора анимации в выбранной части фрейма
repeat_check = ttk.Checkbutton(frame, text="Repeating", variable=repeat_var)
repeat_check.grid(row=0, column=2, sticky='w', padx=5, pady=2)

# Создание кнопки для начала построения графиков
button = ttk.Button(root, text = "Create New", command=build_graphs, state=tk.DISABLED)
button.pack(side='bottom', pady=10)


# Динамическое отображение нужного дополнительного фрейма в зависимости от выбора пользователя
update_settings_frame()

root.mainloop()

