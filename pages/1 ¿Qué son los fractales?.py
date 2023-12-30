import streamlit as st
import warnings
from utils.funciones import *

################################################# CONFIGURACIÓN DE LA PÁGINA  #####################################################
st.set_page_config(
    page_title="Fractales",
    layout="wide",
    page_icon="❄️",
    initial_sidebar_state="collapsed",
)
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action="ignore", category=FutureWarning)


def main():
    # Cambiar la fuente de texto
    st.write(
        """ <style>h1, h2, h3, h4, h5, h6 { font-family: 'roman'; } </style>""",
        unsafe_allow_html=True,
    )

    # Header
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown("# ¿Qué es un fractal?")
        # st.markdown('## SUBTITULO')

    with col2:
        st.image("img/koch_fractal.gif", caption="Fractal de Koch")
    expander = st.expander("Nivel básico")
    expander.write(
        """\
        Un fractal es una figura geométrica que se repite a sí misma en diferentes escalas. Es similar a un patrón que se repite una y otra vez. Piensa en una ramificación de un árbol: cada rama se divide en ramitas más pequeñas, y esas ramitas se vuelven a dividir en ramitas aún más pequeñas. Así es como se ve un fractal: una estructura que se repite a diferentes escalas.
        """
    )

    expander = st.expander("Nivel intermedio")
    expander.write(
        """\
        Los fractales son objetos matemáticos fascinantes que tienen propiedades únicas. Un fractal es una figura que exhibe autosimilitud, lo que significa que su estructura se repite a sí misma en diferentes niveles de detalle. Si te acercas o te alejas de un fractal, seguirás viendo patrones similares. Estos patrones se construyen mediante un proceso llamado iteración, donde una forma inicial se somete repetidamente a una serie de transformaciones.

        Los fractales tienen aplicaciones en diversas áreas, como matemáticas, física, gráficos por computadora y biología. En matemáticas, los fractales se describen utilizando conceptos avanzados como ecuaciones iterativas, sistemas dinámicos y teoría del caos. En física, los fractales pueden describir fenómenos complejos, como la formación de fracturas en materiales sólidos o el comportamiento de los fluidos turbulentos. En gráficos por computadora, se utilizan algoritmos fractales para generar paisajes, texturas y formas naturales de apariencia realista. En biología, los fractales se utilizan para modelar estructuras naturales, como la distribución de ramas en un árbol o los patrones en la superficie de una hoja.
        """
    )

    expander = st.expander("Nivel avanzado")
    expander.write(
        """\
        Un fractal se define matemáticamente como un conjunto cuya dimensión topológica es mayor que su dimensión métrica. Esto significa que su superficie aparente es menor que su contenido interior. El ejemplo más conocido de un fractal es el conjunto de Mandelbrot, que se genera mediante la iteración de una simple fórmula matemática. Los fractales pueden tener formas muy complejas y hermosas, con detalles intrincados que se repiten a diferentes escalas.

        En un nivel más técnico, los fractales se pueden describir utilizando conceptos matemáticos avanzados, como ecuaciones iterativas, sistemas dinámicos y teoría del caos. Un fractal se construye mediante la repetición de un proceso iterativo en el que se aplica una función o transformación a un conjunto de puntos en un espacio matemático. A medida que la iteración continúa, los puntos se acumulan y generan patrones autosemejantes a diferentes escalas.

        Los fractales exhiben características interesantes, como la autosimilitud, donde las partes más pequeñas del objeto se asemejan a la forma general del objeto completo. Esto implica que las propiedades del fractal se mantienen invariantes a diferentes niveles de magnificación. Por ejemplo, en el conjunto de Mandelbrot, una pequeña porción de la figura se asemeja a la estructura general del conjunto completo.

        Además, los fractales pueden tener dimensiones fraccionarias o fractales. Por ejemplo, un objeto bidimensional tradicional, como un círculo, tiene una dimensión de 2, mientras que un fractal puede tener una dimensión fractal de, por ejemplo, 1.5. Esta dimensión fractal es una medida de cómo se llena el espacio con el objeto fractal a medida que se examina a diferentes escalas.
        """
    )


if __name__ == "__main__":
    main()
