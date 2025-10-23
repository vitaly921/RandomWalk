from collections import Counter
import matplotlib.pyplot as plt
import math
import ctypes
import tkinter as tk
from matplotlib.patches import Circle
from tkinter import ttk, SOLID
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.patches import Arc
#from net.visum_mapDistricts import highwaySinks1

from metrics import MetricCheckBox
from random_walk import RandomWalk


def build_graphs(metrics_object_list):
    """Функция для выбора способа отображения линейных и точечных графиков для дальнейшего построения"""
    # По умолчанию выбран статический способ отображения
    if mode_var.get() == 'static':
        build_static_graph(metrics_object_list)
    # Иначе выбирается анимированный способ отображения
    else:
        build_animation(metrics_object_list)


def build_static_graph(metrics_object_list):
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

    # Если выбран точечный график
    if points_var.get():
        # Задание размера окна для точечного графика для случая если выбраны метрики
        if metrics_var.get() and any(m.enabled_var.get() for m in metrics_object_list):
            fig, ax = plt.subplots(figsize=(12, 6))
            # Задание масштабирования
            ax.set_aspect('equal')
            # Задание отступа для графика
            plt.subplots_adjust(right=0.6)
        # Задание размера окна для точечного графика по-умолчанию
        else:
            fig, ax = plt.subplots(figsize=(8, 6))

        # Вызов функции для создания окна графика
        create_window_for_figure(metrics_var, metrics_object_list, rw, fig, ax)

        # Создание заголовка в окне графика
        plt.title("A graph of a random walk")
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


    # Если выбран линейный график
    if line_var.get():
        # Задание размера окна для линейного графика для случая если выбраны метрики
        if metrics_var.get() and any(m.enabled_var.get() for m in metrics_object_list):
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.set_aspect('equal')
            # Задание отступа для графика
            plt.subplots_adjust(right=0.6)
        # Задание размера окна для линейного графика по-умолчанию
        else:
            fig, ax = plt.subplots(figsize=(8, 6))

        # Вызов функции для создания окна графика
        create_window_for_figure(metrics_var, metrics_object_list, rw, fig, ax)
        # Создание заголовка в окне графика
        plt.title("График случайного блуждания линии")
        # Получение пользовательского значения ширины линии
        line_color = line_color_var.get()
        # Получение пользовательского значения цвета линии
        line_size = line_size_var.get()
        # Создание линейной диаграммы с вычисленными точками для X, Y
        plt.plot(rw.x_values, rw.y_values, c=line_color, linewidth = line_size, zorder =1)


    # Отображение графиков независимо от выбора
    plt.show(block=False)

    # Удаление осей X,Y
    #plt.axes().get_xaxis().set_visible(False)
    #plt.axes().get_yaxis().set_visible(False)


def build_animation(metrics_object_list):
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
    animations = []

    def is_graphical_metrics_enabled(metrics_object_list):
        """Вспомогательная функция для задания условия: чек-бокс метрик включен, повтор выключен,
         учитывается отрисовка выбранных пользователем метрик"""
        return(
                metrics_var.get() and
                not repeat_animation and
                any(m.enabled_var.get() for m in metrics_object_list) and
                any(m.show_var.get() for m in metrics_object_list)
        )

    def is_text_metrics_enabled(metrics_object_list):
        """Вспомогательная функция для задания условия: чек-бокс метрик включен, повтор включен или выключен,
        не учитывается отрисовка выбранных пользователем метрик"""
        return(
            (metrics_var.get() and repeat_animation and any(m.enabled_var.get() for m in metrics_object_list)) or
            (metrics_var.get() and not repeat_animation and any(m.enabled_var.get() for m in metrics_object_list))
        )

    # Если выбрана анимация линий
    if line_var.get():
        # Получение пользовательских значений цвета линии
        line_color = line_color_var.get()
        # Получение пользовательских значений ширины линии
        line_size = line_size_var.get()

        # Если чек-бокс "Additional metrics" активен и нет повтора, и выбраны какие-либо метрики пользователем с
        # чек-боксом "Показать на графике"
        if is_graphical_metrics_enabled(metrics_object_list):
            # Задание увеличенного размера окна
            fig_line, ax_line = plt.subplots(figsize=(12, 6))
            # Задание равного масштаба на осях для наглядности графического представления метрик
            ax_line.set_aspect('equal')
            # Задание отступа для графика
            plt.subplots_adjust(right=0.6)
        # Иначе если чек-бокс "Additional metrics" активен, и выбраны какие-либо метрики пользователем без
        # выбора чек-бокса "Показать на графике" и независимо от повтора
        elif is_text_metrics_enabled(metrics_object_list):
            # Задание увеличенного размера окна
            fig_line, ax_line = plt.subplots(figsize=(12, 6))
            # Задание равного масштаба на осях для наглядности графического представления метрик (отключено здесь)
            # ax.set_aspect('equal')
            # Задание отступа для графика
            plt.subplots_adjust(right=0.6)
            # Сразу отображаются метрики справа без графического представления на графике
            create_window_for_figure(metrics_var, metrics_object_list, rw, fig_line, ax_line)
        # Для остальных случаев график отображается в усечённом окне без масштабирования
        else:
            # Задание усечённого размера окна
            fig_line, ax_line = plt.subplots(figsize=(8, 6))

        # Установка границ осей
        ax_line.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax_line.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)

        # Создание начальной точки и линии
        current_point_for_lines, = ax_line.plot(rw.x_values[0], rw.y_values[0], 'ro')
        line, = ax_line.plot([], [], c=line_color, linewidth=line_size)


        def init_line():
            """Функция инициализации"""
            # Установка пустых кадров для линий и точки
            line.set_data([],[])
            current_point_for_lines.set_data([], [])
            # Возврат кортежей с объектами линий и точки
            return line, current_point_for_lines

        def create_update_line_function(repeat_animation):
            def update_line(frame):
                """Функция обновления"""
                # Обновление вида линии от начала и до текущего кадра
                line.set_data(rw.x_values[:frame+1], rw.y_values[:frame+1])
                # Обновление вида точки на текущем кадре
                current_point_for_lines.set_data([rw.x_values[frame]], [rw.y_values[frame]])

                # Если чек-бокс "Additional metrics" активен и нет повтора, и выбраны какие-либо метрики пользователем с
                # чек-боксом "Показать на графике" и сейчас строится последний кадр
                if is_graphical_metrics_enabled(metrics_object_list) and frame == len(rw.x_values) - 1:
                    # Отрисовка метрик с графическим представлением в окне с графиком
                    create_window_for_figure(metrics_var, metrics_object_list, rw, fig_line, ax_line)
                    fig_line.canvas.draw()
                # Возврат кортежей с объектами линий и точки
                return line, current_point_for_lines
            return update_line
        # Управление анимацией
        animation_line = animation.FuncAnimation(fig_line, create_update_line_function(repeat_animation), frames=len(rw.x_values), init_func=init_line, blit=
                                                 True, interval=0, repeat=repeat_animation)
        animations.append(animation_line)
        # Установка заголовка для окна с анимацией
        plt.title("Animation lines")

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

        # Если чек-бокс "Additional metrics" активен и нет повтора, и выбраны какие-либо метрики пользователем с
        # чек-боксом "Показать на графике"
        if is_graphical_metrics_enabled(metrics_object_list):
            # Задание увеличенного размера окна
            fig_point, ax_point = plt.subplots(figsize=(12, 6))
            # Задание равного масштаба на осях для наглядности графического представления метрик
            ax_point.set_aspect('equal')
            # Задание отступа для графика
            plt.subplots_adjust(right=0.6)
        # Иначе если чек-бокс "Additional metrics" активен, и выбраны какие-либо метрики пользователем без выбра
        # выбора чек-бокса "Показать на графике" и независимо от повтора
        elif is_text_metrics_enabled(metrics_object_list):
            # Задание увеличенного размера окна
            fig_point, ax_point = plt.subplots(figsize=(12, 6))
            # Задание равного масштаба на осях для наглядности графического представления метрик (отключено здесь)
            #ax.set_aspect('equal')
            # Задание отступа для графика
            plt.subplots_adjust(right=0.6)
            # Сразу отображаются метрики справа без графического представления на графике
            create_window_for_figure(metrics_var, metrics_object_list, rw, fig_point, ax_point)
        # Для остальных случаев график отображается в усечённом окне без масштабирования
        else:
            # Задание усечённого размера окна
            fig_point, ax_point = plt.subplots(figsize=(8, 6))

        # Установка границ осей
        ax_point.set_xlim(min(rw.x_values) - 1, max(rw.x_values) + 1)
        ax_point.set_ylim(min(rw.y_values) - 1, max(rw.y_values) + 1)

        # Создание начальных точек
        #points, = ax.plot([], [], 'ro', markersize=(size_points**0.5))
        current_point, = ax_point.plot(rw.x_values[0], rw.y_values[0], 'ro', lw=1)


        # Обработка случая отображения с цветовой картой
        if colormap_mode:
            points = ax_point.scatter([], [], c=[], s=size_points, cmap=points_colormap, norm=plt.Normalize(vmin=0, vmax=len(point_numbers)), lw=1)
        # Обработка случая отображения без цветовой карты
        else:
            points = ax_point.scatter([], [], s=size_points, color=points_color, lw=1)

        def init_points():
            """Функция инициализации"""
            # Установка пустых кадров для точек
            points.set_offsets(np.empty((0, 2)))
            points.set_zorder(1)
            # Для случая отображения с цветовой картой
            if colormap_mode:
                points.set_array([])
            current_point.set_data([], [])
            return points, current_point

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
                # Если чек-бокс "Additional metrics" активен и нет повтора, и выбраны какие-либо метрики пользователем с
                # чек-боксом "Показать на графике" и сейчас строится последний кадр
                if is_graphical_metrics_enabled(metrics_object_list) and frame == len(rw.x_values)-1:
                    # Отрисовка метрик с графическим представлением
                    create_window_for_figure(metrics_var, metrics_object_list, rw, fig_point, ax_point)
                    fig_point.canvas.draw()
                return points, current_point
            points.set_zorder(1)
            return update_points
            # Управление анимацией
        animation_points = animation.FuncAnimation(fig_point, update_create_point_function(repeat_animation), frames = len(rw.x_values),
                                                   init_func=init_points, blit=True, interval=0, repeat=repeat_animation)
        animations.append(animation_points)

        # Установка заголовка для окна с анимацией
        plt.title('Animation points')

    # Отображение выбранных окон
    plt.show()


def create_window_for_figure(metrics_var, metrics_object_list, rw, fig=None, ax=None):
    """Функция создания окна для графика"""
    # В зависимости от выбора дополнительных метрик определяется размер и наполнение окна
    if metrics_var.get() and any(m.enabled_var.get() for m in metrics_object_list):
        # Создание окна графика и осей
        #fig, ax = plt.subplots(figsize=(12, 5))
        #ax.set_aspect('equal')
        # Отбираем выбранные пользователем метрики
        enabled_metrics = [m for m in metrics_object_list if m.enabled_var.get()]
        # Получаем текст выбранных пользователем метрик
        metrics_text = '\n\n'.join(f'{m.label}' for m in enabled_metrics)
        # Получаем значения выбранных пользователем метрик
        metrics_value = '\n\n'.join(str(m.calc_func(ax, rw, m.show_var.get())) if callable(m.calc_func) else "...None" for m in enabled_metrics)

        # Отрисовка текста и значений выбранных метрик в окне с графиком
        fig.text(0.75, 0.92, "Расчёт метрик", fontsize=12, va='top', ha='left')
        fig.text(0.62, 0.85, metrics_text, fontsize=9, va='top', ha='left', family='monospace')
        fig.text(0.95, 0.85, metrics_value, fontsize=9, va='top', ha='right', family='monospace')

    return fig, ax


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
        # Кнопка повтора анимации неактивная и имеет значение False
        repeat_check.config(state="disabled")
        repeat_var.set(False)

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
        ttk.Label(frame, text="Choice: ").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        # Создание выпадающего списка с вариантами цветовых карт с привязкой к переменной points_colormap_var
        colormap_combobox = ttk.Combobox(frame, values=colormaps, state='disabled',
                                         width=7, textvariable=points_colormap_var)
        colormap_combobox.grid(row=1, column=3, sticky="w")

        # Создание надписи для выбора цвета точек
        ttk.Label(frame, text="Point color: ").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        # Создание выпадающего списка с вариантами цвета точек
        color_combobox = ttk.Combobox(frame, values=colors, state="readonly", width=7, textvariable=points_color_var)
        color_combobox.grid(row=2, column=3, sticky="w")

        # Создание надписи для задания размера точек
        ttk.Label(frame, text="Point size: ").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        # Создание переключателя значений размера точек
        points_size = tk.Spinbox(frame, from_=1, to=100, width=5, state="readonly", textvariable=points_size_var)
        points_size.grid(row=2, column=1, sticky="w")
        #print(points_size.get())
        #point_count.set(1)

    # Динамический фрейм для создания настроек линейного графика
    if has_lines:
        # Создание надписи для цвета линии
        ttk.Label(frame, text="Color line: ").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Combobox(frame, values=colors, width=7, state="readonly", textvariable=line_color_var).grid(row=3, column=1, sticky="w")

        # Создание надписи для ширины линии
        ttk.Label(frame, text="Width line: ").grid(row=3, column=2, sticky="w", padx=5, pady=2)
        tk.Spinbox(frame, from_=1, to=20 ,width=5, state="readonly", textvariable=line_size_var).grid(row=3, column=3, sticky="w")

    # Создание чек-бокса с возможностью подсчёта метрик и со своим стилем
    style = ttk.Style()
    style.configure("Bold.TCheckbutton", font=("Arial", 10, "bold"))
    check_metrics = ttk.Checkbutton(frame, text="Additional metrics", variable=metrics_var, command=toggle_metrics_frame, style="Bold.TCheckbutton")
    check_metrics.grid(row=4, column=0, sticky="w", padx=5, pady=2)

    #all_check_metrics = ttk.Checkbutton(frame, text="Check and show all metrics", variable=all_check_metrics_var, command=toggle_metrics_frame, style="Bold.TCheckbutton")
    #all_check_metrics.grid(row=4, column=1, sticky="e", padx=(0, 60))
    #all_check_metrics.config(state='disabled')

    # Возврат всех динамических фреймов
    return label, frame


def constant_stub(rw):
    """Функция-заглушка для результатов метрик"""
    return "...None"


def calc_dist(ax, rw, show_var):
    """Функция подсчета расстояния между начальной и конечной точками блуждания"""
    distance = round(math.sqrt((rw.x_values[-1] - rw.x_values[0]) ** 2 + (rw.y_values[-1] - rw.y_values[0]) ** 2), 2)
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки линии между начальной и конечной точками
        draw_dist(ax, rw)
    # Возврат значения метрики
    return distance


def draw_dist(ax, rw):
    """Рисует линию между начальной и конечной точками"""
    ax.scatter(0, 0, c='green', edgecolors='none', s=100, zorder=1, label='Start point')
    ax.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100, zorder=1, label="Finish point")
    ax.plot([0, rw.x_values[-1]], [0, rw.y_values[-1]], c='red', linestyle='--', linewidth=3,
            label='Line between Start and Finish points', zorder=10)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=7)


def calc_max_distance_between_points(ax, rw, show_var):
    """Функция подсчета максимального расстояния между точками"""
    # Создание переменной для хранения максимального расстояния с начальным значением 0
    max_dist = 0
    # Создание двух точек в координатах (0, 0)
    p1 = (rw.x_values[0], rw.y_values[0])
    p2 = (rw.x_values[0], rw.y_values[0])

    # Вычисление расстояния между каждой парой точек без повторений
    for i in range(len(rw.x_values)):
        for j in range(i+1, len(rw.x_values)):
            dist = math.hypot(rw.x_values[i]-rw.x_values[j], rw.y_values[i]-rw.y_values[j])
            # Если полученное расстояние больше максимального
            if dist > max_dist:
                # Обновление переменной с максимальным расстоянием
                max_dist = dist
                # Получение координат точек с максимальным расстоянием
                p1 = (rw.x_values[i], rw.y_values[i])
                p2 = (rw.x_values[j], rw.y_values[j])
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки линии между максимально удалёнными точками
        draw_max_dist(ax, rw, p1, p2)
    # Возврат округлённого значения метрики
    return round(max_dist, 2)


def draw_max_dist(ax, rw, p1, p2):
    """Рисует линию между максимально удалёнными точками"""
    ax.scatter(*p1, c='black', edgecolors='none', s=100, zorder=9, label='Fist max distant point')
    ax.scatter(*p2, c='purple', edgecolors='none', s=100, zorder=9, label='Second max distant point')
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c='orange', linestyle='-', linewidth=3,
            label='Line between the most distant points', zorder=10)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=7)


def calc_max_distance_from_start_point(ax, rw, show_var):
    """Функция подсчета радиуса блуждания"""
    # Создание переменной для хранения максимального расстояния с начальным значением 0
    max_dist = 0
    # Задание координат начальной точки (центра окружности)
    x0, y0 =  rw.x_values[0], rw.y_values[0]
    # Создание переменной для хранения координат самой удаленной точки от начаьной
    farthest_point = (x0, y0)
    # Перебор точек
    for x, y in zip(rw.x_values, rw.y_values):
        # Подсчёт расстояния между текущей и начальной точками
        dist = math.hypot(x-x0, y-y0)
        # Обновление значений максимального расстояния и координаты
        if dist > max_dist:
            max_dist = dist
            farthest_point = (x, y)
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки окружности с центром в начальной точке с радиусом максимального расстояния
        draw_max_distance_from_start_point(ax, x0, y0, max_dist, farthest_point)
    # Возврат округлённого значения метрики
    return round(max_dist, 2)


def draw_max_distance_from_start_point(ax, x0, y0, radius, farthest_point):
    """Функция отрисовки окружности с радиусом блуждания"""
    # Отрисовка круга с центром в начальной точке и радиусом максимального расстояния (блуждания)
    circle = plt.Circle((x0, y0), radius, color = 'blue', fill=False, linestyle='--', linewidth=2, zorder=2,
                        label='A circle with a wandering radius')
    # Добавление круга на график
    ax.add_patch(circle)
    # Изменение размеров окна для наглядного вида с окружностью
    ax.set_xlim(min(ax.get_xlim()[0], x0 - radius), max(ax.get_xlim()[1], x0 + radius))
    ax.set_ylim(min(ax.get_ylim()[0], y0 - radius), max(ax.get_ylim()[1], y0 + radius))

    ax.plot([x0, farthest_point[0]], [y0, farthest_point[1]], color='black', linestyle='--', linewidth=2, zorder=3,
            label='Line of the radius of the walk')
    # Отрисовка начальной и максимально удаленной от неё точек
    ax.scatter([x0], [y0], color='green', s=80, zorder=4, label="Start point")
    ax.scatter([farthest_point[0]], [farthest_point[1]], color='red', s=80, zorder=4, label="Most remote point from Start")
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=8)


def center_of_mass(ax, rw, show_var):
    """Функция подсчёта координат центра масс"""
    x_avg = sum(rw.x_values)/len(rw.x_values)
    y_avg = sum(rw.y_values)/len(rw.y_values)
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки точки с центром масс
        draw_center_of_mass(ax, rw, x_avg, y_avg)
    # Возврат округленных значений координат центра масс
    return f"({x_avg:.2f},{y_avg:.2f})"


def draw_center_of_mass(ax, rw, x_avg, y_avg):
    """Функция отрисовки на графике центра масс"""
    ax.scatter(x_avg, y_avg, c='brown', s=200, marker='X', zorder=3, label="Center of mass")
    # Отрисовка пунктирных линий на оси координат
    ax.axhline(y=y_avg, color='brown', linestyle='--', linewidth=1)
    ax.axvline(x=x_avg, color='brown', linestyle='--', linewidth=1)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=8)


def calc_repeat_points(ax, rw, show_var):
    """Функция подсчёта кол-ва повторяющихся точек"""
    # Получение списка точек
    points = list(zip(rw.x_values, rw.y_values))
    # Подсчёт кол-ва точек
    points_counts = Counter(points)
    # Создание списка с повторяющимися точками
    repeated_points = [pt for pt, count in points_counts.items() if count>1]
    # Подсчёт повторяющихся точек
    count_repeat_points = len(repeated_points)
    # Подсчёт процента повторяющихся точек от общего кол-ва
    percent_repeat_points = count_repeat_points/len(points)*100
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки повторяющихся точек
        draw_repeat_points(ax, repeated_points)
    # Возврат кол-ва повторяющихся точек (в т.ч. в %)
    return f"{count_repeat_points} ({percent_repeat_points:.2f}%)"


def draw_repeat_points(ax, repeated_points):
    """Функция отрисовки повторяющихся точек"""
    # Обработка случая если повторяющихся точек нет, но флаг "Показать на графике" отмечен
    if not repeated_points:
        return
    # Сохранение координат повторяющихся точек
    xs, ys = zip(*repeated_points)
    # Отрисовка метки у повторяющихся точек
    ax.scatter(xs, ys, c='red', s=30, marker='*', label="Repeated points", zorder=5)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=8)


def calc_repeat_start_point(ax, rw, show_var):
    """Функция подсчета кол-ва возвратов в начальную точку"""
    # Задание начальных точек
    x0, y0 = rw.x_values[0], rw.y_values[0]
    # Задание начального кол-ва повторов
    repeats = 0
    # Перебор координат точек от второй до последней
    for x,y in zip(rw.x_values[1:], rw.y_values[1:]):
        # Проверка на наличие совпадений
        if x==x0 and y==y0:
            # Увеличение кол-ва совпадений
            repeats += 1
    # Возврат кол-ва совпадений
    return repeats


def angle_between_start_end_point(ax, rw, show_var):
    """Функция вычисления угла между начальной и конечной точками"""
    # Расстояние между координатой Х и У первой и последней точки
    dx_total = rw.x_values[-1] - rw.x_values[0]
    dy_total = rw.y_values[-1] - rw.y_values[0]

    # Вычисление угла в радианах
    angle_rad = math.atan2(dy_total, dx_total)
    # Вычисление угла в градусах
    angle_deg = math.degrees(angle_rad)
    # Переводим угол в диапазон [-180, 180)
    if angle_deg >= 180:
        angle_deg -= 360

    #angle_deg = (math.degrees(angle_rad) + 360) % 360

    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции отрисовки вектора и угла между ним и осью Х
        draw_angle_start_end(ax, rw, dx_total, dy_total, angle_rad, angle_deg)
    # Возврат значения угла в округленном виде
    return round(angle_deg, 2)


def draw_angle_start_end(ax, rw, dx_total, dy_total, angle_rad, angle_deg):
    """Функция отрисовки вектора от начальной до конечной точки и угла между ним и осью Х"""
    ax.annotate("", xy=(rw.x_values[-1], rw.y_values[-1]), xytext=(rw.x_values[0], rw.y_values[0]),
                arrowprops=dict(arrowstyle='->', color='black', lw=2), zorder=3, label='Vector from Start to End')
    # Создание надписи со значением угла
    #ax.text(rw.x_values[0] + 0.5, rw.y_values[0] + 0.5, f'{angle_deg:.1f}°', color='purple', fontsize=10, zorder=4)

    # Создание линий пересечения в начальной точке
    ax.axhline(y=rw.x_values[0], color='green', linestyle='-', linewidth=1)
    ax.axvline(x=rw.y_values[0], color='green', linestyle='--', linewidth=1)

    # Задание радиуса дуги угла
    arc_radius = 20

    # Проверка значения угла в радиусах для правильной отрисовки дуги
    if angle_deg >= 0:
        # Угол положительный: рисуем от 0 до angle_deg
        theta1, theta2 = 0, angle_deg
    else:
        # Угол отрицательный: рисуем от angle_deg до 0
        theta1, theta2 = angle_deg, 0

    # Создание угла как дуги
    arc = Arc((rw.x_values[0], rw.y_values[0]), width=2*arc_radius, height=2*arc_radius, theta1=theta1, theta2=theta2,
              color='red', linestyle='-', lw=2, label='Angle from X-axis to Vector')
    # Добавление угла на график
    ax.add_patch(arc)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=8)


def calc_average_direction(ax, rw, show_var):
    """Функция вычисления среднего направления движения"""
    # Задание пустого массива углов
    angles = []
    # Вычисление угла между каждыми точками
    for i in range(1, len(rw.x_values)):
        dx = rw.x_values[i] - rw.x_values[i-1]
        dy = rw.y_values[i] - rw.y_values[i-1]
        # Заполнение массива углами
        angles.append(math.atan2(dy, dx))
    # Вычисление среднего угла
    average_angle_rad = math.atan2(sum(math.sin(a) for a in angles) / len(angles),
                                   sum(math.cos(a) for a in angles) / len(angles))
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки
        draw_average_direction(ax, average_angle_rad)
    # Возврат значения среднего угла в округлённом виде
    return round(math.degrees(average_angle_rad), 2)


def draw_average_direction(ax, avg_angle):
    """Функция отрисовки среднего направления движения"""
    arrow_length = 35  # фиксированная длина
    # Задание начальной точки отрисовки стрелки
    x_base = ax.get_xlim()[0]
    y_base = ax.get_ylim()[0]
    # Вычисление точки конца стрелки
    dx = arrow_length * math.cos(avg_angle)
    dy = arrow_length * math.sin(avg_angle)

    # Отрисовка стрелки
    ax.annotate("Average\ndirection",
                xy=(x_base + dx, y_base + dy),
                xytext=(x_base, y_base),
                arrowprops=dict(arrowstyle="->", color="darkgreen", lw=3),
                zorder=3, label="Average direction")


def calc_convex_radius(ax, rw, show_var):
    """Функция вычисления радиуса размаха блуждания между самыми удаленными точками"""
    # Создание переменной для хранения максимального расстояния с начальным значением 0
    max_dist = 0
    # Создание двух точек в координатах (0, 0)
    p1 = (rw.x_values[0], rw.y_values[0])
    p2 = (rw.x_values[0], rw.y_values[0])

    # Вычисление расстояния между каждой парой точек без повторений
    for i in range(len(rw.x_values)):
        for j in range(i + 1, len(rw.x_values)):
            dist = math.hypot(rw.x_values[i] - rw.x_values[j], rw.y_values[i] - rw.y_values[j])
            # Если полученное расстояние больше максимального
            if dist > max_dist:
                # Обновление переменной с максимальным расстоянием
                max_dist = dist
                # Получение координат точек с максимальным расстоянием
                p1 = (rw.x_values[i], rw.y_values[i])
                p2 = (rw.x_values[j], rw.y_values[j])
    # Получение координат центральной точки на линии между двумя максимально удаленными точками
    center_x = (p1[0] + p2[0]) / 2
    center_y = (p1[1] + p2[1]) / 2
    # Получение радиуса размаха (половины длины линии между максимально удаленными точками)
    radius = max_dist / 2

    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки размаха блуждания в виде окружности
        draw_convex_radius(ax, rw, center_x, center_y, radius)
    return round(radius, 2)


def draw_convex_radius(ax, rw, x, y, radius):
    """Функция отрисовки размаха блуждания с диаметром равным максимальному расстоянию между точками"""
    circle = Circle((x, y), radius, edgecolor='orange', linestyle='--', linewidth=2, facecolor='none',
                    label='Convex Radius', zorder=2)
    ax.add_patch(circle)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=8)


def calc_coverage_radius(ax, rw, show_var):
    """Функция вычисления радиуса охвата от центра масс"""
    # Задание начального радиуса
    max_radius = 0.0
    # Вычисление точки центра масс
    x_avg = sum(rw.x_values)/len(rw.x_values)
    y_avg = sum(rw.y_values)/len(rw.y_values)

    # Перебор всех точек и вычисление максимально удаленной от центра масс
    for x, y in zip(rw.x_values, rw.y_values):
        radius = math.hypot(x - x_avg, y - y_avg)
        max_radius = max(max_radius, radius)
    # Если отмечен флаг "Показать на графике"
    if show_var:
        # Вызов функции для отрисовки охвата блуждания в виде окружности
        draw_coverage_radius(ax, rw, x_avg, y_avg, max_radius)
    # Возврат округленного значения максимального расстояния (радиуса от центра масс)
    return round(max_radius, 2)


def draw_coverage_radius(ax, rw, x_avg, y_avg, max_radius):
    """Функция отрисовки охвата блуждания с радиусом максимального расстояния от центра масс"""
    circle = Circle((x_avg, y_avg), max_radius, edgecolor='brown', linestyle='--', linewidth=2, facecolor='none',
                    label='Coverage Radius', zorder=2)
    ax.add_patch(circle)
    # Отрисовка обозначений
    ax.legend(loc="upper right", fontsize=8)


def calc_msd(ax, rw, show_var):
    """Функция подсчёта среднего квадрата перемещения"""
    # Задание начальной точки
    x0, y0 = rw.x_values[0], rw.y_values[0]
    # Задание начальной суммы квадратов расстояний
    sum_squared_dist = 0.0
    # Перебор всех точек и вычисление суммы квадратов расстояний относительно начальной
    for x, y in zip(rw.x_values, rw.y_values):
        # Вычисление расстояния между текущей точкой и начальной
        dx = x - x0
        dy = y - y0
        # Подсчёт суммы квадратов расстояний
        sum_squared_dist += math.hypot(dx, dy)**2
    # Деление суммы квадратов расстояний на количество точек
    msd = sum_squared_dist/len(rw.x_values)
    # Возврат округлённого значения среднего квадрата перемещения
    return round(msd, 2)


def calc_path_length(ax, rw, show_var):
    """Функция вычисления длины пути блуждания"""
    # Длина не будет подсчитана при количестве точек меньше двух
    if len(rw.x_values) < 2:
        return 0.0
    # Задание начальной длины
    total_length = 0.0
    # Перебор точек и суммирование длины между соседними
    for i in range(len(rw.x_values)-1):
        # Расстояние между соседними точками по координатам Х и У
        dx = rw.x_values[i+1] - rw.x_values[i]
        dy = rw.y_values[i+1] - rw.y_values[i]
        # Вычисление расстояния между соседними точками
        length = math.hypot(dx, dy)
        # Суммирование к общей длине
        total_length +=length
    # Возврат округлённого значения длины пути
    return round(total_length, 2)


def calc_efficiency_ratio(ax, rw, show_var):
    """Вычисляет отношение перемещения к длине пути (эффективность движения)"""
    # Метрика не будет считаться при кол-ве точек меньше двух
    if len(rw.x_values) < 2:
        return None
    # Подсчет пути и перемещения
    total_length = calc_path_length(ax, rw, False)
    displacement = calc_dist(ax, rw, False)
    # Если длина пути больше нуля
    if total_length > 0:
        # Подсчёт эффективности движения как отношения перемещения к длине пути
        efficiency = displacement/total_length
        # Перевод результата в проценты
        eff_percent = efficiency*100
    # Иначе эффективность нулевая
    else:
        efficiency = 0.0
        eff_percent = 0.0
    # Возврат вычисленной эффективности движения
    return f"{efficiency:.2f} ({eff_percent:.2f}%)"


def count_turns(ax, rw, show_var):
    """Функция подсчёта значимых поворотов (более 45 град.)в траектории блуждания"""
    # Задание значения угла, при котором поворот является значительным
    angle_threshold = 45
    # При кол-ве точек меньше трех кол-во поворотов равно нулю
    if len(rw.x_values) < 3:
        return 0

    # Задание начального значения кол-ва поворотов
    turn_count = 0
    # Подсчет всех возможных углов
    all_angles_count = len(rw.x_values) - 2

    # Перебор векторов всех точек
    for i in range(1, len(rw.x_values)-1):
        # Вектор предыдущего отрезка
        dx1 = rw.x_values[i] - rw.x_values[i-1]
        dy1 = rw.y_values[i] - rw.y_values[i-1]

        # Вектор следующего отрезка
        dx2 = rw.x_values[i+1] - rw.x_values[i]
        dy2 = rw.y_values[i+1] - rw.y_values[i]

        # Вычисляем угол между векторами
        angle = math.degrees(math.atan2(dy2, dx2) - math.atan2(dy1, dx1))
        angle = (angle + 180) % 360 -180    # Нормализация в диапазоне [-180, 180]

        # Если угол любого знака больше или равен значительному углу
        if abs(angle) >= angle_threshold:
            # Засчитываем поворот как значительный
            turn_count += 1
    # Вычисление процентного соотношения значимых поворотов от общего их числа
    percent_turn_count = turn_count / all_angles_count * 100
    # Возврат кол-ва значимых поворотов и их процентного соотношения
    return f"{turn_count} ({percent_turn_count:.2f}%)"


def mean_angles(ax, rw, show_var):
    """Расчет среднего угла поворота на траектории"""
    # Если кол-во точек меньше трех, то вычисление метрики не производится
    if len(rw.x_values) < 3:
        return 0
    # Создание списка с углами поворота
    angles = []
    # Перебор векторов пути
    for i in range(1, len(rw.x_values)-1):
        # Вектор предыдущего отрезка
        dx1 = rw.x_values[i] - rw.x_values[i-1]
        dy1 = rw.y_values[i] - rw.y_values[i-1]

        # Вектор следующего отрезка
        dx2 = rw.x_values[i+1] - rw.x_values[i]
        dy2 = rw.y_values[i+1] - rw.y_values[i]

        # Вычисляем угол между векторами
        angle = math.degrees(math.atan2(dy2, dx2) - math.atan2(dy1, dx1))
        angle = (angle + 180) % 360 -180    # Нормализация в диапазоне [-180, 180]
        # Добавление вычисленного угла в список
        angles.append(abs(angle))
    # Вычисление среднего угла поворота как отношение суммы всех углов к их кол-ву
    mean_angle = sum(angles)/len(angles) if angles else 0
    # Возврат округленного значения среднего угла поворота
    return round(mean_angle, 2)


def calc_average_step(ax, rw, show_var):
    """Функция подсчета средней длины шага"""
    # Если кол-во точек меньше двух - то подсчёт метрики не производится
    if len(rw.x_values) < 2:
        return None
    # Задание начальной длины шага
    length_steps = 0.0
    # Задание кол-ва шагов = кол-ву точек -1
    step_count = len(rw.x_values)-1
    # Для каждой точки
    for i in range(step_count):
        # Подсчет расстояния от следующей до текущей
        dx = rw.x_values[i+1] - rw.x_values[i]
        dy = rw.y_values[i+1] - rw.y_values[i]
        # Суммирования расстояния
        length_steps += math.hypot(dx, dy)
    # Вычисление средней длины шага как отношение суммы расстояний к кол-ву шагов
    average_length = length_steps / step_count
    return round(average_length, 2)


def on_repeat_toggle():
    """Функция обработчик нажатия кнопки чек-бокса повтора анимации"""
    # Получение текущего значения чек-бокса
    repeat_value = repeat_var.get()
    # Перебираем каждую метрику
    for metric in metrics_object_list:
        # Проверяем, есть ли у метрики этот чекбокс
        if metric.checkbox_show:
            # Для случая, если чек-бокс повтора True
            if repeat_value:
                # Делаем чек-бокс "Показать на графике" не активным и переводим в положение False
                metric.checkbox_show.config(state='disabled')
                metric.show_var.set(False)
            # Иначе если чек-бокс повтора не выделен, а метрика выбрана пользователем
            elif not repeat_value and metric.enabled_var.get():
                # Делаем чек-бокс "Показать на графике" активным
                metric.checkbox_show.config(state='normal')


def create_metrics_frame(parent):
    """Функция создания динамического окна с метриками"""
    # Создание надписи для окна с метриками
    label = ttk.Label(parent, text="Selecting additional metrics", font=("Arial", 8))

    # Создание внешнего фрейма, в который вложен Canvas и Scrollbar
    container = ttk.Frame(parent, borderwidth=1, relief=SOLID)
    # Задание фиксированной высоты контейнера
    container.config(height=200)
    # Запрет автоматическому подстраиванию фрейма по высоте содержимого
    container.pack_propagate(False)

    # Создание еще одного окна Canvas внутри контейнера
    canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
    # Задание высоты и ширины Canvas как у контейнера
    canvas.pack(side="left", fill="both", expand=True)

    # Создание Scrollbar, прикрепленного к окну Canvas (при прокрутке сдвигается Canvas)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    # Создание связи между Scrollbar и Canvas (определение местоположения)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Создание динамического фрейма для метрик
    frame = ttk.Frame(canvas, padding=[8, 10])
    # Прикрепление фрейма к Canvas для создания Scrollbar
    canvas.create_window((0, 0), window=frame, anchor="nw")

    def on_configure(event):
        """Обработчик добавления новых метрик во фрейм"""
        # Обновление области прокрутки для Canvas (bbox возвращает габариты фрейма со всеми метриками)
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Обработка события добавления новых метрик во фрейм
    frame.bind("<Configure>", on_configure)


    # Создание переменной состояния для чек-бокса "Выбрать всё" для метрик
    all_check_metrics_var = tk.BooleanVar(value=False)

    # Создание списка с информацией о метриках:
    metrics_info = [
        ("The distance between the start and end points", "distance", True, calc_dist),
        ("The length of the random walk path", "displacement_to_path_ratio", False, calc_path_length),
        ("Maximum distance between points", "max_distance", True, calc_max_distance_between_points),
        ("The radius of wandering from the starting point","max_distance_from_start_radius", True, calc_max_distance_from_start_point),
        ("Center of mass","center_of_mass", True, center_of_mass),
        ("Number of repeat points","repeat_points", True, calc_repeat_points),
        ("The angle between the start and end points","average_direction", True, angle_between_start_end_point),
        ("Trajectory span radius","convex_radius", True, calc_convex_radius),
        ("Radius of wandering from the center of mass", "coverage_radius", True, calc_coverage_radius),
        ("The average square of movement","mean_squared_displacement", False, calc_msd),
        ("The average direction of wandering","average_direction", True, calc_average_direction),
        ("Average step length between points","total_time", False, calc_average_step),
        ("The effectiveness of wandering","displacement_to_path_ratio", False, calc_efficiency_ratio),
        ("Number of significant turns", "total_time", False, count_turns),
        ("Average angle of rotation", "total_time", False, mean_angles),
    ]

    # Создание пустого списка для объектов метрик
    metrics_object_list = []

    def on_any_metrics_toggle():
        """Функция проверки выбранных метрик пользователем"""
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
    for i, (label_text, key, show_flag, calc_func) in enumerate(metrics_info):
        # Создание объекта метрики через класс
        metric = MetricCheckBox(frame, label_text, i, show_flag, repeat_var, key=key, calc_func=calc_func, on_toggle_callback=on_any_metrics_toggle)
        # Добавление объекта в список
        metrics_object_list.append(metric)


    def toggle_all_metrics():
        """Обработчик включения чек-бокса "Выбрать всё" """
        # Получение значения переменной-состояния чек-бокса "Выбрать всё"
        all_selected = bool(all_check_metrics_var.get())
        #print("Toggle:", all_selected)
        # Для каждого объекта метрики из списка обновить состояние для чек-боксов
        for metric in metrics_object_list:
            metric.update_states(enable=all_selected, show=False)
            #metric.show_var.set(True)
        #repeat_var.set(False)
        #on_repeat_toggle()

    # Создание чек-бокса "Выбрать всё" и задание его расположения
    all_check_metrics = ttk.Checkbutton(frame, text="Check all metrics", command=toggle_all_metrics,variable=all_check_metrics_var, style="Bold.TCheckbutton")
    all_check_metrics.grid(row=len(metrics_info), column=0, sticky="w", columnspan=5)

    return label, container, list(metrics_object_list)


# Создание главного окна
root = tk.Tk()
root.title("Random walk")
root.geometry("500x700+100+100")
root.resizable(False, False)
#icon = tk.PhotoImage(file='random_walk_icon.png')
root.iconbitmap('random_walk.ico')
# Иконка для панели задач (WinAPI)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
root.iconbitmap("random_walk.ico")

# Создание пустых словарей фреймов с дополнительными настройками и заголовков для них
frames = {}
labels = {}

# Создание списка с возможными комбинациями фреймов и заголовков в зависимости от состояния заданного пользователем
options = [
    ("static_points", "Point Static Settings", False, True, False),
    ("static_lines", "Line Static Settings", False, False, True),
    ("static_points_lines", "Settings for static points and lines", False, True, True),
    ("animation_points", "Point Animation Settings", True, True, False),
    ("animation_lines", "Line Animation Settings", True, False, True),
    ("animation_points_lines", "Animation settings for points and lines", True, True, True),
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
metrics_label, metrics_frame, metrics_object_list = create_metrics_frame(root)


# Добавляем все возможные комбинации в словари `frames` и `labels` и вызываем функцию для создания всех возможных
# комбинаций фреймов
for key, title, is_animation, has_points, has_lines in options:
    labels[key], frames[key] = create_settings_frames(title,metrics_label, metrics_frame, is_animation, has_points, has_lines)


# Создание надписи на главном окне
ttk.Label(root, text='Settings Random Walk', font=("Arial", 14)).pack(pady=2)

# Блок создания фрейма для наполнения числовыми данными
#-----------------------------------------------------------------------------------------------------------------------
# Создание надписи для фрейма
ttk.Label(root, text='Numerical data', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
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
ttk.Label(root, text='Type of graph', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
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
ttk.Label(root, text='Display method', font=("Arial", 8)).pack(anchor='nw', pady=(10, 0))
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

# Если отмечен чек-бок "Повторить анимацию", то вызов лямбда-функции
repeat_var.trace_add('write', lambda *args: on_repeat_toggle())

# Создание кнопки для начала построения графиков
button = ttk.Button(root, text = "Create New", command=lambda: build_graphs(metrics_object_list), state=tk.DISABLED)
button.pack(side='bottom', pady=7)


# Динамическое отображение нужного дополнительного фрейма в зависимости от выбора пользователя
update_settings_frame()

root.mainloop()

