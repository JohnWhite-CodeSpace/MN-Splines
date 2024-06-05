from scipy.interpolate import interp1d, splrep, splev
import numpy as np
from plot_canvas import MplCanvas3D2D


class PlotHandler:
    """
    A class which handles interpolation algorithms for each of three plots.
    For the first plot all interpolation methods have been created without using external libraries such as "scipy" or
    "numpy".
    """
    def __init__(self, plot_frame1: MplCanvas3D2D, plot_frame2: MplCanvas3D2D, plot_frame3: MplCanvas3D2D):
        """
        Initialises PlotHandler object and sets the MplCanvas3D2D objects.
        :param plot_frame1:
        :param plot_frame2:
        :param plot_frame3:
        """
        self.plot_frame1 = plot_frame1
        self.plot_frame2 = plot_frame2
        self.plot_frame3 = plot_frame3

    def linear_fit_numpy2d(self, x_array, y_array):
        """
        Linear interpolation method using methods offered by the numpy library
        :param x_array: Array with x values of data loaded from spreadsheet
        :param y_array: Array with y values of data loaded from spreadsheet
        :return: x_line, y_line - Arrays with interpolated x and y values for later plotting
        """
        x_array = np.array(x_array)
        y_array = np.array(y_array)
        sorted_indices = np.argsort(x_array)
        sorted_x = x_array[sorted_indices]
        sorted_y = y_array[sorted_indices]
        x_line = np.linspace(min(x_array), max(x_array), 100)
        y_line = np.interp(x_line, sorted_x, sorted_y)
        return x_line, y_line

    def linear_fit_scipy2d(self, x_array, y_array):
        """
        Linear interpolation method using methods offered by the scipy library
        :param x_array: Array with x values of data loaded from spreadsheet
        :param y_array: Array with y values of data loaded from spreadsheet
        :return: x_line, y_line - Arrays with interpolated x and y values for later plotting
        """
        interpolator = interp1d(x_array, y_array, kind='linear')
        x_line = np.linspace(min(x_array), max(x_array), 100)
        y_line = interpolator(x_line)
        return x_line, y_line

    def manual_interpolation_linear2d(self, x_array, y_array):
        """
        My implementation of the linear interpolation without using any external methods.
        This linear interpolation uses calculation fo the intermediate points for generating interpolated x and y values.
        :param x_array: Array with x values of data loaded from spreadsheet.
        :param y_array: Array with y values of data loaded from spreadsheet.
        :return: x_line, y_line - Arrays with interpolated x and y values for later plotting.
        """
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

    def numpy_square_spline2d(self, x_array, y_array, num_points):
        """
        Square spline interpolation method using method for performing calculations on matrices. the rest of
        this algorithm was written based on the dr. Piotr Fronczak's 5th lecture of the Numerical Methods classes:

        Conditions for creating a square spline:
            1. **Interpolation Conditions:**
                - Each quadratic polynomial P_i(x) = a_i x^2 + b_i x + c_i must pass through the endpoints (x_i, y_i) and (x_{i+1}, y_{i+1}).

            2. **Smoothness Conditions:**
               - The first derivatives of the polynomials must match at the internal points x_i:
                 2a_i x_i + b_i = 2a_{i+1} x_i + b_{i+1} for i = 1, 2, ..., n-2.

            3. **Boundary Condition:**
               - The second derivative at the first point is set to zero: a_0 = 0.

        :param x_array: Array with x values of data loaded from spreadsheet
        :param y_array: Array with y values of data loaded from spreadsheet
        :return: x_line, y_line - Arrays with interpolated x and y values for later plotting
        """
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

    def scipy_square_spline2d(self, x_array, y_array):
        """
        Square spline interpolation method using methods offered by the scipy library.
        :param x_array:
        :param y_array:
        :return: x_spline y_spline
        """
        sqrt_spline = splrep(x_array, y_array, k=2)
        x_spline = np.linspace(min(x_array), max(x_array), 100)
        y_spline = splev(x_spline, sqrt_spline)
        return x_spline, y_spline

    def numpy_qubic_spline2d(self, x_array, y_array, num_points):
        """
        Cubic spline interpolation method using numpy method for performing calculations on matrices. the rest of
        this algorithm was written based on the dr. Piotr Fronczak's 5th lecture of the Numerical Methods classes:
        Conditions for creating a square spline:
            1. **Interpolation Conditions:**
                - Each quadratic polynomial P_i(x) = a_i x^2 + b_i x + c_i must pass through the endpoints (x_i, y_i) and (x_{i+1}, y_{i+1}).

            2. **Smoothness Conditions:**
               - The first derivatives of the polynomials must match at the internal points x_i:
                 2a_i x_i + b_i = 2a_{i+1} x_i + b_{i+1} for i = 1, 2, ..., n-2.

            3. **Boundary Condition:**
               - The second derivative at the first point is set to zero: a_0 = 0.
        :param x_array:
        :param y_array:
        :param num_points:
        :return: x_spline y_spline
        """
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

    def scipy_qubic_spline2d(self, x_array, y_array):
        """
        Cubic spline interpolation method using methods offered by the scipy library.
        :param x_array:
        :param y_array:
        :return: x_spline y_spline
        """
        qube_spline = splrep(x_array, y_array, k=3)
        x_spline = np.linspace(min(x_array), max(x_array), 100)
        y_spline = splev(x_spline, qube_spline)
        return x_spline, y_spline

    def manual_square_spline2d(self, x_array, y_array):
        """
            Manually implemented method for square spline interpolation based on the algorithm described in Dr. Piotr
            Fronczak's 5th lecture of Numerical Methods classes.

            Conditions for creating a square spline:
            1. **Interpolation Conditions:**
               - Each quadratic polynomial P_i(x) = a_i x^2 + b_i x + c_i must pass through the endpoints (x_i, y_i) and (x_{i+1}, y_{i+1}).

            2. **Smoothness Conditions:**
               - The first derivatives of the polynomials must match at the internal points x_i:
                 2a_i x_i + b_i = 2a_{i+1} x_i + b_{i+1} for i = 1, 2, ..., n-2.

            3. **Boundary Condition:**
               - The second derivative at the first point is set to zero: a_0 = 0.

            The method constructs and solves a system of linear equations to determine the coefficients of the quadratic polynomials.

            :param x_array: List of x-coordinates of the data points.
            :param y_array: List of y-coordinates of the data points.
            :return: List of coefficients for the quadratic polynomials, such that for each segment i, the coefficients
                     [a_i, b_i, c_i] are in consecutive positions in the returned list.
        """
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

    def manual_qubic_spline2d(self, x_array, y_array):
        """
        Manually implemented method for cubic spline interpolation based on the algorithm described in Dr. Piotr
        Fronczak's lectures on Numerical Methods.
        Conditions for creating a cubic spline:
        1. **Interpolation Conditions:**
           - Each cubic polynomial P_i(x) = a_i x^3 + b_i x^2 + c_i x + d_i must pass through the endpoints (x_i, y_i) and (x_{i+1}, y_{i+1}).

        2. **Smoothness Conditions:**
           - The first derivatives of the polynomials must match at the internal points x_i:
             3a_i x_i^2 + 2b_i x_i + c_i = 3a_{i+1} x_i^2 + 2b_{i+1} x_i + c_{i+1} for i = 1, 2, ..., n-2.
           - The second derivatives of the polynomials must also match at the internal points x_i:
             6a_i x_i + 2b_i = 6a_{i+1} x_i + 2b_{i+1} for i = 1, 2, ..., n-2.

        3. **Boundary Conditions:**
           - The second derivative at the first and last points are set to zero: 6a_0 x_0 + 2b_0 = 0 and 6a_{n-2} x_{n-1} + 2b_{n-2} = 0.
        The method constructs and solves a system of linear equations to determine the coefficients of the cubic polynomials.
        :param x_array: List of x-coordinates of the data points.
        :param y_array: List of y-coordinates of the data points.
        :return: List of coefficients for the cubic polynomials, such that for each segment i, the coefficients
                 [a_i, b_i, c_i, d_i] are in consecutive positions in the returned list.
        """
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
        """
           Solves the system of linear equations Ax = B using Gaussian elimination.

           The method performs partial pivoting to improve numerical stability (value less than 1e-10 can cause
           computational problems like division by 0), and then applies forward elimination to transform the matrix A
           into an upper triangular form. Back substitution is used to solve for the vector x.

           :param A: Coefficient matrix of the system.
           :param B: Right-hand side vector.
           :return: Solution vector x.
        """
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
