import tkinter as tk
from tkinter import ttk, SOLID

class MetricCheckBox:
    """"""
    def __init__(self, parent, label, row):
        """"""
        self.enabled_var = tk.BooleanVar(value=False)
        self.show_var = tk.BooleanVar(value=False)

        self.checkbox_enabled = ttk.Checkbutton(parent, text=label, variable=self.enabled_var, command=self.toggle_show_state)
        self.checkbox_show = ttk.Checkbutton(parent, text="Показать на графике", variable=self.show_var)

        self.checkbox_show.config(state="disabled")

        self.checkbox_enabled.grid(row=row, column=0, sticky='w', padx=(0, 60))
        self.checkbox_show.grid(row=row, column=1, sticky='e')

    def toggle_show_state(self):
        """"""
        print(self.enabled_var.get())
        if self.enabled_var.get():
            self.checkbox_show.config(state="normal")
        else:
            self.checkbox_show.config(state="disabled")

    def update_states(self, enable=True, show=False):
        self.enabled_var.set(value=enable)
        self.show_var.set(value=show)
        self.toggle_show_state()