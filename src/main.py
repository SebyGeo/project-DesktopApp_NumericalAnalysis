import sys
import numpy as np
from scipy.interpolate import lagrange, CubicSpline
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog, QVBoxLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from gui import Ui_MainWindow
from math_functions import evaluate_func, bernstein_poly, lagrange_implementation

class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        
        self.plot_layout = QVBoxLayout(self.plot_widget)
        self.plot_layout.addWidget(self.canvas)

        self.current_file_path = None

        self.problem_combo.currentIndexChanged.connect(self.switch_layout)
        self.data_source_combo.currentIndexChanged.connect(self.update_lagrange_inputs)
        self.btn_browse_file.clicked.connect(self.open_file_dialog)
        self.btn_calc_bernstein.clicked.connect(self.run_bernstein)
        self.btn_calc_lagrange.clicked.connect(self.run_lagrange)
        self.btn_export_plot.clicked.connect(self.export_plot)
        
        self.problem_combo.setCurrentIndex(1)
        self.switch_layout()
        self.update_lagrange_inputs()
        
    def switch_layout(self):
        current_mode = self.problem_combo.currentText()
        if "Bernstein" in current_mode:
            self.bernstein_container.setVisible(True)
            self.lagrange_container.setVisible(False)
        else:
            self.bernstein_container.setVisible(False)
            self.lagrange_container.setVisible(True)
            
    def update_lagrange_inputs(self):
        source = self.data_source_combo.currentText()
        if source == "File":
            self.label_file.setVisible(True)
            self.btn_browse_file.setVisible(True)
            self.label_nodes_x.setVisible(False)
            self.input_nodes_x.setVisible(False)
            self.label_f_lagrange.setVisible(False)
            self.input_f_lagrange.setVisible(False)
        else:
            self.label_file.setVisible(False)
            self.btn_browse_file.setVisible(False)
            self.label_nodes_x.setVisible(True)
            self.input_nodes_x.setVisible(True)
            self.label_f_lagrange.setVisible(True)
            self.input_f_lagrange.setVisible(True)
        
    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self.centralwidget, "Choose data file", "", 
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)", 
            options=options
        )
        if file_path:
            self.current_file_path = file_path
            self.result_label.setText(f"Selected file:\n{file_path}")
    
    def export_plot(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.centralwidget, "Save Plot", "", 
            "PNG Image (*.png);;JPEG Image (*.jpg);;PDF Document (*.pdf);;All Files (*)", 
            options=options
        )
        if file_path:
            try:
                self.figure.savefig(file_path, bbox_inches='tight')
                QMessageBox.information(self.centralwidget, "Success", f"Plot successfully saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self.centralwidget, "Error", f"Failed to save plot:\n{str(e)}")
                
    
    def run_bernstein(self):
        a = self.input_a.value()
        b = self.input_b.value()
        n = self.input_n.value()
        x_eval = self.input_x_eval.value()
        f_str = self.input_f.text()

        if a >= b:
            QMessageBox.warning(self.centralwidget, "Warning", "a must be strictly less than b!")
            return
        if not (a <= x_eval <= b):
            QMessageBox.warning(self.centralwidget, "Warning", "x must be within the interval [a, b]!")
            return

        try:
            val_f = evaluate_func(f_str, x_eval)
            val_B = bernstein_poly(f_str, a, b, n, x_eval)
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Math Error", f"Function error: {str(e)}")
            return

        err_abs = abs(val_f - val_B)
        err_rel = (err_abs / abs(val_f)) * 100 if val_f != 0 else float('inf')

        self.result_label.setText(
            f"<b>Bernstein Results:</b><br>"
            f"f({x_eval}) = {val_f:.6f}<br>"
            f"B_{n}({x_eval}) = {val_B:.6f}<br>"
            f"Absolute Error = {err_abs:.6f}<br>"
            f"Relative Error = {err_rel:.6f} %"
        )

        x_plot = np.linspace(a, b, 200)
        y_plot_f = evaluate_func(f_str, x_plot)
        y_plot_B = bernstein_poly(f_str, a, b, n, x_plot)
        
        self.ax.clear()
        self.ax.plot(x_plot, y_plot_f, 'k-', linewidth=2, label=f"f(x) = {f_str}")
        self.ax.plot(x_plot, y_plot_B, 'r--', linewidth=2, label=f"B_{n}(x)")
        self.ax.set_title(f"Bernstein Approximation (n={n})")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()
    
    def run_lagrange(self):
        source = self.data_source_combo.currentText()
        self.ax.clear()

        try:
            if source == "Keyboard":
                x = np.array([float(i.strip()) for i in self.input_nodes_x.text().split(',')])
                f_str = self.input_f_lagrange.text()
                
                try:
                    y = evaluate_func(f_str, x)
                except Exception as e:
                    QMessageBox.critical(self.centralwidget, "Math Error", f"Function error: {str(e)}")
                    return

            elif source == "File":
                if not self.current_file_path:
                    QMessageBox.warning(self.centralwidget, "Warning", "Please select a file first.")
                    return
                try:
                    data = np.loadtxt(self.current_file_path, delimiter=',')
                    if data.shape[0] > data.shape[1]:
                        x = data[:, 0]
                        y = data[:, 1]
                    else:
                        x = data[0, :]
                        y = data[1, :]
                except Exception as e:
                    QMessageBox.critical(self.centralwidget, "File Error", f"Could not read the file.\nError: {e}")
                    return

            if len(x) != len(y) or len(x) < 2:
                QMessageBox.warning(self.centralwidget, "Warning", "You must input the same number of X and Y nodes (minimum 2).")
                return

            n_grad = len(x) - 1

            self.result_label.setText(
                f"<b>Lagrange Results:</b><br>"
                f"Calculated polynomial of maximum degree (n={n_grad}).<br>"
                f"X Nodes: {np.round(x, 2)}<br>"
                f"Y Values: {np.round(y, 2)}"
            )

            x_plot = np.linspace(min(x) - 1, max(x) + 1, 200)
            
            y_plot = lagrange_implementation(x_plot, x, y)
            
            if source == "Keyboard":
                y_real = evaluate_func(f_str, x_plot)
                self.ax.plot(x_plot, y_real, 'k--', label=f"f(x) = {f_str}")

            self.ax.plot(x_plot, y_plot, 'b-', linewidth=3, label=f"Lagrange Polynomial (degree {n_grad})")
            
            if self.check_compare.isChecked():
                poly_scipy = lagrange(x, y)
                y_plot_scipy = np.polyval(poly_scipy, x_plot)
                self.ax.plot(x_plot, y_plot_scipy, 'g:', linewidth=2, label="Scipy Lagrange")
                
                sort_idx = np.argsort(x)
                x_sorted = x[sort_idx]
                y_sorted = y[sort_idx]
                if len(np.unique(x_sorted)) == len(x_sorted) and len(x_sorted) >= 2:
                    cs = CubicSpline(x_sorted, y_sorted)
                    y_plot_cubic = cs(x_plot)
                    self.ax.plot(x_plot, y_plot_cubic, 'm-.', linewidth=2, label="Cubic Spline")
                    
            self.ax.plot(x, y, 'ro', markersize=8, label="Interpolation points")
            self.ax.set_title("Lagrange Polynomial Interpolation")
            self.ax.grid(True)
            self.ax.legend()
            self.canvas.draw()

        except ValueError:
            QMessageBox.critical(self.centralwidget, "Data Error", "Ensure you only input numbers separated by commas (e.g., 1, 2.5, 3).")
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())