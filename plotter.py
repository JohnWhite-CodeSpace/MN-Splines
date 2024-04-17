from scipy.interpolate import interp1d, splrep, splev

import numpy as np

from plot_canvas import MplCanvas3D2D


class PlotHandler:

    def __init__(self, plot_frame1: MplCanvas3D2D, plot_frame2: MplCanvas3D2D, plot_frame3: MplCanvas3D2D):
        self.plot_frame1 = plot_frame1
        self.plot_frame2 = plot_frame2
        self.plot_frame3 = plot_frame3

    def linear_fit_numpy2d(self, x_array, y_array):
        print("Inside linear_fit_numpy2d")
        print("x_array:", x_array)
        print("y_array:", y_array)
        x_array = np.array(x_array)
        y_array = np.array(y_array)
        sorted_indices = np.argsort(x_array)
        sorted_x = x_array[sorted_indices]
        sorted_y = y_array[sorted_indices]
        x_line = np.linspace(min(x_array), max(x_array), 100)
        y_line = np.interp(x_line, sorted_x, sorted_y)
        return x_line, y_line

    def linear_fit_scipy2d(self, x_array, y_array):
        print("Inside linear_fit_scipy2d")
        print("x_array:", x_array)
        print("y_array:", y_array)
        interpolator = interp1d(x_array, y_array, kind='linear')
        x_line = np.linspace(min(x_array), max(x_array), 100)
        y_line = interpolator(x_line)
        return x_line, y_line

    def manual_interpolation_linear(self, x_array, y_array):
        x_line = []
        y_line = []
        n = len(x_array)
        if n != len(y_array):
            print("shit")
        else:
            for i in range(n - 1):
                x = (x_array[i + 1] + x_array[i]) / 2
                delta_x = x_array[i + 1] - x_array[i]
                delta_y = y_array[i + 1] - y_array[i]

                line_slope = delta_y / delta_x

                inter_y = y_array[i] + line_slope * (x - x_array[i])
                x_line.append(x)
                y_line.append(inter_y)
            print(x_line)
            print(y_line)
        return x_line, y_line

    def numpy_square_spline(self, x_array, y_array, num_points):
        # dafuq - this numpy quad spline still doesnt work as intended
        sorted_indices = np.argsort(x_array)
        sorted_x = np.take(x_array, sorted_indices)
        sorted_y = np.take(y_array, sorted_indices)
        x_spline = np.array([])
        y_spline = np.array([])
        for i in range(len(sorted_x) - 1):
            x0, x1 = sorted_x[i], sorted_x[i + 1]
            y0, y1 = sorted_y[i], sorted_y[i + 1]

            coeffs = np.polyfit([x0, (x0 + x1) / 2, x1], [y0, y0, y1], 2)
            polynomial = np.poly1d(coeffs)

            x_part = np.linspace(x0, x1, num_points)
            y_part = polynomial(x_part)

            x_spline = np.concatenate((x_spline, x_part))
            y_spline = np.concatenate((y_spline, y_part))

        return x_spline, y_spline

    def scipy_square_spline(self, x_array, y_array):
        sqrt_spline = splrep(x_array, y_array, k=2)
        x_spline = np.linspace(min(x_array), max(x_array), 100)
        y_spline = splev(x_spline, sqrt_spline)
        return x_spline, y_spline

    def manual_square_spline(self, x_array, y_array):
        n = len(x_array)
        A = []
        B = []
        x_spline = []
        y_spline = []
        # adding quadratic function equality in the edge points of each x range
        for i in range(n - 1):
            x0, y0 = x_array[i], y_array[i]
            x1, y1 = x_array[i + 1], y_array[i + 1]
            #quad function coeffs
            row0 = [0] * (3 * i) + [x0 ** 2, x0, 1] + [0] * (3 * (n - i - 2))
            row1 = [0] * (3 * i) + [x1 ** 2, x1, 1] + [0] * (3 * (n - i - 2))
            A.append(row0)
            A.append(row1)
            B.append(y0)
            B.append(y1)

        # Adding first derivatives equality condition to the A and B matrices
        for i in range(n - 2):
            x0 = x_array[i]
            # first derivative coeffs
            row0 = [0] * (3 * i) + [2 * x0, 1, 0] + [-2 * x0, -1, 0] + [0] * (3 * (n - 3 - i))
            A.append(row0)
            B.append(0)
        # secind derivative condition for the first point(x1,y1)
        row_last = [1, 0, 0] + [0] * (3 * (n - 2))
        A.append(row_last)
        B.append(0)
        x = self.gaussian_elimination(A,B)
        return x

    def gaussian_elimination(self, A, B):
        # n=number of rows of the A matrix
        n = len(A)
        for i in range(n):
            # Swapping rows so that the diagonal elements are the largest value in the column
            max_index = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_index][i]):
                    max_index = k
            A[i], A[max_index] = A[max_index], A[i]
            B[i], B[max_index] = B[max_index], B[i]
            shift = A[i][i]
            if abs(shift) < 1e-10:
                shift = 1e-10
            # elimination algorithm
            for k in range(i + 1, n):
                param = A[k][i] / shift
                for j in range(i, n):
                    A[k][j] -= param * A[i][j]
                B[k] -= param * B[i]
        # transfering augmentd matrix into an upper triangular one.
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = B[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        return x
