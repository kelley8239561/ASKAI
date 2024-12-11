import sys
sys.path.append('d:\\KAIShow Tech\\20240605ASK\\ASK')
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
import PyQt6.QtCore
import graphic_interface.ui.test_window_ui
import graphic_interface.ui.test_widget_ui
app = QApplication(sys.argv)
window = QMainWindow()
graphic_interface.ui.test_window_ui.Ui_MainWindow().setupUi(window)
window.show()

window1 = QWidget()
graphic_interface.ui.test_widget_ui.Ui_Form().setupUi(window1)
window1.show()

sys.exit(app.exec())


# test_widget.setupUi()