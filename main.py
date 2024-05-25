import sys
import matplotlib
from matplotlib import pyplot as plt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import scipy as scp
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSplitter, QApplication, \
    QStyleFactory, QTextEdit, QWidget, QPushButton, QTableWidget, QAction, QTableWidgetItem, QMenu
from data_loader import SpreadsheetLoader as SL
from plot_canvas import MplCanvas3D2D
from plotter import PlotHandler as PH


class main_frame(QMainWindow):

    def __init__(self):
        super(main_frame, self).__init__()
        self.loader = None
        self.plotter = None
        self.plot_frame_3 = None
        self.plot_frame_2 = None
        self.plot_frame_1 = None
        self.spreadsheet = None
        self.x_array = []
        self.y_array = []
        self.z_array = []
        self.init_UI()

    def init_UI(self):
        self.plot_frame_1 = MplCanvas3D2D()
        self.plot_frame_2 = MplCanvas3D2D()
        self.plot_frame_3 = MplCanvas3D2D()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox_central = QVBoxLayout(central_widget)
        hbox_splitter = QHBoxLayout()
        hbox_bottom = QHBoxLayout()

        spredsheet_frame = QFrame()
        spredsheet_frame.setFrameShape(QFrame.StyledPanel)

        plot_frame = QFrame()
        plot_frame.setFrameShape(QFrame.StyledPanel)

        plot_layout = QHBoxLayout()

        subplot_layout1 = QVBoxLayout()
        subplot_layout2 = QVBoxLayout()
        subplot_layout3 = QVBoxLayout()

        toolbar1 = NavigationToolbar(self.plot_frame_1, self)
        toolbar2 = NavigationToolbar(self.plot_frame_2, self)
        toolbar3 = NavigationToolbar(self.plot_frame_3, self)

        subplot_layout1.addWidget(toolbar1)
        subplot_layout1.addWidget(self.plot_frame_1)
        subplot_layout2.addWidget(toolbar2)
        subplot_layout2.addWidget(self.plot_frame_2)
        subplot_layout3.addWidget(toolbar3)
        subplot_layout3.addWidget(self.plot_frame_3)

        plot_layout.addLayout(subplot_layout1)
        plot_layout.addLayout(subplot_layout2)
        plot_layout.addLayout(subplot_layout3)

        terminal1_layout = QVBoxLayout()
        terminal2_layout = QVBoxLayout()
        terminal3_layout = QVBoxLayout()

        terminal_layout = QHBoxLayout()

        my_term_label = QLabel("Main terminal:")
        self.my_terminal = QTextEdit()

        numpy_label = QLabel("Numpy terminal:")
        self.numpy_terminal = QTextEdit()

        scipy_label = QLabel("Scipy terminal:")
        self.scipy_terminal = QTextEdit()

        terminal1_layout.addWidget(my_term_label)
        terminal1_layout.addWidget(self.my_terminal)

        terminal2_layout.addWidget(numpy_label)
        terminal2_layout.addWidget(self.numpy_terminal)

        terminal3_layout.addWidget(scipy_label)
        terminal3_layout.addWidget(self.scipy_terminal)

        terminal_layout.addLayout(terminal1_layout)
        terminal_layout.addLayout(terminal2_layout)
        terminal_layout.addLayout(terminal3_layout)

        Vplot_layout = QVBoxLayout()
        Vplot_layout.addLayout(plot_layout, 70)
        Vplot_layout.addLayout(terminal_layout, 30)

        plot_frame.setLayout(Vplot_layout)

        splitter = QSplitter()
        splitter.addWidget(spredsheet_frame)
        splitter.addWidget(plot_frame)
        splitter.setStretchFactor(1, 1)
        hbox_splitter.addWidget(splitter)

        vbox_central.addLayout(hbox_splitter)

        # Create a spreadsheet widget
        self.spreadsheet = QTableWidget(20, 3)
        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem()
                self.spreadsheet.setItem(i, j, item)

        # Add the spreadsheet to the layout
        spredsheet_layout = QVBoxLayout()
        spredsheet_layout.addWidget(QLabel("Data spreadsheet:"))
        spredsheet_layout.addWidget(self.spreadsheet)
        spredsheet_frame.setLayout(spredsheet_layout)
        spredsheet_frame.setMinimumWidth(400)
        self.loader = SL(self.spreadsheet)
        self.plotter = PH(self.plot_frame_1, self.plot_frame_2, self.plot_frame_3)
        self.create_menu_bar()
        self.setWindowTitle('Python spline comparator - MN project')
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        save_action = QAction('Save', self)
        saveas_action = QAction('Save As', self)
        load_action = QAction('Load Data', self)

        close_action = QAction('Close', self)
        file_menu.addAction(save_action)
        file_menu.addAction(saveas_action)
        file_menu.addAction(load_action)
        file_menu.addAction(close_action)
        plot_menu = menu_bar.addMenu('Plot')
        load_action.triggered.connect(self.loader.load_data_from_file)
        scatterplot = QAction('Scatter Plot', self)
        scatterplot.triggered.connect(self.init_scatter_plot)
        linearplot = QAction('Linear Plot', self)
        linearplot.triggered.connect(self.init_linear_plot)
        plot_menu.addAction(scatterplot)
        plot_menu.addAction(linearplot)
        analysis = QMenu('Analysis', self)
        linear_fit = QAction('Linear', self)
        linear_fit.triggered.connect(self.plot_Linear_fit2D)
        square_spline = QAction('Square Spline', self)
        square_spline.triggered.connect(self.plot_square_spline2D)
        qubic_spline = QAction('Qubic Spline', self)
        qubic_spline.triggered.connect(self.plot_qubic_spline2D)
        analysis.addAction(linear_fit)
        analysis.addAction(square_spline)
        analysis.addAction(qubic_spline)
        plot_menu.addMenu(analysis)
        help_menu = menu_bar.addMenu('Help')
        manual = QAction('Manual', self)
        docs = QAction('Documentation', self)
        help_menu.addAction(manual)
        help_menu.addAction(docs)

    def init_scatter_plot(self):
        column_values = SL.read_spreadsheet(self)
        if len(column_values) == 2:
            self.scatter_plot2D()
        elif len(column_values) == 3:
            self.scatter_plot3D()
        else:
            self.append_all("Error: Issue occurred while displaying data!")

    def init_linear_plot(self):
        column_values = SL.read_spreadsheet(self)
        if len(column_values) == 2:
            self.linear_plot2D()
        elif len(column_values) == 3:
            self.linear_plot3D()
        else:
            self.append_all("Error: Issue occured while displaying data")

    def linear_plot2D(self):
        self.clear_all()
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        self.plot_frame_1.lineplot2D(self.x_array, self.y_array, 'x', 'y', 'blue', True)
        self.plot_frame_2.lineplot2D(self.x_array, self.y_array, 'x', 'y', 'red', True)
        self.plot_frame_3.lineplot2D(self.x_array, self.y_array, 'x', 'y', 'green', True)
        self.append_all("Displayed data: ")
        self.append_all("X: ")
        for i in self.x_array:
            self.append_all(str(i))
        self.append_all("Y: ")
        for i in self.y_array:
            self.append_all(str(i))

    def linear_plot3D(self):
        self.clear_all()
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        self.z_array = column_values[2]
        self.plot_frame_1.lineplot3D(self.x_array, self.y_array, self.z_array, 'x', 'y', 'z', 'blue', True)
        self.plot_frame_2.lineplot3D(self.x_array, self.y_array, self.z_array, 'x', 'y', 'z', 'red', True)
        self.plot_frame_3.lineplot3D(self.x_array, self.y_array, self.z_array, 'x', 'y', 'z', 'green', True)
        self.append_all("Displayed data: ")
        self.append_all("X: ")
        for i in self.x_array:
            self.append_all(str(i))
        self.append_all("Y: ")
        for i in self.y_array:
            self.append_all(str(i))
        self.append_all("Z: ")
        for i in self.z_array:
            self.append_all(str(i))

    def scatter_plot2D(self):
        self.clear_all()
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        self.plot_frame_1.scatterplot2D(self.x_array, self.y_array, 'x', 'y', 'blue', True)
        self.plot_frame_2.scatterplot2D(self.x_array, self.y_array, 'x', 'y', 'red', True)
        self.plot_frame_3.scatterplot2D(self.x_array, self.y_array, 'x', 'y', 'green', True)
        self.append_all("Displayed data: ")
        self.append_all("X: ")
        for i in self.x_array:
            self.append_all(str(i))
        self.append_all("Y: ")
        for i in self.y_array:
            self.append_all(str(i))

    def scatter_plot3D(self):
        self.clear_all()
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        self.z_array = column_values[2]
        self.plot_frame_1.scatterplot3D(self.x_array, self.y_array, self.z_array, 'x', 'y', 'z', 'blue', True)
        self.plot_frame_2.scatterplot3D(self.x_array, self.y_array, self.z_array, 'x', 'y', 'z', 'red', True)
        self.plot_frame_3.scatterplot3D(self.x_array, self.y_array, self.z_array, 'x', 'y', 'z', 'green', True)
        self.append_all("Displayed data: ")
        self.append_all("X: ")
        for i in self.x_array:
            self.append_all(str(i))
        self.append_all("Y: ")
        for i in self.y_array:
            self.append_all(str(i))
        self.append_all("Z: ")
        for i in self.z_array:
            self.append_all(str(i))

    def plot_Linear_fit2D(self):
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        axN = self.plot_frame_2.get_axis()
        axS = self.plot_frame_3.get_axis()
        axM = self.plot_frame_1.get_axis()
        x_lineM, y_lineM = self.plotter.manual_interpolation_linear(self.x_array, self.y_array)
        axM.plot(x_lineM, y_lineM, color='orange')
        x_lineN, y_lineN = self.plotter.linear_fit_numpy2d(self.x_array, self.y_array)
        axN.plot(x_lineN, y_lineN, color='orange')
        x_lineS, y_lineS = self.plotter.linear_fit_scipy2d(self.x_array, self.y_array)
        axS.plot(x_lineS, y_lineS, color='orange')
        self.plot_frame_1.draw()
        self.plot_frame_2.draw()
        self.plot_frame_3.draw()

    def plot_square_spline2D(self):
        axN = self.plot_frame_2.get_axis()
        axS = self.plot_frame_3.get_axis()
        axM = self.plot_frame_1.get_axis()
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        x_lineN, y_lineN = self.plotter.numpy_square_spline(self.x_array, self.y_array, 100)
        axN.plot(x_lineN, y_lineN, color='orange')
        x_lineS, y_lineS = self.plotter.scipy_square_spline(self.x_array, self.y_array)
        axS.plot(x_lineS, y_lineS, color='orange')
        x = self.plotter.manual_square_spline(self.x_array, self.y_array)
        for i in range(len(x) // 3):
            x_spline = np.linspace(self.x_array[i], self.x_array[i + 1], 100)
            y_spline = x[3 * i] * x_spline ** 2 + x[3 * i + 1] * x_spline + x[3 * i + 2]
            axM.plot(x_spline, y_spline, color='orange')
        self.plot_frame_1.draw()
        self.plot_frame_2.draw()
        self.plot_frame_3.draw()

    def plot_qubic_spline2D(self):
        axN = self.plot_frame_2.get_axis()
        axS = self.plot_frame_3.get_axis()
        axM = self.plot_frame_1.get_axis()
        column_values = SL.read_spreadsheet(self)
        self.x_array = column_values[0]
        self.y_array = column_values[1]
        print("testing numpy qubic")
        x_lineN, y_lineN = self.plotter.numpy_qubic_spline(self.x_array, self.y_array, 100)
        axN.plot(x_lineN, y_lineN, color='orange')
        x_lineS, y_lineS = self.plotter.scipy_qubic_spline(self.x_array, self.y_array)
        axS.plot(x_lineS, y_lineS, color='orange')
        x = self.plotter.manual_qubic_spline(self.x_array, self.y_array)
        for i in range(len(x) // 4):
            x_spline = np.linspace(self.x_array[i], self.x_array[i + 1], 100)
            y_spline = x[4 * i] * x_spline ** 3 + x[4 * i + 1] * x_spline ** 2 + x[4 * i + 2] * x_spline + x[4 * i + 3]
            axM.plot(x_spline, y_spline, color='orange')
        self.plot_frame_1.draw()
        self.plot_frame_2.draw()
        self.plot_frame_3.draw()

    def append_text_t1(self, text):
        self.my_terminal.append(text)

    def append_text_t2(self, text):
        self.numpy_terminal.append(text)

    def append_text_t3(self, text):
        self.scipy_terminal.append(text)

    def append_all(self, text):
        self.append_text_t1(text)
        self.append_text_t2(text)
        self.append_text_t3(text)

    def clear_t1(self):
        self.my_terminal.clear()

    def clear_t2(self):
        self.numpy_terminal.clear()

    def clear_t3(self):
        self.scipy_terminal.clear()

    def clear_all(self):
        self.clear_t1()
        self.clear_t2()
        self.clear_t3()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = main_frame()
    main_window.show()
    sys.exit(app.exec_())
