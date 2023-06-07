import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import tempfile
import cmath
import mpmath
import time

# Diccionario de funciones disponibles para el fractal de Mandelbrot
function_dict = {
    'Fractal de Mandelbrot del tipo z = z^m + c': lambda z, c, m: z ** m + c,
    'Fractal de Mandelbrot del tipo z =  z^m + 1/c': lambda z, c, m: z ** m + 1/c,
    'Fractal de Mandelbrot del tipo z = cos(z^m) + 1/c': lambda z, c, m: cmath.cos(z**m) + 1/c,
    'Fractal de Mandelbrot del tipo z = sin(z^m) + 1/c': lambda z, c, m: cmath.sin(z**m) + 1/c,
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
    Genera y muestra un gráfico del conjunto de Mandelbrot utilizando la biblioteca Matplotlib.

    Args:
        n: Número de puntos en cada dimensión del gráfico.
        k: Número máximo de iteraciones.
        Xr: Rango de valores del eje x [xmin, xmax].
        Yr: Rango de valores del eje y [ymin, ymax].
        color: Mapa de colores a utilizar en el gráfico.
        selected_func: Nombre de la función seleccionada por el usuario.
        m: Potencia de z.

    Returns:
        BytesIO: Archivo de imagen en formato PNG.
    """
    start_time = time.time()  # Registro del tiempo de inicio de la ejecución

    # Obtener el nombre de la función seleccionada
    name_selected_func = function_dict[selected_func]

    # Generar las coordenadas x e y
    x = np.linspace(Xr[0], Xr[1], n)
    y = np.linspace(Yr[0], Yr[1], n)
    X, Y = np.meshgrid(x, y)

    # Inicializar la matriz de valores del conjunto de Mandelbrot
    W = np.zeros((len(X), len(Y)))

    # Barra de progreso
    progress_bar = st.progress(0)

    # Calcular el valor del conjunto de Mandelbrot para cada punto
    for i in range(len(X)):
        for j in range(len(Y)):
            c = X[i, j] + Y[i, j] * 1j
            z = 0
            func = function_dict[selected_func]
            for _ in range(k):
                z = func(z, c, m)
                if abs(z) > 2:
                    break
            # Almacenar el número de iteraciones en la matriz W
            W[i, j] = _
        # Muestra el progreso de la ejecución
        progress_bar.progress(i / len(X))
    # Crear una figura y mostrar la imagen del conjunto de Mandelbrot en ella
    fig = plt.figure()
    plt.imshow(W, extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
               cmap=color, interpolation='bilinear', aspect="equal")

    # Configurar el título de la gráfica con los parámetros y la función seleccionada
    plt.title(
        f"{selected_func}, m={m}, n={n}, k={k}", fontsize=9)
    # Configurar el tamaño de los números de los ejes x e y
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # Mostrar la figura en la interfaz de Streamlit
    st.pyplot(fig)

    # Generar el nombre del archivo basado en los datos de entrada y la función seleccionada
    # ! arreglar el nombre con el que se guarda el archivo
    filename = f"img/{name_selected_func}_m{m}_n{n}_k{k}.png"

    # Guardar la figura en un archivo temporal en formato PNG
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png")
        tmpfile.seek(0)  # Reiniciar el puntero del archivo al inicio
        img_bytes = tmpfile.read()

    end_time = time.time()  # Registro del tiempo de finalización de la ejecución
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución: {round(execution_time, 2)} segundos")

    # st.write(f"Tiempo de ejecución: {round(execution_time, 2)} segundos")

    # Devolver los bytes de la imagen y el nombre del archivo
    return img_bytes, filename


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
    Genera y muestra un gráfico del conjunto de Julia utilizando la biblioteca Matplotlib.

    Args:
        n: Número de puntos en cada dimensión del gráfico.
        c_real: Parte real del parámetro c en la ecuación z = z^2 + c.
        c_imag: Parte imaginaria del parámetro c en la ecuación z = z^2 + c.
        k: Número máximo de iteraciones.
        Xr: Rango de valores del eje x [xmin, xmax].
        Yr: Rango de valores del eje y [ymin, ymax].

    Returns:
        BytesIO: Archivo de imagen en formato PNG.
    """

    # Obtener el nombre de la función seleccionada
    name_selected_funct = funct_dict[selected_funct]

    c = complex(c_real, c_imag)
    x = np.linspace(Xr[0], Xr[1], n)
    y = np.linspace(Yr[0], Yr[1], int(n * (Yr[1] - Yr[0]) / (Xr[1] - Xr[0])))
    X, Y = np.meshgrid(x, y)
    W = np.zeros((len(X), len(Y)))

    # Barra de progresp
    progress_bar_j = st.progress(0)
    for m in range(X.shape[0]):
        for j in range(Y.shape[0]):
            z = X[m, j] + Y[m, j] * 1j
            R = max(abs(c), 2)
            i = 0
            funct = funct_dict[selected_funct]
            while i < k:
                if abs(z) > R:
                    break
                z = funct(z, c, m_j)

                i += 1
            W[m, j] = i
        progress_bar_j.progress(m / X.shape[0])

    # Crear una figura y mostrar la imagen del conjunto de Mandelbrot en ella
    fig = plt.figure()
    plt.imshow(W, extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
               cmap=color, interpolation='bilinear', aspect="equal")

    # Establecer el título de la gráfica con los parámetros
    plt.title(
        f"Conjunto de Julia ({selected_funct}, m={m_j},c={c}, n={n}, k={k})", fontsize=9)

    # Configurar el tamaño de los números de los ejes x e y
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # Mostrar la figura en la interfaz de Streamlit
    st.pyplot(fig)

    # Generar el nombre del archivo basado en los datos de entrada y la función seleccionada
    filename_j = f"img/julia_{name_selected_funct}_m{m_j}_c{c}_n{n}_k{k}.png"

    # Guardar la figura en un archivo temporal en formato PNG
    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png")
        tmpfile.seek(0)  # Reiniciar el puntero del archivo al inicio
        img_bytes = tmpfile.read()

    # Devolver los bytes de la imagen
    return img_bytes, filename_j


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
