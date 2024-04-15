from SessionPage import SessionPage
from PyQt6.QtWidgets import QApplication
import time

if __name__ == "__main__":
    # Create MainWindow Instance with PyQT
    app = QApplication([])

    time.sleep(2)

    paint = False; # Variable to control the painting of the graph
    frontend = SessionPage(paint=paint)

    frontend.show()

    # Fixed values for the control
    fixed_k = 0.6
    fixed_angle = 53

    frontend.plotter.basic_control()
    # frontend.plotter.basic_control_with_last_data()
    # frontend.plotter.angle_control(fixed_k)
    # frontend.plotter.impedance_control(fixed_angle)

    app.exec()