from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas3D2D(FigureCanvasQTAgg):
    def __init__(self, parents=None, width=20, height=20, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.figure)

    def lineplot3D(self, x_array, y_array, z_array, x_label, y_label, z_label, color, clear_option):
        if clear_option is True:
            self.figure.clear()

        axs = self.figure.add_subplot(111, projection='3d', position=[0.1, 0.1, 0.85, 0.85])
        axs.plot(x_array, y_array, z_array, color=color)
        axs.set_xlabel(x_label)
        axs.set_ylabel(y_label)
        axs.set_zlabel(z_label)
        self.draw()

    def lineplot2D(self, x_array, y_array, x_label, y_label, color, clear_option):
        if clear_option is True:
            self.figure.clear()

        axs = self.figure.add_subplot(111, position=[0.1, 0.1, 0.85, 0.85])
        axs.plot(x_array, y_array, color=color)
        axs.set_xlabel(x_label)
        axs.set_label(y_label)
        self.draw()

    def scatterplot3D(self, x_array, y_array, z_array, x_label, y_label, z_label, color,  clear_option):
        if clear_option is True:
            self.figure.clear()
        axs = self.figure.add_subplot(111, projection='3d', position=[0.1, 0.1, 0.85, 0.85])
        axs.scatter(x_array, y_array, z_array, color=color, s=10)
        axs.set_xlabel(x_label)
        axs.set_ylabel(y_label)
        axs.set_zlabel(z_label)
        self.draw()

    def scatterplot2D(self, x_array, y_array, x_label, y_label, color, clear_option):
        if clear_option is True:
            self.figure.clear()
        axs = self.figure.add_subplot(111, position=[0.1, 0.1, 0.85, 0.85])
        axs.scatter(x_array, y_array, color=color, s=10)
        axs.set_xlabel(x_label)
        axs.set_ylabel(y_label)
        self.draw()

    def add_subplot(self, position, projection='2d'):
        if projection == '2d':
            axs = self.figure.add_subplot(position)
        elif projection == '3d':
            axs = self.figure.add_subplot(position, projection='3d')
        else:
            raise ValueError("Invalid projection type. Use '2d' or '3d'.")
        return axs

    def get_axis(self):
        return self.figure.gca()

    def clear(self):
        self.figure.clear()
        self.draw()