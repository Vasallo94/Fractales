import tempfile
import math
import numpy as np
import matplotlib.pyplot as plt
import time
import streamlit as st
from numba import jit, prange

# Mapping of function names to IDs for Numba
# Mapping of function names to IDs for Numba
MANDELBROT_FUNCS = [
    "Fractal de Mandelbrot del tipo z = z^m + c",
    "Fractal de Mandelbrot del tipo z =  z^m + 1/c",
    "Fractal de Mandelbrot del tipo z = cos(z^m) + 1/c",
    "Fractal de Mandelbrot del tipo z = sin(z^m) + 1/c",
    "Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / sqrt(c^3)]",
    "Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / c^3]",
    "Fractal de Mandelbrot del tipo z = cos(z^m/c^m)",
    "Fractal de Mandelbrot del tipo z = exp(z^m/c^m)",
    "Fractal de Mandelbrot del tipo z = exp(c^m/z^m)",
    "Fractal de Mandelbrot del tipo z = exp(z/c^m) + 1/c",
    "Fractal de Mandelbrot del tipo z = cosh(z^m/c^m)",
]

JULIA_FUNCS = [
    "Fractal de Julia del tipo z^m + c",
    "Fractal de Julia del tipo z^m + 1/c",
    "Fractal de Julia del tipo z = Exp(z^m/c^m)",
]

# LaTeX mappings for titles
MANDELBROT_LATEX = {
    "Fractal de Mandelbrot del tipo z = z^m + c": r"$z_{n+1} = z_n^m + c$",
    "Fractal de Mandelbrot del tipo z =  z^m + 1/c": r"$z_{n+1} = z_n^m + 1/c$",
    "Fractal de Mandelbrot del tipo z = cos(z^m) + 1/c": r"$z_{n+1} = \cos(z_n^m) + 1/c$",
    "Fractal de Mandelbrot del tipo z = sin(z^m) + 1/c": r"$z_{n+1} = \sin(z_n^m) + 1/c$",
    "Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / sqrt(c^3)]": r"$z_{n+1} = \exp\left(\frac{z_n^m - 1.00001 z_n}{\sqrt{c^3}}\right)$",
    "Fractal de Mandelbrot del tipo z = exp[(z^m - 1.00001 * z) / c^3]": r"$z_{n+1} = \exp\left(\frac{z_n^m - 1.00001 z_n}{c^3}\right)$",
    "Fractal de Mandelbrot del tipo z = cos(z^m/c^m)": r"$z_{n+1} = \cos(z_n^m/c^m)$",
    "Fractal de Mandelbrot del tipo z = exp(z^m/c^m)": r"$z_{n+1} = \exp(z_n^m/c^m)$",
    "Fractal de Mandelbrot del tipo z = exp(c^m/z^m)": r"$z_{n+1} = \exp(c^m/z_n^m)$",
    "Fractal de Mandelbrot del tipo z = exp(z/c^m) + 1/c": r"$z_{n+1} = \exp(z_n/c^m) + 1/c$",
    "Fractal de Mandelbrot del tipo z = cosh(z^m/c^m)": r"$z_{n+1} = \cosh(z_n^m/c^m)$",
}

JULIA_LATEX = {
    "Fractal de Julia del tipo z^m + c": r"$z_{n+1} = z_n^m + c$",
    "Fractal de Julia del tipo z^m + 1/c": r"$z_{n+1} = z_n^m + 1/c$",
    "Fractal de Julia del tipo z = Exp(z^m/c^m)": r"$z_{n+1} = \exp(z_n^m/c^m)$",
}

# Create dictionaries to maintain compatibility with existing main code
function_dict = {name: i for i, name in enumerate(MANDELBROT_FUNCS)}
funct_dict = {name: i for i, name in enumerate(JULIA_FUNCS)}

@jit(nopython=True, fastmath=True, parallel=True)
def compute_mandelbrot_numba(h, w, k, x_min, x_max, y_min, y_max, func_id, m):
    result = np.zeros((h, w), dtype=np.int32)
    
    dx = (x_max - x_min) / w
    dy = (y_max - y_min) / h
    
    for i in prange(h):
        y = y_min + i * dy
        for j in range(w):
            x = x_min + j * dx
            c = complex(x, y)
            z = 0.0j
            
            iter_count = 0
            while iter_count < k and (z.real*z.real + z.imag*z.imag) <= 4.0:
                if func_id == 0:
                    z = z**m + c
                elif func_id == 1:
                    if c != 0: z = z**m + 1/c
                    else: z = 0 # Handle division by zero
                elif func_id == 2:
                    if c != 0: z = np.cos(z**m) + 1/c
                elif func_id == 3:
                    if c != 0: z = np.sin(z**m) + 1/c
                elif func_id == 4:
                    # exp[(z^m - 1.00001 * z) / sqrt(c^3)]
                    if c != 0:
                        term = np.sqrt(c**3)
                        if term != 0:
                            z = np.exp((z**m - 1.00001 * z) / term)
                elif func_id == 5:
                    if c != 0: z = np.exp((z**m - 1.00001 * z) / c**3)
                elif func_id == 6:
                    if c != 0: z = np.cos(z**m / c**m)
                elif func_id == 7:
                    if c != 0: z = np.exp(z**m / c**m)
                elif func_id == 8:
                    if z != 0: z = np.exp(c**m / z**m)
                elif func_id == 9:
                    if c != 0: z = np.exp(z / c**m) + 1/c
                elif func_id == 10:
                    if c != 0: z = np.cosh(z**m / c**m)
                
                iter_count += 1
            
            result[i, j] = iter_count
            
    return result

@jit(nopython=True, fastmath=True, parallel=True)
def compute_julia_numba(h, w, k, x_min, x_max, y_min, y_max, func_id, c, m_j):
    result = np.zeros((h, w), dtype=np.int32)
    
    dx = (x_max - x_min) / w
    dy = (y_max - y_min) / h
    
    R = max(abs(c), 2.0)
    R2 = R * R
    
    for i in prange(h):
        y = y_min + i * dy
        for j in range(w):
            x = x_min + j * dx
            z = complex(x, y)
            
            iter_count = 0
            while iter_count < k and (z.real*z.real + z.imag*z.imag) <= R2:
                if func_id == 0:
                    z = z**m_j + c
                elif func_id == 1:
                    if c != 0: z = z**m_j + 1/c
                elif func_id == 2:
                    if c != 0: z = np.exp(z**m_j / c**m_j)
                
                iter_count += 1
            
            result[i, j] = iter_count
            
    return result

@st.cache_data()
def st_plot_mandelbrot(n, k, Xr, Yr, color, selected_func, m):
    start_time = time.time()
    
    # Get ID from the dict (which now maps to ints) or handle if it's still using old dict
    # The main file passes the key string.
    func_id = function_dict.get(selected_func, 0)
    
    # Ensure inputs are correct types for Numba
    x_min, x_max = float(Xr[0]), float(Xr[1])
    y_min, y_max = float(Yr[0]), float(Yr[1])
    
    # Compute
    # Note: n is used for both width and height in the original code? 
    # Original: x = np.linspace(Xr[0], Xr[1], n), y = np.linspace(Yr[0], Yr[1], n)
    # So it's n x n
    W = compute_mandelbrot_numba(n, n, k, x_min, x_max, y_min, y_max, func_id, m)
    
    # Plotting
    fig, ax = plt.subplots()
    ax.imshow(
        W,
        extent=[x_min, x_max, y_min, y_max],
        cmap=color,
        interpolation="bilinear",
        aspect="equal",
        origin="lower" # Matplotlib imshow origin is upper by default, but we generated from y_min to y_max
    )
    
    # Use LaTeX title if available
    title_str = MANDELBROT_LATEX.get(selected_func, selected_func)
    ax.set_title(f"{title_str}, m={m}, n={n}, k={k}", fontsize=10)
    ax.tick_params(axis="both", labelsize=8)
    st.pyplot(fig)

    filename = f"img/{selected_func}_m{m}_n{n}_k{k}.png"

    with tempfile.NamedTemporaryFile(suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name, format="png", dpi=300) # Reduced DPI for speed, 1000 is overkill for web
        tmpfile.seek(0)
        img_bytes = tmpfile.read()

    end_time = time.time()
    execution_time = end_time - start_time
    
    minutes = math.floor(execution_time / 60)
    seconds = execution_time % 60
    time_str = (
        f"{minutes} minutes and {seconds} seconds"
        if minutes > 0
        else f"{round(seconds, 2)} seconds"
    )
    print(f"Execution time: {time_str}")

    return img_bytes, filename, execution_time

@st.cache_data()
def st_plot_julia(n, c_real, c_imag, k, Xr, Yr, color, selected_funct, m_j):
    start_time_j = time.time()
    
    func_id = funct_dict.get(selected_funct, 0)
    c = complex(c_real, c_imag)
    
    x_min, x_max = float(Xr[0]), float(Xr[1])
    y_min, y_max = float(Yr[0]), float(Yr[1])
    
    # Original logic for height: int(n * (Yr[1] - Yr[0]) / (Xr[1] - Xr[0]))
    h = int(n * (y_max - y_min) / (x_max - x_min))
    w = n
    
    W = compute_julia_numba(h, w, k, x_min, x_max, y_min, y_max, func_id, c, m_j)

    fig = plt.figure()
    plt.imshow(
        W,
        extent=[x_min, x_max, y_min, y_max],
        cmap=color,
        interpolation="bilinear",
        aspect="equal",
        origin="lower"
    )
    
    # Use LaTeX title if available
    title_str = JULIA_LATEX.get(selected_funct, selected_funct)
    plt.title(
        f"{title_str}, m={m_j}, c={c:.2f}, n={n}, k={k}",
        fontsize=10,
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
