import tkinter as tk


class Cmd_Frame(tk.Frame):

    def __init__(self, master=None, cmd_type=None, unit=None):
        super().__init__(master)
        self.cmd_type = cmd_type
        self.unit = unit
        self.initComponent(master)

    def initComponent(self, master):
        self.rowconfigure(0, weight=1);
        self.rowconfigure(1, weight=1);
        self.rowconfigure(2, weight=1);
        self.columnconfigure(0, weight=1)

        self.title_label = tk.Label(self,
                                    text=self.cmd_type + ":",
                                    font=('Arial', 18),
                                    # width=self,
                                    # height=int(self.winfo_height() / 3) - 2
                                    )
        self.title_label.grid(row=0, column=0, sticky=tk.NW, padx=1, pady=1)

        self.value = tk.StringVar()
        self.value.set("0")
        self.value_label = tk.Label(self,
                                    textvariable=self.value,
                                    font=('Arial', 28),
                                    # width=15,
                                    # height=int(self.winfo_height() / 3) - 2
                                    )
        self.value_label.grid(row=1, column=0, sticky=tk.NSEW, padx=1, pady=1)

        self.unit_label = tk.Label(self,
                                   text=self.unit,
                                   font=('Arial', 14),
                                   # width=15,
                                   # height=int(self.winfo_height() / 3) - 2
                                   )
        self.unit_label.grid(row=2, column=0, sticky=tk.SE, padx=1, pady=1)

    def set_value(self, value_str):
        self.value.set(value_str)

    def get_value(self):
        return self.value.get()

    def disable_size_change(self):
        self.configure(height=self["height"], width=self["width"])
        self.grid_propagate(0)
