from PyQt4 import QtGui, uic
import os


def get_absolute_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

main_window_ui = uic.loadUiType(get_absolute_path("./guis/main_window.ui"))


class GUI:
    def __init__(self):
        self.main_window = MainWindow()

        self.__bind_signals()
        self.main_window.show()
        self.main_window.raise_()

    def __bind_signals(self):
        self.main_window.push_button_file_path.clicked.connect(
            self.__on_main_window_push_button_file_path_clicked
        )

        self.main_window.push_button_simulate.clicked.connect(
            self.__on_main_window_push_button_simulate_clicked
        )

    def __on_main_window_push_button_file_path_clicked(self):
        file_path = QtGui.QFileDialog.getOpenFileName()
        self.main_window.line_edit_file_path.setText(file_path)

    def __on_main_window_push_button_simulate_clicked(self):
        # TODO: integrar backend...
        pass


class MainWindow(*main_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication([])
    gui = GUI()
    app.exec_()
