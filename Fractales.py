"""
Aplicación de Streamlit para la representación y visualización de fractales generados con python.

Enrique Vasallo Fernández
"""
import warnings
import math
from utils.funciones import *
import streamlit as st


st.set_page_config(
    page_title="Fractales",
    layout="wide",
    page_icon="❄️",
    initial_sidebar_state="expanded",
)

warnings.simplefilter(action="ignore", category=FutureWarning)

st.markdown(
    """<style>.css-njmhce.e1ewe7hr3{visibility: hidden;}{.css-10pw50.e1g8pov61{visibility: hidden;}</style›""",
    unsafe_allow_html=True,
)

########################################### INICIO DE LA PÁGINA ###########################################################


def main():
    # Cambiar la fuente de texto
    st.write(
        """ <style>h1, h2, h3, h4, h5, h6 { font-family: 'roman'; } </style>""",
        unsafe_allow_html=True,
    )
    st.markdown("# Fractales")

    # Sidebar navigation
    st.sidebar.title("Navegación")
    selection = st.sidebar.radio(
        "Ir a:",
        ["Inicio", "Conjunto de Mandelbrot", "Conjunto de Julia"]
    )

    # Inicio
    if selection == "Inicio":
        # Hero Section
        st.markdown("## 🌀 Explorador de Fractales")
        st.markdown(
            """
            <div style='background-color: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <p style='font-size: 1.1em; line-height: 1.6;'>
            Descubre la belleza infinita de las matemáticas a través de los <strong>conjuntos de Mandelbrot y Julia</strong>. 
            Esta aplicación te permite explorar y generar visualizaciones fractales únicas ajustando diferentes parámetros.
            </p>
            <p style='margin-top: 10px;'>
            👈 <strong>Comienza</strong> seleccionando un conjunto en la barra lateral y experimenta con los controles.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Example Images
        st.markdown("### 🎨 Ejemplos de lo que puedes crear")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.image("img/julia.png", use_container_width=True)
            st.caption("✨ Conjunto de Julia - Patrones orgánicos y ramificados")
        with col2:
            st.image("img/img_mandelbrot_Fractal de Mandelbrot del tipo z^m + 1_c_n600_k100_x-1.5_1.5_y-1.5_1.5.png", use_container_width=True)
            st.caption("🌟 Conjunto de Mandelbrot - El fractal más famoso")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Educational Content
        st.markdown("## 📚 ¿Qué es un fractal?")
        
        # Expandable explanations with better formatting
        with st.expander("🌱 Nivel básico - Introducción", expanded=True):
            col_img_small, col_text_small = st.columns([1, 2])
            with col_img_small:
                st.image("img/koch_fractal.gif", use_container_width=True)
                st.caption("Fractal de Koch")
            with col_text_small:
                st.markdown(
                    """
                    Un **fractal** es una estructura matemática que exhibe **autosimilitud**: 
                    sus patrones se repiten a diferentes escalas. 
                    
                    Imagina un **árbol**: cada rama se divide en ramas más pequeñas, y esas ramas 
                    se dividen en ramitas aún más pequeñas. Este patrón que se repite una y otra 
                    vez es la esencia de un fractal.
                    """
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                """
                **Ejemplos en la naturaleza:**
                - 🌿 Helechos y brócoli romanesco
                - ❄️ Copos de nieve
                - 🌊 Costas y montañas
                - ⚡ Rayos y relámpagos
                
                Los fractales están por todas partes en la naturaleza, creando formas 
                infinitamente complejas a partir de reglas simples.
                """
            )

        with st.expander("🔬 Nivel intermedio - Propiedades y aplicaciones"):
            st.markdown(
                """
                ### Autosimilitud e iteración
                
                Los fractales exhiben **autosimilitud**: su estructura se repite a diferentes 
                niveles de detalle. Se construyen mediante **iteración**, aplicando repetidamente 
                una transformación matemática.
                
                ### Aplicaciones prácticas
                
                Los fractales no son solo belleza matemática, tienen aplicaciones reales:
                
                - **📐 Matemáticas:** Teoría del caos y sistemas dinámicos
                - **🔬 Física:** Modelado de turbulencia y fracturas en materiales
                - **🎮 Gráficos:** Generación de paisajes, nubes y texturas realistas
                - **🧬 Biología:** Modelado de estructuras como vasos sanguíneos y pulmones
                - **📡 Telecomunicaciones:** Diseño de antenas fractales compactas
                """
            )

        with st.expander("🎓 Nivel avanzado - Matemáticas profundas"):
            st.markdown(
                """
                ### Definición matemática
                
                Un fractal se define como un conjunto cuya **dimensión de Hausdorff-Besicovitch** 
                excede su dimensión topológica. Esto significa que tienen una "dimensión fraccionaria".
                
                Por ejemplo:
                - Una línea tiene dimensión 1
                - Un plano tiene dimensión 2  
                - La **curva de Koch** tiene dimensión ≈ 1.26
                - El **conjunto de Mandelbrot** tiene dimensión 2 (su frontera tiene dimensión fractal)
                
                ### Generación iterativa
                
                Los conjuntos de Mandelbrot y Julia se generan mediante la iteración de funciones 
                complejas de la forma:
                
                $$z_{n+1} = f(z_n, c)$$
                
                Donde:
                - $z_n$ es un número complejo en la iteración $n$
                - $c$ es un parámetro complejo
                - Para **Mandelbrot**: $z_0 = 0$ y $c$ varía por cada píxel
                - Para **Julia**: $c$ es fijo y $z_0$ varía por cada píxel
                
                Un punto pertenece al conjunto si la secuencia ${z_n}$ permanece acotada 
                (no tiende a infinito) tras infinitas iteraciones.
                
                ### Propiedades fascinantes
                
                - **Complejidad infinita:** Puedes hacer zoom infinitamente y siempre encontrarás nuevos detalles
                - **Frontera fractal:** La frontera del conjunto de Mandelbrot tiene longitud infinita
                - **Conexión:** El conjunto de Mandelbrot es conexo (una sola pieza), un resultado sorprendente demostrado por Douady y Hubbard
                """
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; padding: 20px; color: #888;'>
            <p>💡 <em>Explora los fractales usando la navegación de la izquierda</em></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Mandelbrot
    elif selection == "Conjunto de Mandelbrot":
        st.markdown(
            "<center><h2><l style='color:white; font-size: 30px;'>Conjunto de Mandelbrot</h2></l></center>",
            unsafe_allow_html=True,
        )
        # Menú desplegable para obtener más información sobre el conjunto de Mandelbrot
        with st.expander("ℹ️ Información sobre el conjunto de Mandelbrot"):
            st.markdown(
                """
                ### ¿Qué es el conjunto de Mandelbrot?
                
                El conjunto de Mandelbrot es uno de los objetos matemáticos más famosos y bellos. 
                Es un **conjunto de números complejos** que exhibe un comportamiento fascinante cuando 
                se itera una función simple.
                
                ### ¿Cómo se genera?
                
                Para cada punto $c$ en el plano complejo, iteramos la función:
                
                $$z_{n+1} = z_n^m + c$$
                
                Comenzando con $z_0 = 0$. Si la secuencia permanece acotada (no tiende a infinito), 
                entonces $c$ pertenece al conjunto de Mandelbrot.
                
                ### Parámetros de esta aplicación
                
                - **$m = 2$**: La función clásica $z^2 + c$ que genera el Mandelbrot tradicional
                - **$m > 2$**: Variaciones polinómicas que crean formas con más "pétalos"
                - **Otras funciones**: Puedes explorar variaciones con seno, coseno, exponenciales, etc.
                
                ### 💡 Consejos para explorar
                
                - Empieza con los valores por defecto para ver la forma clásica
                - Aumenta las iteraciones (k) para ver más detalles en los bordes
                - Ajusta los rangos de x e y para hacer zoom en regiones interesantes
                - Prueba diferentes funciones y valores de m para descubrir nuevas formas
                """
            )

        st.sidebar.markdown("""---""")
        st.sidebar.markdown("""### Configuración Mandelbrot""")
        # Obtener los valores de los sliders desde el usuario
        n_m = st.sidebar.slider(
            "Número de puntos a generar (n)",
            min_value=100,
            max_value=5000,
            value=1200,
            step=50,
            help="El número de puntos a generar en el conjunto de Mandelbrot. A n mayor, mayor será la resolución de la imagen generada, pero también mayor será el tiempo de ejecución.",
        )
        k_m = st.sidebar.slider(
            "Número de iteraciones (k)",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="El número de iteraciones para determinar si un punto pertenece al conjunto de Mandelbrot. A k mayor, mayor será el tiempo de ejecución.",
        )
        Xr_m = st.sidebar.slider(
            "Rango de valores del eje $x$:",
            -10.0,
            10.0,
            (-2.0, 1.0),
            step=0.1,
            help="El rango de valores del eje x para la visualización del conjunto de Mandelbrot.",
        )
        Yr_m = st.sidebar.slider(
            "Rango de valores del eje $y$:",
            -10.0,
            10.0,
            (-1.0, 1.0),
            step=0.1,
            help="El rango de valores del eje y para la visualización del conjunto de Mandelbrot.",
        )
        selected_func = st.sidebar.selectbox(
            "Selecciona la función (Mandelbrot)",
            list(function_dict.keys()),
            help="La función utilizada para generar el conjunto de Mandelbrot.",
        )
        m = st.sidebar.slider(
            "Valor de $m$ (Mandelbrot):",
            min_value=1,
            max_value=15,
            value=2,
            step=1,
            help="El valor de m utilizado en la función para generar el conjunto de Mandelbrot.",
        )
        color_m = st.sidebar.selectbox(
            "Selecciona la paleta de colores (Mandelbrot):",
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
        if st.sidebar.button("🎨 Generar Fractal", type="primary", use_container_width=True):
            # Llamar a la función st_plot_mandelbrot con los parámetros ingresados
            img_bytes, filename, execution_time = st_plot_mandelbrot(
                n_m, k_m, Xr_m, Yr_m, color_m, selected_func, m
            )
            # Guardar en session state para persistencia simple (opcional, pero bueno para UX)
            st.session_state["mandelbrot_image"] = (img_bytes, filename)
            
            # Convertir el tiempo de ejecución a minutos y segundos
            minutes = math.floor(execution_time / 60)
            seconds = execution_time % 60

            # Formatear el tiempo en minutos y segundos
            time_str = (
                f"{minutes} minutos y {seconds} segundos"
                if minutes > 0
                else f"{round(seconds, 2)} segundos"
            )
            st.success(f"Tiempo de ejecución: {time_str}")
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

    # Julia
    elif selection == "Conjunto de Julia":
        st.markdown(
            "<center><h2><l style='color:white; font-size: 30px;'>Conjunto de Julia</h2></l></center>",
            unsafe_allow_html=True,
        )
        # Menú desplegable para obtener más información sobre el conjunto de Julia
        with st.expander("ℹ️ Información sobre el conjunto de Julia"):
            st.markdown(
                """
                ### ¿Qué es el conjunto de Julia?
                
                Los conjuntos de Julia son una familia infinita de fractales, cada uno definido por 
                un valor específico del parámetro complejo $c$. Están íntimamente relacionados con el 
                conjunto de Mandelbrot.
                
                ### ¿Cómo se genera?
                
                Para un valor fijo de $c$, iteramos la función:
                
                $$z_{n+1} = z_n^m + c$$
                
                Pero ahora $c$ es **constante** y $z_0$ varía según la posición en el plano complejo.
                Si la secuencia permanece acotada, ese punto pertenece al conjunto de Julia para ese $c$.
                
                ### Relación con Mandelbrot
                
                🔗 **Conexión fascinante**: Cada punto $c$ del conjunto de Mandelbrot corresponde a 
                un conjunto de Julia **conexo** (de una sola pieza). Los puntos fuera de Mandelbrot 
                generan conjuntos de Julia **fragmentados** (polvo de Cantor).
                
                ### 💡 Consejos para explorar
                
                - **Valores interesantes de $c$**:
                  - $c = -0.7 + 0.27i$ (espiral)
                  - $c = 0.285 + 0.01i$ (dendritas)
                  - $c = -0.8 + 0.156i$ (forma de conejo)
                - Experimenta con diferentes valores de $m$ para crear variaciones
                - Ajusta los rangos para hacer zoom en detalles específicos
                """
            )
        
        st.sidebar.markdown("""---""")
        st.sidebar.markdown("""### Configuración Julia""")
        # Obtener los valores de los sliders desde el usuario
        n_j = st.sidebar.slider(
            "Número de puntos a generar (n)",
            min_value=100,
            max_value=10000,
            value=1500,
            step=50,
            key="slider_n_j",
            help="El número de puntos a generar para el conjunto de Julia. A n mayor, mayor será la resolución de la imagen generada, pero también mayor será el tiempo de ejecución.",
        )
        k_j = st.sidebar.slider(
            "Número de iteraciones (k)",
            min_value=1,
            max_value=1000,
            value=100,
            step=10,
            key="slider_k_j",
            help="El número de iteraciones para el conjunto de Julia. A k mayor, mayor será el tiempo de ejecución.",
        )
        c_real = st.sidebar.number_input(
            "Valor de la parte real de c, $Re(c)$:",
            value=0.0,
            help="El valor de la parte real de c para el conjunto de Julia.",
        )
        c_imag = st.sidebar.number_input(
            "Valor de la parte imaginaria de c, $Im(c)$:",
            value=-1.0,
            help="El valor de la parte imaginaria de c para el conjunto de Julia.",
        )
        selected_funct = st.sidebar.selectbox(
            "Selecciona la función (Julia)",
            list(funct_dict.keys()),
            key="selectbox_funct_j",
            help="La función utilizada para generar el conjunto de Julia.",
        )
        m_j = st.sidebar.slider(
            "Valor de $m$ (Julia):",
            min_value=2,
            max_value=25,
            value=2,
            step=1,
            key="slider_m_j",
            help="El valor de m utilizado en la función para generar el conjunto de Julia.",
        )
        Xr_j = st.sidebar.slider(
            "Rango de Valores del eje $x$ (Julia):",
            -10.0,
            10.0,
            (-2.0, 2.0),
            key="slider_Xr_j",
            step=0.1,
            help="El rango de valores del eje x para la visualización del conjunto de Julia.",
        )
        Yr_j = st.sidebar.slider(
            "Rango de Valores del eje $y$ (Julia):",
            -10.0,
            10.0,
            (-2.0, 2.0),
            key="slider_Yr_j",
            step=0.1,
            help="El rango de valores del eje y para la visualización del conjunto de Julia.",
        )
        color_j = st.sidebar.selectbox(
            "Selecciona la paleta de colores (Julia):",
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
        if st.sidebar.button("🎨 Generar Fractal", type="primary", use_container_width=True, key="button_plot"):
            # Llamar a la función plot_julia con los parámetros ingresados
            img_bytes, filename_j, execution_time_j = st_plot_julia(
                n_j, c_real, c_imag, k_j, Xr_j, Yr_j, color_j, selected_funct, m_j
            )
            # Guardar en session state
            st.session_state["julia_image"] = (img_bytes, filename_j)

            # Convertir el tiempo de ejecución a minutos y segundos
            minutes_j = math.floor(execution_time_j / 60)
            seconds_j = execution_time_j % 60

            # Formatear el tiempo en minutos y segundos
            time_str = (
                f"{minutes_j} minutos y {seconds_j} segundos"
                if minutes_j > 0
                else f"{round(seconds_j, 2)} segundos"
            )
            st.success(f"Tiempo de ejecución: {time_str}")
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