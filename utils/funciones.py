import tempfile
import cmath
import mpmath
import math
import numpy as np
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
import streamlit as st
import time
import math
import tempfile
import numpy as np
from tqdm import tqdm

# Diccionario de funciones disponibles para el fractal de Mandelbrot
function_dict = {
    "Fractal de Mandelbrot del tipo z = z^m + c": lambda z, c, m: z**m + c,
    "Fractal de Mandelbrot del tipo z =  z^m + 1/c": lambda z, c, m: z**m + 1 / c,
    "Fractal de Mandelbrot del tipo z = cos(z^m) + 1/c": lambda z, c, m: mpmath.cos(
        z**m
    )
    + 1 / c,
    "Fractal de Mandelbrot del tipo z = sin(z^m) + 1/c": lambda z, c, m: mpmath.sin(
        z**m
    )
    + 1 / c,
    "Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / sqrt(c^3)]": lambda z, c, m: mpmath.exp(
        (z**m - 1.00001 * z) / cmath.sqrt(c**3)
    ),
    "Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / c^3]": lambda z, c, m: mpmath.exp(
        (z**m - 1.00001 * z) / c**3
    ),
    "Fractal de Mandelbrot del tipo z = cos(z^m/c^m)": lambda z, c, m: mpmath.cos(
        z**m / c**m
    ),
    "Fractal de Mandelbrot del tipo z = exp(z^m/c^m)": lambda z, c, m: mpmath.exp(
        z**m / c**m
    ),
    "Fractal de Mandelbrot del tipo z = exp(c^m/z^m)": lambda z, c, m: mpmath.exp(
        c**m / z**m
    ),
    "Fractal de Mandelbrot del tipo z = exp(z/c^m) + 1/c": lambda z, c, m: mpmath.exp(
        z / c**m
    ),
    "Fractal de Mandelbrot del tipo z = cosh(z^m/c^m)": lambda z, c, m: mpmath.cosh(
        z**m / c**m
    ),
}


@st.cache_data()
def st_plot_mandelbrot(n, k, Xr, Yr, color, selected_func, m):
    """
    Generates and displays a plot of the Mandelbrot set using the Matplotlib library.

    Args:
        n: Number of points in each dimension of the plot.
        k: Maximum number of iterations.
        Xr: Range of values for the x-axis [xmin, xmax].
        Yr: Range of values for the y-axis [ymin, ymax].
        color: Color map to use in the plot.
        selected_func: Name of the selected function.
        m: Power of z.

    Returns:
        BytesIO: Image file in PNG format.
    """
    start_time = time.time()  # Start execution time measurement

    # Get the name of the selected function
    name_selected_func = function_dict[selected_func]

    # Generate x and y coordinates
    x = np.linspace(Xr[0], Xr[1], n)
    y = np.linspace(Yr[0], Yr[1], n)
    X, Y = np.meshgrid(x, y)

    # Initialize the Mandelbrot set value matrix
    W = np.zeros((len(X), len(Y)))

    # Progress bar
    progress_bar = st.progress(0)

    # Define the function to calculate the Mandelbrot value for a single point
    def calculate_mandelbrot(i, j):
        c = X[i, j] + Y[i, j] * 1j
        z = 0
        func = function_dict[selected_func]
        for _ in range(k):
            z = func(z, c, m)
            if abs(z) > 2:
                break
        return _

    # Parallelize the computation of the Mandelbrot set
    num_cores = -1  # Adjust the number of cores to use (-1 uses all)
    results = Parallel(n_jobs=num_cores)(
        delayed(calculate_mandelbrot)(i, j)
        for i in range(len(X))
        for j in range(len(Y))
    )

    # Store the results in the W matrix
    for i in range(len(X)):
        for j in range(len(Y)):
            W[i, j] = results[i * len(Y) + j]

        # Update progress bar
        progress_bar.progress(i / len(X))  # ! Arreglar la barra de progreso

    # Create a figure and display the Mandelbrot set image
    fig, ax = plt.subplots()
    ax.imshow(
        W,
        extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
        cmap=color,
        interpolation="bilinear",
        aspect="equal",
    )

    # Set the plot title with the selected parameters and function
    ax.set_title(f"{selected_func}, m={m}, n={n}, k={k}", fontsize=9)
    # Set the font size of x and y axis labels
    ax.tick_params(axis="both", labelsize=8)

    # Display the plot in the Streamlit interface
    st.pyplot(fig)

    # Generate the filename based on the input data and the selected function
    filename = f"img/{selected_func}_m{m}_n{n}_k{k}.png"

    # Save the figure to a temporary file in PNG format
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png", dpi=300)
        tmpfile.seek(0)  # Reset the file pointer to the beginning
        img_bytes = tmpfile.read()

    end_time = time.time()  # End execution time measurement
    execution_time = end_time - start_time
    print(f"Execution time: {round(execution_time, 2)} seconds")
    # Convert execution time to minutes and seconds
    minutes = math.floor(execution_time / 60)
    seconds = execution_time % 60

    # Format the time in minutes and seconds
    time_str = (
        f"{minutes} minutes and {round(seconds, 2)} seconds"
        if minutes > 0
        else f"{round(seconds, 2)} seconds"
    )
    print(f"Execution time: {time_str}")

    # Return the image bytes and the filename
    return img_bytes, filename, execution_time


funct_dict = {
    "Fractal de Julia del tipo z^m + c": lambda z, c, m: z**m + c,
    "Fractal de Julia del tipo z^m + 1/c": lambda z, c, m: z**m + 1 / c,
    # ! FALTA AÑADIR MÁS ECUACIONES
    "Fractal de Julia del tipo z = Exp(z^m/c^m)": lambda z, c, m: mpmath.exp(
        z**m / c**m
    ),
}
#! INTENTAR HACER UNA FORMA DE QUE EL USUARIO AÑADA SU ECUACIÓN


@st.cache_data()
def st_plot_julia(n, c_real, c_imag, k, Xr, Yr, color, selected_funct, m_j):
    """
    Generates and displays a plot of the Julia set using the Matplotlib library.

    Args:
        n: Number of points in each dimension of the plot.
        c_real: Real part of the parameter c in the equation z = z^2 + c.
        c_imag: Imaginary part of the parameter c in the equation z = z^2 + c.
        k: Maximum number of iterations.
        Xr: Range of values for the x-axis [xmin, xmax].
        Yr: Range of values for the y-axis [ymin, ymax].
        color: Color map to use in the plot.
        selected_funct: Name of the selected function.
        m_j: Power of z.

    Returns:
        BytesIO: Image file in PNG format.
    """
    start_time_j = time.time()  # Start execution time measurement

    # Get the name of the selected function
    name_selected_funct = funct_dict[selected_funct]

    c = complex(c_real, c_imag)
    x = np.linspace(Xr[0], Xr[1], n)
    y = np.linspace(Yr[0], Yr[1], int(n * (Yr[1] - Yr[0]) / (Xr[1] - Xr[0])))
    X, Y = np.meshgrid(x, y)
    W = np.zeros((len(X), len(Y)))

    # Create an empty progress bar object
    progress_bar_j = st.progress(0)

    # Define the function to calculate the Julia set value for a single point
    def calculate_julia(m, j):
        """
        Calcula la pertenencia de un punto al conjunto de Julia y devuelve el resultado.

        Args:
            m: Índice de fila del punto en la matriz.
            j: Índice de columna del punto en la matriz.

        Returns:
            Número de iteraciones realizadas antes de determinar la pertenencia.
        """
        z = X[m, j] + Y[m, j] * 1j
        R = max(abs(c), 2)
        i = 0
        funct = funct_dict[selected_funct]
        while i < k:
            if abs(z) > R:
                break
            z = funct(z, c, m_j)

            i += 1
        return i

    # Paraleliza el cálculo del conjunto de Julia
    num_cores = -1  # Ajusta el número de núcleos a utilizar (-1 utiliza todos)
    results = Parallel(n_jobs=num_cores)(
        delayed(calculate_julia)(m, j)
        for m in range(X.shape[0])
        for j in range(Y.shape[0])
    )

    # Almacena los resultados en la matriz W
    for m in range(X.shape[0]):
        for j in range(Y.shape[0]):
            W[m, j] = results[m * Y.shape[0] + j]

        # Actualiza la barra de progreso
        # Incrementa el progreso en 1 y divide por el total
        progress_bar_j.progress((m + 1) / X.shape[0])

    # Crea una figura y muestra la imagen del conjunto de Julia
    fig = plt.figure()
    plt.imshow(
        W,
        extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
        cmap=color,
        interpolation="bilinear",
        import matplotlib.pyplot as plt
        def Julia_plot(n, c, k, Xr=(-2, 2), Yr=(-2, 2)):
            """
            Función para generar y guardar un gráfico del conjunto de Julia.

            Args:
                n: Número de puntos en cada dimensión del gráfico.
                c: Parámetro constante para el conjunto de Julia.
                k: Número máximo de iteraciones para determinar la pertenencia de un punto al conjunto.
                Xr: Rango del eje x (valores mínimo y máximo).
                Yr: Rango del eje y (valores mínimo y máximo).

            Returns:
                None
            """
            x = np.linspace(Xr[0], Xr[1], n)
            y = np.linspace(Yr[0], Yr[1], n)
            X, Y = np.meshgrid(x, y)
            W = np.zeros((len(X), len(Y)))

            # Create a progress bar
            progress_bar = tqdm(total=n*n, desc="Calculating", unit="point")

            # Calcular el valor de pertenencia para cada punto del gráfico
            for m in range(X.shape[0]):
                for j in range(Y.shape[1]):
                    w, iter = Julia(X[m, j] + Y[m, j] * 1j, c, k)
                    W[m, j] += iter

                    # Update the progress bar
                    progress_bar.update()

            # Close the progress bar
            progress_bar.close()

            # Rest of the code...
            # ...
            # ...
