"""
Aplicación de Streamlit para la representación y visualización de fractales generados con python.

Enrique Vasallo Fernández
"""
import warnings
import math
from utils.funciones import *
import streamlit as st

# Establece la opción de almacenamiento en caché de Streamlit en disco
st.set_option("client.caching", "disk")

################################################# CONFIGURACIÓN DE LA PÁGINA  #####################################################
st.set_page_config(
    page_title="Fractales",
    layout="wide",
    page_icon="❄️",
    initial_sidebar_state="collapsed",
)
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action="ignore", category=FutureWarning)

# # Configuración de la barra lateral y de Made with Streamlit
# st.markdown("""
# <style>
# .css-njmhce.e1ewe7hr3
# {
# visibility: hidden;
# }
# {
# .css-10pw50.e1g8pov61
# {
# visibility: hidden;
# }
# </style›""", unsafe_allow_html=True)

########################################### INICIO DE LA PÁGINA ###########################################################


def main():
    # Cambiar la fuente de texto
    st.write(
        """ <style>h1, h2, h3, h4, h5, h6 { font-family: 'roman'; } </style>""",
        unsafe_allow_html=True,
    )
    # Header
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("# Fractales")
        # st.markdown('## SUBTITULO')

    with col2:
        st.image("img/koch_fractal.gif", caption="Fractal de Koch")

    # Tabs para la selección de fractales
    tabs = st.tabs(["Conjunto de Mandelbrot", "Conjunto de Julia"])

    # Tab 1
    # Mandelbrot
    with tabs[0]:
        st.markdown(
            "<center><h2><l style='color:white; font-size: 30px;'>Conjunto de Mandelbrot</h2></l></center>",
            unsafe_allow_html=True,
        )
        st.markdown("""---""")

        # Obtener los valores de los sliders desde el usuario
        n_m = st.slider(
            "Número de puntos a generar (n)",
            min_value=100,
            max_value=5000,
            value=600,
            step=25,
            help="El número de puntos a generar en el conjunto de Mandelbrot.",
        )
        k_m = st.slider(
            "Número de iteraciones (k)",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="El número de iteraciones para determinar si un punto pertenece al conjunto de Mandelbrot.",
        )
        Xr_m = st.slider(
            "Rango de valores del eje $x$:",
            -10.0,
            10.0,
            (-2.0, 1.0),
            step=0.1,
            help="El rango de valores del eje x para la visualización del conjunto de Mandelbrot.",
        )
        Yr_m = st.slider(
            "Rango de valores del eje $y$:",
            -10.0,
            10.0,
            (-1.0, 1.0),
            step=0.1,
            help="El rango de valores del eje y para la visualización del conjunto de Mandelbrot.",
        )
        selected_func = st.selectbox(
            "Selecciona la función",
            list(function_dict.keys()),
            help="La función utilizada para generar el conjunto de Mandelbrot.",
        )
        m = st.slider(
            "Valor de $m$:",
            min_value=1,
            max_value=25,
            value=2,
            step=1,
            help="El valor de m utilizado en la función para generar el conjunto de Mandelbrot.",
        )
        color_m = st.selectbox(
            "Selecciona la paleta de colores:",
            (
                "hot",
                "cool",
                "spring",
                "summer",
                "autumn",
                "winter",
                "RdBu",
                "RdGy",
                "RdYlBu",
                "RdYlGn",
                "Spectral",
                "plasma",
                "inferno",
                "magma",
                "viridis",
            ),
            help="La paleta de colores utilizada para la visualización del conjunto de Mandelbrot.",
        )

        # Verificar si se ha presionado el botón "Generar Plot"
        if st.button("Generar gráfico del conjunto de Mandelbrot"):
            # Llamar a la función st_plot_mandelbrot con los parámetros ingresados
            img_bytes, filename, execution_time = st_plot_mandelbrot(
                n_m, k_m, Xr_m, Yr_m, color_m, selected_func, m
            )
            # Convertir el tiempo de ejecución a minutos y segundos
            minutes = math.floor(execution_time / 60)
            seconds = execution_time % 60

            # Formatear el tiempo en minutos y segundos
            time_str = (
                f"{minutes} minutos y {round(seconds, 2)} segundos"
                if minutes > 0
                else f"{round(seconds, 2)} segundos"
            )
            st.write(f"Tiempo de ejecución: {time_str}")
            # Verificar si se pudo generar el gráfico
            if img_bytes is not None:
                # Agregar un botón para descargar la imagen en formato PNG
                st.download_button(
                    "Descargar imagen",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/png",
                )
            else:
                # Mostrar un mensaje de error si no se pudo generar el gráfico
                st.error("No se pudo generar el gráfico.")

    # Tab 2
    # Julia
    with tabs[1]:
        st.markdown(
            "<center><h2><l style='color:white; font-size: 30px;'>Conjunto de Julia</h2></l></center>",
            unsafe_allow_html=True,
        )
        st.markdown("""---""")
        # Obtener los valores de los sliders desde el usuario
        n_j = st.slider(
            "Número de puntos a generar (n)",
            min_value=100,
            max_value=10000,
            value=1000,
            step=10,
            key="slider_n_j",
            help="El número de puntos a generar para el conjunto de Julia.",
        )
        k_j = st.slider(
            "Número de iteraciones (k)",
            min_value=1,
            max_value=1000,
            value=100,
            step=10,
            key="slider_k_j",
            help="El número de iteraciones para el conjunto de Julia.",
        )
        c_real = st.number_input(
            "Valor de la parte real de c, $Re(c)$:",
            value=0.0,
            help="El valor de la parte real de c para el conjunto de Julia.",
        )
        c_imag = st.number_input(
            "Valor de la parte imaginaria de c, $Im(c)$:",
            value=-1.0,
            help="El valor de la parte imaginaria de c para el conjunto de Julia.",
        )
        selected_funct = st.selectbox(
            "Selecciona la función",
            list(funct_dict.keys()),
            key="selectbox_funct_j",
            help="La función utilizada para generar el conjunto de Julia.",
        )
        m_j = st.slider(
            "Valor de $m$:",
            min_value=2,
            max_value=25,
            value=2,
            step=1,
            key="slider_m_j",
            help="El valor de m utilizado en la función para generar el conjunto de Julia.",
        )
        Xr_j = st.slider(
            "Rango de Valores del eje $x$:",
            -10.0,
            10.0,
            (-2.0, 2.0),
            key="slider_Xr_j",
            step=0.1,
            help="El rango de valores del eje x para la visualización del conjunto de Julia.",
        )
        Yr_j = st.slider(
            "Rango de Valores del eje $y$:",
            -10.0,
            10.0,
            (-2.0, 2.0),
            key="slider_Yr_j",
            step=0.1,
            help="El rango de valores del eje y para la visualización del conjunto de Julia.",
        )
        color_j = st.selectbox(
            "Selecciona la paleta de colores:",
            (
                "hot",
                "cool",
                "spring",
                "summer",
                "autumn",
                "winter",
                "RdBu",
                "RdGy",
                "RdYlBu",
                "RdYlGn",
                "Spectral",
                "plasma",
                "inferno",
                "magma",
                "viridis",
            ),
            key="selectbox_color_j",
            help="La paleta de colores utilizada para la visualización del conjunto de Julia.",
        )
        # Verificar si se ha presionado el botón "Generar Plot"
        if st.button("Generar gráfico del conjunto de Julia", key="button_plot"):
            # Llamar a la función plot_julia con los parámetros ingresados
            img_bytes, filename_j, execution_time_j = st_plot_julia(
                n_j, c_real, c_imag, k_j, Xr_j, Yr_j, color_j, selected_funct, m_j
            )
            # Convertir el tiempo de ejecución a minutos y segundos
            minutes_j = math.floor(execution_time_j / 60)
            seconds_j = execution_time_j % 60

            # Formatear el tiempo en minutos y segundos
            time_str = (
                f"{minutes_j} minutos y {round(seconds_j, 2)} segundos"
                if minutes_j > 0
                else f"{round(seconds_j, 2)} segundos"
            )
            st.write(f"Tiempo de ejecución: {time_str}")
            # Verificar si se pudo generar el gráfico
            if img_bytes is not None:
                # Agregar un botón para descargar la imagen en formato PNG
                st.download_button(
                    "Descargar imagen",
                    data=img_bytes,
                    file_name=filename_j,
                    mime="image/png",
                )
            else:
                # Mostrar un mensaje de error si no se pudo generar el gráfico
                st.error("No se pudo generar el gráfico.")


if __name__ == "__main__":
    main()
