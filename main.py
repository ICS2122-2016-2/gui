from PyQt4 import QtGui, uic
import os
import shutil
from Entrega4.SoftwareE4 import \
    calcular_datos_periodos, generar_benchmark, optimizar_con_simulacion


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

periods_window_ui = uic.loadUiType(
    get_absolute_path("./guis/periods_window.ui"))
simulation_window_ui = uic.loadUiType(
    get_absolute_path("./guis/simulation_window.ui"))


class GUI:
    def __init__(self):
        self.periods_window = PeriodsWindow()
        self.simulation_window = SimulationWindow()

        self.__bind_signals()
        self.create_folders()
        self.periods_window.show()
        self.periods_window.raise_()

    def __bind_signals(self):
        self.periods_window.file_path_push_button.clicked.connect(
            self.__on_periods_window_file_path_push_button_click
        )

        self.periods_window.calculate_push_button.clicked.connect(
            self.__on_periods_window_calculate_push_button_click
        )

        self.simulation_window.simulate_push_button.clicked.connect(
            self.__on_simulation_window_simulate_push_button_click
        )

    def create_folders(self):
        folders = ("./Datos",)
        for folder in folders:
            print("[GUI] Trying to create folder {}...".format(folder))
            try:
                os.mkdir(folder)
                print("[GUI] Folder created succesfully...")
            except FileExistsError:
                print("[GUI] Folder exists...")

    def __on_periods_window_file_path_push_button_click(self):
        print("[GUI] __on_periods_window_file_path_push_button_click")
        file_path = QtGui.QFileDialog.getOpenFileName()
        self.periods_window.file_path_line_edit.setText(file_path)

    # TODO: implementar barra de progreso...
    def __on_periods_window_calculate_push_button_click(self):
        print("[GUI] __on_periods_window_calculate_push_button_click")
        db_path = self.periods_window.file_path_line_edit.text()
        try:
            shutil.copy(db_path, "./retail.dat")
        except shutil.SameFileError:
            pass
        calcular_datos_periodos(self.periods_window.progress_bar)

    # TODO:implementar barra de progreso...
    def __on_simulation_window_simulate_push_button_click(self):
        print("[GUI] __on_simulation_window_simulate_push_button_click")

        # Benchmark
        generar_benchmark()

        # Mapeo entre texto y enteros
        mapeo = {
            "1er periodo": 1,
            "2do periodo": 2,
            "3er periodo": 3
        }
        periodo = mapeo[self.periods_combo_box.currentText()]
        velocidad_cliente = self.customer_speed_spin_box.value()

        optimizar_con_simulacion(
            periodo,
            velocidad_cliente,
            30,
            100,
            2000
        )


class PeriodsWindow(*periods_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class SimulationWindow(*simulation_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_items()

    def add_items(self):
        items = ("1er periodo", "2do periodo", "3er periodo")
        for item in items:
            self.periods_combo_box.addItem(items)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    gui = GUI()
    app.exec_()
