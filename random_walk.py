from random import choice


class RandomWalk():
    """Класс для генерирования случайных блужданий"""
    def __init__(self, num_points=5000, max_step=8):
        """Инициализирует атрибуты блуждания"""
        self.num_points = num_points
        self.max_step = max_step +1

        # Задание начальной точки блуждания (0, 0)
        self.x_values = [0]
        self.y_values = [0]

    def get_step(self):
        """Определение направления и расстояния перемещения"""
        # Случайных выбор направления (для Х - лево, право; для У - вверх, низ)
        direction = choice([-1, 1])
        # Создание списка длины шагов от нуля до максимального заданного
        list_max_step = list(range(self.max_step))
        # Случайный выбор длины шага из созданного списка
        distance = choice(list_max_step)
        # Определения направления шага
        step = direction * distance
        # Возврат шага
        return step

    def fill_walk(self):
        """Дополнение массива точек блуждания"""
        # Пока длина списка Х-координат (равной длине У-координат) меньше кол-ва заданных точек блуждания
        while len(self.x_values) < self.num_points:
            # Вычисление направления и длины шага по осям
            x_step = self.get_step()
            y_step = self.get_step()
            # Игнорирование краевого случая, когда перемещение по осям равно нулю
            if x_step==0 and y_step==0:
                continue

            # Определение координат следующей точки после шага относительно последней для каждой оси
            next_x = self.x_values[-1] + x_step
            next_y = self.y_values[-1] + y_step

            # Сохранение координат x, y в соответствующих списках
            self.x_values.append(next_x)
            self.y_values.append(next_y)

