import tempfile
import cmath
import mpmath
import math
import numpy as np
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
import streamlit as st

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
    start_time = time.time()
    name_selected_func = function_dict[selected_func]
    x = np.linspace(Xr[0], Xr[1], n)
    y = np.linspace(Yr[0], Yr[1], n)
    X, Y = np.meshgrid(x, y)
    W = np.zeros((len(X), len(Y)))

    def calculate_mandelbrot(i, j):
        c = X[i, j] + Y[i, j] * 1j
        z = 0
        func = function_dict[selected_func]
        for _ in range(k):
            z = func(z, c, m)
            if abs(z) > 2:
                break
        return _

    num_cores = -1
    results = Parallel(n_jobs=num_cores)(
        delayed(calculate_mandelbrot)(i, j)
        for i in range(len(X))
        for j in range(len(Y))
    )

    for i in range(len(X)):
        for j in range(len(Y)):
            W[i, j] = results[i * len(Y) + j]

    fig, ax = plt.subplots()
    ax.imshow(
        W,
        extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
        cmap=color,
        interpolation="bilinear",
        aspect="equal",
    )
    ax.set_title(f"{selected_func}, m={m}, n={n}, k={k}", fontsize=9)
    ax.tick_params(axis="both", labelsize=8)
    st.pyplot(fig)

    filename = f"img/{selected_func}_m{m}_n{n}_k{k}.png"

    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png", dpi=300)
        tmpfile.seek(0)
        img_bytes = tmpfile.read()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {round(execution_time, 2)} seconds")

    minutes = math.floor(execution_time / 60)
    seconds = execution_time % 60
    time_str = (
        f"{minutes} minutes and {seconds} seconds"
        if minutes > 0
        else f"{round(seconds, 2)} seconds"
    )
    print(f"Execution time: {time_str}")

    return img_bytes, filename, execution_time


funct_dict = {
    "Fractal de Julia del tipo z^m + c": lambda z, c, m: z**m + c,
    "Fractal de Julia del tipo z^m + 1/c": lambda z, c, m: z**m + 1 / c,
    "Fractal de Julia del tipo z = Exp(z^m/c^m)": lambda z, c, m: mpmath.exp(
        z**m / c**m
    ),
}


@st.cache_data()
def st_plot_julia(n, c_real, c_imag, k, Xr, Yr, color, selected_funct, m_j):
    start_time_j = time.time()
    name_selected_funct = funct_dict[selected_funct]
    c = complex(c_real, c_imag)
    x = np.linspace(Xr[0], Xr[1], n)
    y = np.linspace(Yr[0], Yr[1], int(n * (Yr[1] - Yr[0]) / (Xr[1] - Xr[0])))
    X, Y = np.meshgrid(x, y)
    W = np.zeros((len(X), len(Y)))

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

    num_cores = -1
    results = Parallel(n_jobs=num_cores)(
        delayed(calculate_julia)(m, j)
        for m in range(X.shape[0])
        for j in range(Y.shape[0])
    )

    for m in range(X.shape[0]):
        for j in range(Y.shape[0]):
            W[m, j] = results[m * Y.shape[0] + j]

    fig = plt.figure()
    plt.imshow(
        W,
        extent=[Xr[0], Xr[1], Yr[0], Yr[1]],
        cmap=color,
        interpolation="bilinear",
        aspect="equal",
    )
    plt.title(
        f"Conjunto de Julia ({selected_funct}, m={m_j}, c={c}, n={n}, k={k})",
        fontsize=9,
    )
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    st.pyplot(fig)

    filename_j = f"img/julia_{selected_funct}_m{m_j}_c{c}_n{n}_k{k}.png"

    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png", dpi=300)
        tmpfile.seek(0)
        img_bytes = tmpfile.read()

    end_time = time.time()
    execution_time_j = end_time - start_time_j

    minutes_j = math.floor(execution_time_j / 60)
    seconds_j = execution_time_j % 60
    time_str = (
        f"{minutes_j} minutos y {seconds_j} segundos"
        if minutes_j > 0
        else f"{round(seconds_j, 2)} segundos"
    )
    print(f"Tiempo de ejecución: {time_str}")

    return img_bytes, filename_j, execution_time_j
