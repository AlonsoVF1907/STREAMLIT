import math
import re
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Calculadora Científica Web", page_icon="🧮", layout="centered"
)

# Estilo personalizado para el teclado y la pantalla
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        height: 3.2rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 8px;
    }
    .pantalla-resultado {
        font-family: 'Courier New', monospace;
        font-size: 2rem;
        background-color: #1e1e2e;
        color: #a6e3a1;
        padding: 15px;
        border-radius: 10px;
        text-align: right;
        margin-bottom: 20px;
        word-wrap: break-word;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🧮 Calculadora Científica Web")

# Inicializar variable de estado para la expresión
if "expresion" not in st.session_state:
    st.session_state.expresion = ""


# Función para evaluar la expresión matemática
def evaluar_expresion(expr):
    try:
        if not expr.strip():
            return ""

        # Reemplazos de símbolos por sintaxis de Python/Math
        expr_eval = expr.replace("π", "math.pi")
        expr_eval = expr_eval.replace("e", "math.e")
        expr_eval = expr_eval.replace("^", "**")
        expr_eval = expr_eval.replace("√", "math.sqrt")
        expr_eval = expr_eval.replace("÷", "/")
        expr_eval = expr_eval.replace("×", "*")

        # Funciones trigonométricas (evaluadas en grados)
        expr_eval = expr_eval.replace("sin(", "math.sin(math.radians(")
        expr_eval = expr_eval.replace("cos(", "math.cos(math.radians(")
        expr_eval = expr_eval.replace("tan(", "math.tan(math.radians(")

        # Conversiones explicitas
        expr_eval = expr_eval.replace("rad(", "math.radians(")
        expr_eval = expr_eval.replace("deg(", "math.degrees(")

        # Logaritmos
        expr_eval = expr_eval.replace("ln(", "math.log(")
        expr_eval = expr_eval.replace("log(", "math.log10(")

        # Factorial (remplaza n! por math.factorial(n))
        expr_eval = re.sub(r"(\d+)\!", r"math.factorial(\1)", expr_eval)

        # Autocierre de paréntesis incompletos
        abiertos = expr_eval.count("(")
        cerrados = expr_eval.count(")")
        if abiertos > cerrados:
            expr_eval += ")" * (abiertos - cerrados)

        # Evaluar
        resultado = eval(expr_eval, {"math": math})

        if isinstance(resultado, float) and resultado.is_integer():
            return str(int(resultado))
        else:
            return str(round(resultado, 8))

    except ZeroDivisionError:
        return "Error: División por 0"
    except Exception:
        return "Error de Sintaxis"


# Callback para manejar las pulsaciones de los botones
def al_presionar(val):
    if val == "C":
        st.session_state.expresion = ""
    elif val == "⌫":
        st.session_state.expresion = st.session_state.expresion[:-1]
    elif val == "=":
        st.session_state.expresion = evaluar_expresion(
            st.session_state.expresion
        )
    elif val in ["sin", "cos", "tan", "ln", "log", "√", "rad", "deg"]:
        st.session_state.expresion += f"{val}("
    elif val == "x!":
        st.session_state.expresion += "!"
    else:
        st.session_state.expresion += str(val)


# Mostrar la pantalla con la expresión actual
pantalla_texto = (
    st.session_state.expresion if st.session_state.expresion else "0"
)
st.markdown(
    f'<div class="pantalla-resultado">{pantalla_texto}</div>',
    unsafe_allow_html=True,
)

# Definición del teclado en cuadrícula
matriz_botones = [
    ["rad", "deg", "x!", "(", ")"],
    ["sin", "cos", "tan", "π", "e"],
    ["ln", "log", "√", "^", "÷"],
    ["7", "8", "9", "×", "C"],
    ["4", "5", "6", "-", "⌫"],
    ["1", "2", "3", "+", "="],
    ["0", ".", "+/-"],
]

# Renderizado de botones
for fila in matriz_botones:
    cols = st.columns(len(fila))
    for i, texto in enumerate(fila):
        # Asignar tipos/colores de botón según el tipo de acción
        tipo_boton = "secondary"
        if texto in ["=", "C", "⌫"]:
            tipo_boton = "primary"

        cols[i].button(
            texto,
            key=f"btn_{texto}_{fila}",
            type=tipo_boton,
            use_container_width=True,
            on_click=al_presionar,
            args=(texto,),
        )