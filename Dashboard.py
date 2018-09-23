import tkinter as tk
import threading
import time
from Cmd_Frame import Cmd_Frame
import obd
from tkinter.ttk import Progressbar


class Dashboard:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Toyota Aurion Dashboard')
        self.window_height = self.window.winfo_screenheight()
        self.window_width = self.window.winfo_screenwidth()
        self.window.attributes("-fullscreen", True)
        self.window.config(
            padx=20,
            pady=20
        )

        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)

        # first row
        # =====================================================================
        # ================================|SPEED|==============================
        # =====================================================================
        self.speed_frame = Cmd_Frame(self.window, "Speed", "km/h")
        self.speed_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.speed_frame.config(
            width=int(self.window_width / 3) - 20,
            height=int(self.window_height / 2) - 20,
            relief=tk.GROOVE,
            bd=20,
            padx=50,
            pady=50,
        );
        self.speed_frame.disable_size_change()

        # =====================================================================
        # ================================|RPM|==============================
        # =====================================================================
        self.rpm_frame = Cmd_Frame(self.window, "RPM", "rpm")
        self.rpm_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.rpm_frame.config(
            width=int(self.window_width / 3) - 20,
            height=int(self.window_height / 2) - 20,
            relief=tk.GROOVE,
            bd=20,
            padx=50,
            pady=50,
        );
        self.rpm_frame.disable_size_change()

        # =====================================================================
        # ================================|LOAD|==============================
        # =====================================================================
        self.load_frame = Cmd_Frame(self.window, "load", "%")
        self.load_frame.grid(row=0, column=2, sticky=tk.NSEW)
        self.load_frame.config(
            width=int(self.window_width / 3) - 20,
            height=int(self.window_height / 2) - 20,
            relief=tk.GROOVE,
            bd=20,
            padx=50,
            pady=50,
        )

        self.progress_value = tk.DoubleVar()
        self.progress_value.set(0)
        self.progress_bar = Progressbar(self.load_frame, orient=tk.VERTICAL, variable=self.progress_value)
        self.progress_bar.grid(row=0, column=3, rowspan=2, sticky=tk.NS)

        self.load_frame.disable_size_change()

        # second row
        # =====================================================================
        # ============================|COOLANT TEMP|===========================
        # =====================================================================
        self.coolant_temp_frame = Cmd_Frame(self.window, "Coolant Temp", "C")
        self.coolant_temp_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.coolant_temp_frame.config(
            width=int(self.window_width / 3) - 20,
            height=int(self.window_height / 2) - 20,
            relief=tk.GROOVE,
            bd=20,
            padx=50,
            pady=50,
        );
        self.coolant_temp_frame.disable_size_change()

        # =====================================================================
        # ===========================|long term fuel|==========================
        # =====================================================================
        self.long_term_fuel_frame = Cmd_Frame(self.window, "Long Term Fuel", "L/100km")
        self.long_term_fuel_frame.grid(row=1, column=1, sticky=tk.NSEW)
        self.long_term_fuel_frame.config(
            width=int(self.window_width / 3) - 20,
            height=int(self.window_height / 2) - 20,
            relief=tk.GROOVE,
            bd=20,
            padx=50,
            pady=50,
        );
        self.long_term_fuel_frame.disable_size_change()

        # =====================================================================
        # ==========================|short term fuel|==========================
        # =====================================================================
        self.short_term_fuel_frame = Cmd_Frame(self.window, "Short Term Fuel", "L/100km")
        self.short_term_fuel_frame.grid(row=1, column=2, sticky=tk.NSEW)
        self.short_term_fuel_frame.config(
            width=int(self.window_width / 3) - 20,
            height=int(self.window_height / 2) - 20,
            relief=tk.GROOVE,
            bd=20,
            padx=50,
            pady=50,
        );
        self.short_term_fuel_frame.disable_size_change()

        self.window.bind("<F11>", self.toggle_fullscreen)
        self.window.bind("<Escape>", self.end_fullscreen)

    def start(self):
        self.window.mainloop()

    def set_speed_value(self, value_str):
        self.speed_frame.set_value(value_str)

    def toggle_fullscreen(self, event=None):
        self.window.attributes("-fullscreen", True)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.window.attributes("-fullscreen", False)
        return "break"


dashboard = Dashboard()


def set_speed(value_str):
    dashboard.speed_frame.set_value(str(value_str.value))


def set_RPM(value_str):
    dashboard.rpm_frame.set_value(str(value_str.value))


def set_load(value_str):
    dashboard.progress_value.set(value_str.value)
    dashboard.load_frame.set_value(str(value_str.value))


def set_temp(value_str):
    dashboard.coolant_temp_frame.set_value(str(value_str.value))


def set_long_fuel(value_str):
    dashboard.long_term_fuel_frame.set_value(str(value_str.value))


def set_short_fuel(value_str):
    dashboard.short_term_fuel_frame.set_value(str(value_str.value))


def connection_thread():
    connection = obd.Async()
    connection.watch(obd.commands.RPM, callback=set_RPM)
    connection.watch(obd.commands.SPEED, callback=set_speed)
    connection.watch(obd.commands.ENGINE_LOAD, callback=set_load)
    connection.watch(obd.commands.COOLANT_TEMP, callback=set_temp)
    connection.watch(obd.commands.SHORT_FUEL_TRIM_1, callback=set_short_fuel)
    connection.watch(obd.commands.LONG_FUEL_TRIM_1, callback=set_long_fuel)
    connection.start()
    # the callback will now be fired upon receipt of new values
    connection.stop()


def test():
    while (True):
        print(str(dashboard.progress_value.get()) + '\n')
        dashboard.progress_value.set(dashboard.progress_value.get() + 1)
        dashboard.load_frame.value.set(str(dashboard.progress_value.get()))
        time.sleep(0.5)


print(obd.scan_serial())

t = threading.Thread(target=connection_thread, name='thread-connection')
t.setDaemon(True)
t.start()

test = threading.Thread(target=test, name='thread-test')
test.setDaemon(True)
test.start()

dashboard.start()
