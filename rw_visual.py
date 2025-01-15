import matplotlib.pyplot as plt
import math

from random_walk import RandomWalk

# Задание бесконечного цикла
while True:
    # Создание экземпляра с регулируемой длиной списка координат точек
    rw = RandomWalk(5000)
    # Заполнение списка координатами
    rw.fill_walk()
    # Сохранение списка длиной кол-ва точек
    point_numbers = list(range(rw.num_points))

    # Задание размера окна графика точек
    plt.figure(figsize=(9, 5))
    # Создание точечной диаграммы с вычисленными точками для X,Y
    plt.scatter(rw.x_values, rw.y_values, c=point_numbers, cmap=plt.cm.Greys, edgecolors='none', s=20)
    # Отрисовка увеличенных начальной и конечной точек блуждания
    plt.scatter(0, 0, c='green', edgecolors='none', s=100)
    plt.scatter(rw.x_values[-1], rw.y_values[-1], c='orange', edgecolors='none', s=100)
    plt.plot([0, rw.x_values[-1]], [0, rw.y_values[-1]], c='red', linestyle='--', linewidth=3,
             label='Line between points')

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
    # Ожидание ответа от пользователя на отрисовку следующего графика
    keep_running = input("Make another walk? (y/n): ")
    # Проверка условия продолжения работы программы и выхода из цикла
    if keep_running == 'n':
        break
