from scipy.interpolate import interp1d, splrep, splev
import numpy as np
from plot_canvas import MplCanvas3D2D


class PlotHandler:

    def __init__(self, plot_frame1: MplCanvas3D2D, plot_frame2: MplCanvas3D2D, plot_frame3: MplCanvas3D2D):
        self.plot_frame1 = plot_frame1
        self.plot_frame2 = plot_frame2
        self.plot_frame3 = plot_frame3

    def linear_fit_numpy2d(self, x_array, y_array):
        x_array = np.array(x_array)
        y_array = np.array(y_array)
        sorted_indices = np.argsort(x_array)
        sorted_x = x_array[sorted_indices]
        sorted_y = y_array[sorted_indices]
        x_line = np.linspace(min(x_array), max(x_array), 100)
        y_line = np.interp(x_line, sorted_x, sorted_y)
        return x_line, y_line

    def linear_fit_scipy2d(self, x_array, y_array):
        interpolator = interp1d(x_array, y_array, kind='linear')
        x_line = np.linspace(min(x_array), max(x_array), 100)
        y_line = interpolator(x_line)
        return x_line, y_line

    def manual_interpolation_linear(self, x_array, y_array):
        x_line = []
        y_line = []
        n = len(x_array)
        for i in range(n - 1):
            x0, y0 = x_array[i], y_array[i]
            x1, y1 = x_array[i + 1], y_array[i + 1]
            x_line.append(x0)
            y_line.append(y0)
            num_intermediate_points = 10
            for j in range(1, num_intermediate_points):
                t = j / num_intermediate_points
                x = x0 + t * (x1 - x0)
                y = y0 + t * (y1 - y0)
                x_line.append(x)
                y_line.append(y)
        x_line.append(x_array[-1])
        y_line.append(y_array[-1])
        return x_line, y_line

    def numpy_square_spline(self, x_array, y_array, num_points):
        n = len(x_array)
        A = []
        B = []
        for i in range(n - 1):
            x0, y0 = x_array[i], y_array[i]
            x1, y1 = x_array[i + 1], y_array[i + 1]
            row0 = [0] * (3 * i) + [x0 ** 2, x0, 1] + [0] * (3 * (n - i - 2))
            row1 = [0] * (3 * i) + [x1 ** 2, x1, 1] + [0] * (3 * (n - i - 2))
            A.append(row0)
            A.append(row1)
            B.append(y0)
            B.append(y1)
        for i in range(n - 2):
            x0 = x_array[i]
            row0 = [0] * (3 * i) + [2 * x0, 1, 0] + [-2 * x0, -1, 0] + [0] * (3 * (n - 3 - i))
            A.append(row0)
            B.append(0)
        row_last = [1, 0, 0] + [0] * (3 * (n - 2))
        A.append(row_last)
        B.append(0)
        x_spline = np.linspace(min(x_array), max(x_array), num_points)
        coeffs = np.linalg.solve(A, B)
        coeffs = coeffs.reshape((n-1), 3)
        y_spline = []
        for x in x_spline:
            for i in range(n-1):
                if x_array[i] <=x<= x_array[i+1]:
                    a, b, c = coeffs[i]
                    y_spline.append(a * x ** 2 + b * x + c)
                    break

        return x_spline, y_spline

    def scipy_square_spline(self, x_array, y_array):
        sqrt_spline = splrep(x_array, y_array, k=2)
        x_spline = np.linspace(min(x_array), max(x_array), 100)
        y_spline = splev(x_spline, sqrt_spline)
        return x_spline, y_spline

    def numpy_qubic_spline(self, x_array, y_array, num_points):
        n = len(x_array)
        A = []
        B = []

        for i in range(n - 1):
            x0, y0 = x_array[i], y_array[i]
            x1, y1 = x_array[i + 1], y_array[i + 1]
            row0 = [0] * (4 * i) + [x0 ** 3, x0 ** 2, x0, 1] + [0] * (4 * (n - 2 - i))
            row1 = [0] * (4 * i) + [x1 ** 3, x1 ** 2, x1, 1] + [0] * (4 * (n - 2 - i))
            A.append(row0)
            A.append(row1)
            B.append(y0)
            B.append(y1)

        for i in range(1, n - 1):
            x0 = x_array[i]
            row0 = [0] * (4 * (i - 1)) + [3 * x0 ** 2, 2 * x0, 1, 0, -3 * x0 ** 2, -2 * x0, -1, 0] + [0] * (
                    4 * (n - 2 - i))
            A.append(row0)
            B.append(0)

        for i in range(1, n - 1):
            x0 = x_array[i]
            row0 = [0] * (4 * (i - 1)) + [6 * x0, 2, 0, 0, -6 * x0, -2, 0, 0] + [0] * (4 * (n - 2 - i))
            A.append(row0)
            B.append(0)

        row_start = [6 * x_array[0], 2, 0, 0] + [0] * (4 * (n - 2))
        row_end = [0] * (4 * (n - 2)) + [6 * x_array[-1], 2, 0, 0]

        A.append(row_start)
        A.append(row_end)
        B.append(0)
        B.append(0)

        coeffs = np.linalg.solve(A, B)
        coeffs = coeffs.reshape((n - 1, 4))
        x_spline = np.linspace(min(x_array), max(x_array), num_points)
        y_spline = []
        for x in x_spline:
            for i in range(n - 1):
                if x_array[i] <= x <= x_array[i + 1]:
                    a, b, c, d = coeffs[i]
                    y_spline.append(a * x ** 3 + b * x ** 2 + c * x + d)
                    break

        return x_spline, y_spline

    def scipy_qubic_spline(self, x_array, y_array):
        qube_spline = splrep(x_array, y_array, k=3)
        x_spline = np.linspace(min(x_array), max(x_array), 100)
        y_spline = splev(x_spline, qube_spline)
        return x_spline, y_spline

    def manual_square_spline(self, x_array, y_array):
        n = len(x_array)
        A = []
        B = []
        for i in range(n - 1):
            x0, y0 = x_array[i], y_array[i]
            x1, y1 = x_array[i + 1], y_array[i + 1]
            row0 = [0] * (3 * i) + [x0 ** 2, x0, 1] + [0] * (3 * (n - i - 2))
            row1 = [0] * (3 * i) + [x1 ** 2, x1, 1] + [0] * (3 * (n - i - 2))
            A.append(row0)
            A.append(row1)
            B.append(y0)
            B.append(y1)
        for i in range(n - 2):
            x0 = x_array[i]
            row0 = [0] * (3 * i) + [2 * x0, 1, 0] + [-2 * x0, -1, 0] + [0] * (3 * (n - 3 - i))
            A.append(row0)
            B.append(0)
        row_last = [1, 0, 0] + [0] * (3 * (n - 2))
        A.append(row_last)
        B.append(0)
        x = self.gaussian_elimination(A, B)
        return x

    def manual_qubic_spline(self, x_array, y_array):
        n = len(x_array)
        A = []
        B = []
        for i in range(n - 1):
            x0, y0 = x_array[i], y_array[i]
            x1, y1 = x_array[i + 1], y_array[i + 1]
            row0 = [0] * (4 * i) + [x0 ** 3, x0 ** 2, x0, 1] + [0] * (4 * (n - 2 - i))
            row1 = [0] * (4 * i) + [x1 ** 3, x1 ** 2, x1, 1] + [0] * (4 * (n - 2 - i))
            A.append(row0)
            A.append(row1)
            B.append(y0)
            B.append(y1)
        for i in range(1, n - 1):
            x0 = x_array[i]
            row0 = [0] * (4 * (i - 1)) + [3 * x0 ** 2, 2 * x0, 1, 0, -3 * x0 ** 2, -2 * x0, -1, 0] + [0] * (
                        4 * (n - 2 - i))
            A.append(row0)
            B.append(0)
        for i in range(1, n - 1):
            x0 = x_array[i]
            row0 = [0] * (4 * (i - 1)) + [6 * x0, 2, 0, 0, -6 * x0, -2, 0, 0] + [0] * (4 * (n - 2 - i))
            A.append(row0)
            B.append(0)
        row_start = [6 * x_array[0], 2, 0, 0] + [0] * (4 * (n - 2))
        row_end = [0] * (4 * (n - 2)) + [6 * x_array[-1], 2, 0, 0]
        A.append(row_start)
        A.append(row_end)
        B.append(0)
        B.append(0)
        x = self.gaussian_elimination(A, B)
        return x

    def gaussian_elimination(self, A, B):
        n = len(A)
        for i in range(n):
            max_index = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_index][i]):
                    max_index = k
            A[i], A[max_index] = A[max_index], A[i]
            B[i], B[max_index] = B[max_index], B[i]
            shift = A[i][i]
            if abs(shift) < 1e-10:
                shift = 1e-10
            for k in range(i + 1, n):
                param = A[k][i] / shift
                for j in range(i, n):
                    A[k][j] -= param * A[i][j]
                B[k] -= param * B[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = B[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]

        return x
