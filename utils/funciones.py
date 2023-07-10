import tempfile
import cmath
import mpmath
import math
import numpy as np
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
import streamlit as st

# Diccionario de funciones disponibles para el fractal de Mandelbrot
function_dict = {
    'Fractal de Mandelbrot del tipo z = z^m + c': lambda z, c, m: z ** m + c,
    'Fractal de Mandelbrot del tipo z =  z^m + 1/c': lambda z, c, m: z ** m + 1/c,
    'Fractal de Mandelbrot del tipo z = cos(z^m) + 1/c': lambda z, c, m: mpmath.cos(z**m) + 1/c,
    'Fractal de Mandelbrot del tipo z = sin(z^m) + 1/c': lambda z, c, m: mpmath.sin(z**m) + 1/c,
    'Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / sqrt(c^3)]': lambda z, c, m: mpmath.exp((z**m - 1.00001 * z) / cmath.sqrt(c**3)),
    'Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / c^3]': lambda z, c, m: mpmath.exp((z**m - 1.00001 * z) / c**3),
    'Fractal de Mandelbrot del tipo z = cos(z^m/c^m)': lambda z, c, m: mpmath.cos(z**m/c**m),
    'Fractal de Mandelbrot del tipo z = exp(z^m/c^m)': lambda z, c, m: mpmath.exp(z ** m / c ** m),
    'Fractal de Mandelbrot del tipo z = exp(c^m/z^m)': lambda z, c, m: mpmath.exp(c ** m / z ** m),
    'Fractal de Mandelbrot del tipo z = exp(z/c^m) + 1/c': lambda z, c, m: mpmath.exp(z / c ** m),
    'Fractal de Mandelbrot del tipo z = cosh(z^m/c^m)': lambda z, c, m: mpmath.cosh(z ** m / c**m),
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
    results = Parallel(n_jobs=num_cores)(delayed(calculate_mandelbrot)(
        i, j) for i in range(len(X)) for j in range(len(Y)))

    # Store the results in the W matrix
    for i in range(len(X)):
        for j in range(len(Y)):
            W[i, j] = results[i * len(Y) + j]

        # Update progress bar
        progress_bar.progress(i / len(X))  # ! Arreglar la barra de progreso

    # Create a figure and display the Mandelbrot set image
    fig, ax = plt.subplots()
    ax.imshow(W, extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
              cmap=color, interpolation='bilinear', aspect="equal")

    # Set the plot title with the selected parameters and function
    ax.set_title(f"{selected_func}, m={m}, n={n}, k={k}", fontsize=9)
    # Set the font size of x and y axis labels
    ax.tick_params(axis='both', labelsize=8)

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
    time_str = f"{minutes} minutes and {round(seconds, 2)} seconds" if minutes > 0 else f"{round(seconds, 2)} seconds"
    print(f"Execution time: {time_str}")

    # Return the image bytes and the filename
    return img_bytes, filename, execution_time


funct_dict = {
    'Fractal de Julia del tipo z^m + c': lambda z, c, m: z ** m + c,
    'Fractal de Julia del tipo z^m + 1/c': lambda z, c, m: z ** m + 1/c,
    # ! FALTA AÑADIR MÁS ECUACIONES
    'Fractal de Julia del tipo z = Exp(z^m/c^m)': lambda z, c, m: mpmath.exp(z ** m / c ** m),
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

    # Parallelize the computation of the Julia set
    num_cores = -1  # Adjust the number of cores to use (-1 uses all)
    results = Parallel(n_jobs=num_cores)(delayed(calculate_julia)(
        m, j) for m in range(X.shape[0]) for j in range(Y.shape[0]))

    # Store the results in the W matrix
    for m in range(X.shape[0]):
        for j in range(Y.shape[0]):
            W[m, j] = results[m * Y.shape[0] + j]

        # Update progress bar
        # Increment the progress by 1 and divide by total
        progress_bar_j.progress((m + 1) / X.shape[0])

    # Create a figure and display the Julia set image
    fig = plt.figure()
    plt.imshow(W, extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
               cmap=color, interpolation='bilinear', aspect="equal")

    # Set the plot title with the selected parameters
    plt.title(
        f"Julia Set ({selected_funct}, m={m_j}, c={c}, n={n}, k={k})", fontsize=9)

    # Set the font size of x and y axis labels
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # Display the plot in the Streamlit interface
    st.pyplot(fig)

    # Generate the filename based on the input data and the selected function
    filename_j = f"img/julia_{selected_funct}_m{m_j}_c{c}_n{n}_k{k}.png"

    # Save the figure to a temporary file in PNG format
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png", dpi=300)
        tmpfile.seek(0)  # Reset the file pointer to the beginning
        img_bytes = tmpfile.read()

    end_time = time.time()  # End execution time measurement
    execution_time_j = end_time - start_time_j

    # Convert execution time to minutes and seconds
    minutes_j = math.floor(execution_time_j / 60)
    seconds_j = execution_time_j % 60

    # Format the time in minutes and seconds
    time_str = f"{minutes_j} minutes and {round(seconds_j, 2)} seconds" if minutes_j > 0 else f"{round(seconds_j, 2)} seconds"
    print(f"Execution time: {time_str}")

    # Return the image bytes and the filename
    return img_bytes, filename_j, execution_time_j

# def plot_mandelbrot(n, k, Xr, Yr):
#     """
#     Genera y muestra un gráfico del conjunto de Mandelbrot utilizando la biblioteca Matplotlib.

#     Args:
#         n: Número de puntos en cada dimensión del gráfico.
#         k: Número máximo de iteraciones.
#         Xr: Rango de valores del eje x [xmin, xmax].
#         Yr: Rango de valores del eje y [ymin, ymax].

#     Returns:
#         None
#     """
#     x = np.linspace(Xr[0], Xr[1], n)
#     y = np.linspace(Yr[0], Yr[1], n)
#     X, Y = np.meshgrid(x, y)
#     W = np.zeros((len(X), len(Y)))

#     for m in range(X.shape[0]):
#         for j in range(Y.shape[1]):
#             w, iter = Mandelbrot(X[m, j] + Y[m, j] * 1j, k)
#             W[m, j] += iter

#     # Establecer el título de la gráfica con los parámetros
#     plt.title(f"Conjunto de Mandelbrot (n={n}, k={k})")

#     plt.imshow(W, extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
#                cmap='hot', interpolation='bilinear')

#     # Generar el nombre del archivo basado en los datos de entrada
#     filename = f"img/mandelbrot_n{n}_k{k}_x{Xr[0]}_{Xr[1]}_y{Yr[0]}_{Yr[1]}.png"
#     # Guardar la figura en un archivo PNG
#     plt.savefig(filename)

#     plt.show()


# def Julia_plot(n, c, k, Xr=(-2, 2), Yr=(-2, 2)):
#     """
#     Función para generar y guardar un gráfico del conjunto de Julia.

#     Args:
#         n: Número de puntos en cada dimensión del gráfico.
#         c: Parámetro constante para el conjunto de Julia.
#         k: Número máximo de iteraciones para determinar la pertenencia de un punto al conjunto.
#         Xr: Rango del eje x (valores mínimo y máximo).
#         Yr: Rango del eje y (valores mínimo y máximo).

#     Returns:
#         None
#     """
#     x = np.linspace(Xr[0], Xr[1], n)
#     y = np.linspace(Yr[0], Yr[1], n)
#     X, Y = np.meshgrid(x, y)
#     W = np.zeros((len(X), len(Y)))

#     # Calcular el valor de pertenencia para cada punto del gráfico
#     for m in range(X.shape[1]):
#         for j in range(Y.shape[1]):
#             w, iter = Julia(X[m, j] + Y[m, j] * 1j, c, k)
#             W[m, j] += iter

#     # Crear el gráfico de Heatmap con Plotly
#     fig = go.Figure(data=go.Heatmap(x=x, y=y, z=W))
#     fig.update_layout(
#         title=f"Julia Set (c={c}, n={n}, k={k})",
#         xaxis_title="Real",
#         yaxis_title="Imaginary",
#         width=800,
#         height=600
#     )

#     # Ajustar el rango de ejes al centro del gráfico
#     fig.update_xaxes(range=[Xr[0], Xr[1]], constrain="domain")
#     fig.update_yaxes(range=[Yr[0], Yr[1]], constrain="domain")

#     # Generar el nombre del archivo basado en los datos de entrada
#     filename = f"img/julia_{n}_{c}_{k}_{Xr[0]}_{Xr[1]}_{Yr[0]}_{Yr[1]}.html"
#     # Guardar la figura en un archivo HTML
#     pio.write_html(fig, filename)

#     # Mostrar el gráfico
#     fig.show()


# def Mandelbrot_3D(n, k, Xr=(-2, 2), Yr=(-2, 2)):
#     """
#     Función para generar y guardar un gráfico en 3D del conjunto de Mandelbrot.

#     Args:
#         n: Número de puntos en cada dimensión del gráfico.
#         k: Número máximo de iteraciones para determinar la pertenencia de un punto al conjunto.
#         Xr: Rango del eje x (valores mínimo y máximo).
#         Yr: Rango del eje y (valores mínimo y máximo).

#     Returns:
#         None
#     """
#     x = np.linspace(Xr[0], Xr[1], n)
#     y = np.linspace(Yr[0], Yr[1], n)
#     X, Y = np.meshgrid(x, y)
#     Z = np.zeros((len(X), len(Y)))

#     # Calcular el valor de pertenencia para cada punto del gráfico
#     for m in range(X.shape[1]):
#         for j in range(Y.shape[1]):
#             w, iter = Mandelbrot(X[m, j] + Y[m, j] * 1j, k)
#             Z[m, j] += iter

#     # Crear el gráfico 3D con Plotly
#     fig = go.Figure(data=[go.Surface(x=x, y=y, z=Z)])
#     fig.update_layout(
#         title=f"Mandelbrot Set - 3D (n={n}, k={k})",
#         scene=dict(
#             xaxis_title="Real",
#             yaxis_title="Imaginary",
#             zaxis_title="Iterations"
#         )
#     )

#     # Generar el nombre del archivo basado en los datos de entrada
#     filename = f"img/mandelbrot_3d_{n}_{k}_{Xr[0]}_{Xr[1]}_{Yr[0]}_{Yr[1]}.html"
#     # Guardar la figura en un archivo HTML
#     pio.write_html(fig, filename)

#     # Mostrar el gráfico
#     fig.show()

# def Mandelbrot(c, m):
#     """
#     Calcula la pertenencia de un punto al conjunto de Mandelbrot y devuelve el resultado.

#     Args:
#         c: Valor complejo a evaluar.
#         m: Número máximo de iteraciones.

#     Returns:
#         Tuple (pertenece, iteraciones):
#             - pertenece: Booleano que indica si el punto pertenece al conjunto de Mandelbrot.
#             - iteraciones: Número de iteraciones realizadas antes de determinar la pertenencia.
#     """
#     k = 0
#     z = c
#     while k < m:
#         if abs(z) > 2:
#             return 1, k
#         z = z**2 + c
#         k += 1
#     return 0, k


# def plot_julia(n, c, k, Xr, Yr):
#     """
#     Genera y muestra un gráfico del conjunto de Julia utilizando la biblioteca Matplotlib.

#     Args:
#         n: Número de puntos en cada dimensión del gráfico.
#         c: Parámetro en la ecuación z = z^2 + c.
#         k: Número máximo de iteraciones.
#         Xr: Rango de valores del eje x [xmin, xmax].
#         Yr: Rango de valores del eje y [ymin, ymax].

#     Returns:
#         None
#     """
#     x = np.linspace(Xr[0], Xr[1], n)
#     y = np.linspace(Yr[0], Yr[1], int(n*(Yr[1]-Yr[0])/(Xr[1]-Xr[0])))
#     X, Y = np.meshgrid(x, y)
#     W = np.zeros((len(X), len(Y)))

#     for m in range(X.shape[1]):
#         for j in range(Y.shape[1]):
#             w, iter = Julia(X[m, j] + Y[m, j] * 1j, c, k)
#             W[m, j] += iter

#     # Establecer el título de la gráfica con los parámetros
#     plt.title(f"Conjunto de Julia (c={c}, n={n},k={k})")

#     plt.imshow(W, extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
#                cmap='hot', interpolation='bilinear')

#     # Generar el nombre del archivo basado en los datos de entrada
#     filename = f"img/julia_n{n}_c{c.real}_{c.imag}_k{k}_x{Xr[0]}_{Xr[1]}_y{Yr[0]}_{Yr[1]}.png"
#     # Guardar la figura en un archivo PNG
#     plt.savefig(filename)

#     plt.show()


# def Julia(z, c, k):
#     """
#     Calcula la pertenencia de un punto al conjunto de Julia y devuelve el resultado.

#     Args:
#         z: Punto complejo a evaluar.
#         c: Parámetro en la ecuación z = z^2 + c.
#         k: Número máximo de iteraciones.

#     Returns:
#         Tuple (pertenece, iteraciones):
#             - pertenece: Booleano que indica si el punto pertenece al conjunto de Julia.
#             - iteraciones: Número de iteraciones realizadas antes de determinar la pertenencia.
#     """
#     R = max(abs(c), 2)
#     i = 0
#     while i < k:
#         if abs(z) > R:
#             return 1, i
#         z = z**2 + c
#         i += 1
#     return 0, i


# def Mandelbrot_plot(n, k, Xr=(-2, 2), Yr=(-2, 2)):
#     """
#     Función para generar y guardar un gráfico del conjunto de Mandelbrot.

#     Args:
#         n: Número de puntos en cada dimensión del gráfico.
#         k: Número máximo de iteraciones para determinar la pertenencia de un punto al conjunto.
#         Xr: Rango del eje x (valores mínimo y máximo).
#         Yr: Rango del eje y (valores mínimo y máximo).

#     Returns:
#         None
#     """
#     x = np.linspace(Xr[0], Xr[1], n)
#     y = np.linspace(Yr[0], Yr[1], n)
#     X, Y = np.meshgrid(x, y)
#     W = np.zeros((len(X), len(Y)))

#     # Calcular el valor de pertenencia para cada punto del gráfico
#     for m in range(X.shape[1]):
#         for j in range(Y.shape[1]):
#             w, iter = Mandelbrot(X[m, j] + Y[m, j] * 1j, k)
#             W[m, j] += iter

#     # Crear el gráfico de Heatmap con Plotly
#     fig = go.Figure(data=go.Heatmap(x=x, y=y, z=W))
#     fig.update_layout(
#         title=f"Mandelbrot Set (n={n}, k={k})",
#         xaxis_title="Real",
#         yaxis_title="Imaginary",
#         width=800,
#         height=600
#     )

#     # Ajustar el rango de ejes al centro del gráfico
#     fig.update_xaxes(range=[Xr[0], Xr[1]], constrain="domain")
#     fig.update_yaxes(range=[Yr[0], Yr[1]], constrain="domain")

#     # Generar el nombre del archivo basado en los datos de entrada
#     filename = f"img/mandelbrot_{n}_{k}_{Xr[0]}_{Xr[1]}_{Yr[0]}_{Yr[1]}.html"
#     # Guardar la figura en un archivo HTML
#     pio.write_html(fig, filename)

#     # Mostrar el gráfico
#     fig.show()
