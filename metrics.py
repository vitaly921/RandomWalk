import tkinter as tk
from tkinter import ttk, SOLID

class MetricCheckBox:
    """Класс для создания пары чек-боксов, управляющих выбором метрики и её отображения на графике"""
    def __init__(self, parent, label, row, show_flag, repeat_var, key=None, calc_func=None, on_toggle_callback=None):
        """Функция инициализации
        - основного чек-бокса для включения-выключения метрики;
        - дополнительного чек-бокса для отображения включенной метрики на графике

        :param parent: основной frame;
        :param label: название метрики;
        :param row: номер строки (ряда) размещения чек-боксов;
        :param show_flag: флаг, регулирующий отображение чек-бокса 'Показать на графике' в окне настроек
        :param repeat_var: переменная, регулирующая состояние чек-бокса 'Повторить' в окне настроек
        :param key: id метрики;
        :param calc_func: закрепленная за метрикой внешняя функция для подсчета текущей метрики;
        :param on_toggle_callback: внешняя функция проверки выбора пользователем чек-боксов метрик """

        # Инициализация аргументов
        self.label = label
        self.key = key
        self.calc_func = calc_func
        self.repeat_var = repeat_var
        self.on_toggle_callback = on_toggle_callback

        # Создание булевых переменных-состояний чек-боксов метрики и "Показать на графике"
        self.enabled_var = tk.BooleanVar(value=False)
        self.show_var = tk.BooleanVar(value=False)


        # Создание чек-бокса текущей метрики с состоянием из self.enabled_var
        self.checkbox_enabled = ttk.Checkbutton(parent, text=label, variable=self.enabled_var, command=self._internal_toggle_callback)
        # Задание расположения чек-бокса
        self.checkbox_enabled.grid(row=row, column=0, sticky='w', padx=(0, 60))

        # Если передан флаг для отображения дополнительного чек-бокса метрики
        if show_flag:
            # Создание для текущей метрики чек-бокса "Показать на графике с состоянием из self.show_var"
            self.checkbox_show = ttk.Checkbutton(parent, text="Show on graph", variable=self.show_var)
            # Чек-бокс отображения метрики по-умолчанию неактивен для пользователя
            self.checkbox_show.config(state="disabled")
            # Задание расположение чек-бокса "Показать на графике"
            self.checkbox_show.grid(row=row, column=0, sticky='e', padx=300)
        # Иначе если флаг не передан, то дополнительный чек-бокс метрики не создаётся
        else:
            self.checkbox_show = None
            #self.show_var.set(True)

    def _internal_toggle_callback(self):
        """Функция обработки события нажатия на чек-бокс метрики"""
        # Вызов функции регулировки состояния чек-бокса "Показать на графике"
        self.toggle_show_state()
        # Вызов внешней функции вне класса
        if self.on_toggle_callback:
            self.on_toggle_callback()

    def toggle_show_state(self):
        """Функция обновления состояния чек-бокса 'Показать на графике'"""
        # Функция работает только если чек-бокс "Показать на графике" для текущей метрики доступен
        if self.checkbox_show is not None:
            # Если выбран чек-бокс с текущей метрикой
            if self.enabled_var.get():
                self.checkbox_show.config(state="normal")   # Чек-бокс "Показать на графике" становится доступным
                self.show_var.set(True)                     # Чек-бокс "Показать на графике" имеет значение True
                self.repeat_var.set(False)                  # Чек-бокс "Повторить" для анимации имеет значение False
            # Иначе если чек-бокс с метрикой не выбран
            else:
                self.checkbox_show.config(state="disabled") # Чек-бокс "Показать на графике" остаётся недоступным
                self.show_var.set(False)                    # Чек-бокс "Показать на графике" имеет значение False

    def update_states(self, enable=True, show=False):
        """Функция для обновления одновременного состояния чек-боксов метрики и 'Показать на графике'"""
        self.enabled_var.set(value=enable)
        self.show_var.set(value=show)
        # Синхронизация с функцией состояния чек-бокса 'Показать на графике'
        self.toggle_show_state()