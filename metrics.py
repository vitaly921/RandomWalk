import tkinter as tk
from tkinter import ttk, SOLID

class MetricCheckBox:
    """Класс для создания пары чек-боксов, управляющих выбором метрики и её отображения на графике"""
    def __init__(self, parent, label, row, show_flag, key=None, calc_func=None, on_toggle_callback=None):
        """Функция инициализации
        - основного чек-бокса для включения-выключения метрики;
        - дополнительного чек-бокса для отображения включенной метрики на графике

        :param parent: основной frame;
        :param label: название метрики;
        :param row: номер строки (ряда) размещения чек-боксов"""

        self.label = label
        self.key = key
        self.calc_func = calc_func
        # Создание булевых переменных-состояний чек-боксов
        self.enabled_var = tk.BooleanVar(value=False)
        self.show_var = tk.BooleanVar(value=True)
        self.on_toggle_callback = on_toggle_callback

        # Создание чек-боксов для включения-выключения чек-бокса метрики и её отображения на графике
        self.checkbox_enabled = ttk.Checkbutton(parent, text=label, variable=self.enabled_var, command=self._internal_toggle_callback)
        # Задание расположения чек-боксов
        self.checkbox_enabled.grid(row=row, column=0, sticky='w', padx=(0, 60))

        if show_flag:

            self.checkbox_show = ttk.Checkbutton(parent, text="Показать на графике", variable=self.show_var)
            # Чек-бокс отображения метрики на графике по-умолчанию отключен
            self.checkbox_show.config(state="disabled")
            self.checkbox_show.grid(row=row, column=0, sticky='e', padx=300)
        else:
            self.checkbox_show = None
            #self.show_var.set(True)

    def _internal_toggle_callback(self):
        """Функция для вызова функций обработки нажатия на чек-бокс метрики"""
        self.toggle_show_state()
        # Вызов внешней функции вне класса
        if self.on_toggle_callback:
            self.on_toggle_callback()

    def toggle_show_state(self):
        """Функция обновления доступности чек-бокса отображения на графике"""
        if self.checkbox_show is not None:
            # Если выбран чек-бокс с метрикой, то чек-бокс "Показать на графике" доступен
            if self.enabled_var.get():
                self.checkbox_show.config(state="normal")
                self.show_var.set(True)
            else:
                self.checkbox_show.config(state="disabled")
                self.show_var.set(False)

    def update_states(self, enable=True, show=False):
        """Функция для задания состояний всех чек-боксов"""
        self.enabled_var.set(value=enable)
        self.show_var.set(value=show)
        # Синхронизация с функцией обновления доступности чек-бокса отображения на графике
        self.toggle_show_state()