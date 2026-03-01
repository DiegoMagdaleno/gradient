import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import sympify, latex
import pandas as pd

st.set_page_config(
    page_title="Descenso del Gradiente • Elegancia",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ELEGANT HIGH-CONTRAST SERIF UI CUSTOM CSS ---
st.markdown("""
<style>
    /* Import sophisticated serif and sans fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #000000;
    }
    
    h1, h2, h3, h4, .main-title {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        color: #000000;
    }

    /* Main Background: Pure & Airy with subtle grid */
    .stApp {
        background-color: #ffffff;
        background-image: radial-gradient(#d1d5db 0.8px, #ffffff 0.8px);
        background-size: 30px 30px;
    }
    
    /* Ensure content stays centered and doesn't overlap with sidebar */
    .block-container {
        max-width: 1200px !important;
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* Sidebar: Clean contrast + WIDER BY DEFAULT ON DESKTOP */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #000000;
    }
    
    @media (min-width: 768px) {
        /* Set custom width */
        [data-testid="stSidebar"] {
            min-width: 480px !important;
            max-width: 480px !important;
        }
        /* IMPORTANT: Shift the main content so it doesn't overlap the fixed sidebar */
        [data-testid="stSidebarCollapsedControl"] ~ section.main {
            margin-left: 480px !important;
        }
        /* If sidebar is collapsed, margin should go back to 0 */
        [data-testid="stSidebar"][aria-expanded="false"] ~ section.main {
            margin-left: 0 !important;
        }
    }
    
    /* Responsive Sidebar Content */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    .main-title {
        font-size: 4rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
        letter-spacing: -1.5px;
    }
    .sub-title {
        text-align: center;
        color: #374151;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-style: italic;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    .calc-for {
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        color: #000000;
        font-size: 1.5rem;
        margin-top: 2rem;
        font-weight: 700;
    }
    
    .stLatex {
        text-align: center !important;
        padding: 1.5rem 0 3.5rem 0;
    }
    .katex-display {
        font-size: 4.5rem !important;
        color: #000000 !important;
        margin: 0 !important;
    }

    /* Buttons */
    .stButton > button {
        background: #ffffff;
        border: 2px solid #000000;
        color: #000000;
        border-radius: 0px;
        padding: 0.6rem;
        font-weight: 700;
        transition: all 0.2s ease;
        text-transform: lowercase;
        font-variant: small-caps;
        letter-spacing: 1.5px;
    }
    .stButton > button:hover {
        background: #000000;
        color: #ffffff;
    }
    
    [data-testid="stFormSubmitButton"] > button {
        background: #000000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0px !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        padding: 1.2rem !important;
        letter-spacing: 3px;
        box-shadow: 6px 6px 0px #eeeeee !important;
        text-transform: uppercase;
        width: 100%;
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input {
        border: none !important;
        border-bottom: 2px solid #000000 !important;
        background: transparent !important;
        border-radius: 0 !important;
        color: #000000 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-align: center;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 2px solid #000000;
        padding: 2.5rem;
        border-radius: 0;
        box-shadow: 12px 12px 0px #f3f4f6;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        color: #000000;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.85rem;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        color: #000000;
        font-weight: 700;
        font-size: 3.2rem;
    }

    /* Table Section Header */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        border-bottom: 2px solid #000000;
        margin-top: 5rem;
        margin-bottom: 2rem;
        padding-bottom: 0.5rem;
    }
    
    /* Responsive adjustment for Mobile */
    @media (max-width: 768px) {
        .katex-display {
            font-size: 2.8rem !important;
        }
        .main-title {
            font-size: 2.5rem !important;
        }
        .sub-title {
            font-size: 1.2rem !important;
        }
        [data-testid="stSidebar"] {
            border-right: none;
            border-bottom: 2px solid #000000;
            min-width: 100% !important;
        }
        .stButton > button {
            padding: 0.4rem;
            font-size: 0.7rem;
            letter-spacing: 1px;
        }
        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
        }
        
        /* HIDDEN ON MOBILE: Numbers, parens, backspace */
        div:has(> .hide-numpad-mobile) ~ div[data-testid="stHorizontalBlock"] {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Math Engine Logic
def python_to_latex(expr_str):
    if not expr_str or expr_str.strip() == "": return "?"
    try:
        clean_expr = expr_str.replace("^", "**")
        expr = sympify(clean_expr)
        return latex(expr)
    except:
        return expr_str

def evaluar_funcion(x, expr):
    contexto = {
        'x': x, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
        'abs': np.abs, 'pi': np.pi, 'e': np.e
    }
    try:
        return eval(expr.replace("^", "**"), {"__builtins__": {}}, contexto)
    except Exception:
        return None

def gradiente_numerico(x, expr, h=1e-7):
    f_mas = evaluar_funcion(x + h, expr)
    f_menos = evaluar_funcion(x - h, expr)
    if f_mas is None or f_menos is None: return None
    return (f_mas - f_menos) / (2 * h)

def descenso_gradiente(x0, lr, n_iter, expr):
    hx = [x0]
    f0 = evaluar_funcion(x0, expr)
    if f0 is None: return None, None
    hf = [f0]
    x = x0
    for _ in range(n_iter):
        grad = gradiente_numerico(x, expr)
        if grad is None: break
        x = x - lr * grad
        f_val = evaluar_funcion(x, expr)
        if f_val is None: break
        hx.append(x)
        hf.append(f_val)
        if abs(grad) < 1e-8: break
    return hx, hf

# Header Section
st.markdown('<div class="main-title">El Descenso del Gradiente</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Una Exploración de la Convergencia Matemática</div>', unsafe_allow_html=True)

if 'func_expr' not in st.session_state:
    st.session_state.func_expr = "x**2 + 5*x"

# Center Stage: Live Equation Rendering
st.markdown('<div class="calc-for">Calculando para:</div>', unsafe_allow_html=True)
latex_display = python_to_latex(st.session_state.func_expr)
st.latex(rf"f(x) = {latex_display}")

# Sidebar Panel
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #000; font-weight: 800;'>CONFIGURACIÓN</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 0; border-top: 3px solid #000; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Live Input
    st.markdown("<label style='font-size: 0.9rem; color: #000; font-weight: 800; letter-spacing: 2px; display: block; text-align: center; margin-bottom: 10px;'>EXPRESIÓN MATEMÁTICA</label>", unsafe_allow_html=True)
    funcion_expr = st.text_input("f(x)", value=st.session_state.func_expr, key="func_input", label_visibility="collapsed")
    if funcion_expr != st.session_state.func_expr:
        st.session_state.func_expr = funcion_expr
        st.rerun()

    def mk_btn(label, val, col):
        if col.button(label, use_container_width=True, key=f"btn_{label}"):
            if label == 'C': st.session_state.func_expr = ""
            elif label == '⌫': st.session_state.func_expr = st.session_state.func_expr[:-1] if st.session_state.func_expr else ""
            else: st.session_state.func_expr += val
            st.rerun()

    # SECTION 1: FUNCTIONS (Always Visible)
    keyboard_funcs = [
        [("x", "x"), ("x²", "**2"), ("sin", "sin(")],
        [("cos", "cos("), ("exp", "exp("), ("log", "log(")],
        [("tan", "tan("), ("^", "**"), ("C", "")]
    ]
    for r in keyboard_funcs:
        cols = st.columns(len(r))
        for i, (lbl, val) in enumerate(r):
            mk_btn(lbl, val, cols[i])

    # MOBILE HIDE MARKER
    st.markdown('<div class="hide-numpad-mobile"></div>', unsafe_allow_html=True)

    # SECTION 2: NUMBERS AND SYMBOLS (Hidden on mobile)
    keyboard_nums = [
        [("(", "("), (")", ")"), ("⌫", "")],
        [("7", "7"), ("8", "8"), ("9", "9")],
        [("4", "4"), ("5", "5"), ("6", "6")],
        [("1", "1"), ("2", "2"), ("3", "3")],
        [("0", "0")]
    ]
    for r in keyboard_nums:
        cols = st.columns(len(r))
        for i, (lbl, val) in enumerate(r):
            mk_btn(lbl, val, cols[i])

    st.markdown("<hr style='border: 0; border-top: 3px solid #000; margin: 2rem 0;'>", unsafe_allow_html=True)
    
    with st.form("opt_params"):
        st.markdown("<label style='font-size: 0.85rem; color: #000; font-weight: 800; letter-spacing: 1px;'>TAMAÑO DEL PASO (α)</label>", unsafe_allow_html=True)
        learning_rate = st.number_input("α", min_value=0.0001, max_value=1.0, value=0.1, step=0.001, format="%.4f", label_visibility="collapsed")
        
        st.markdown("<label style='font-size: 0.85rem; color: #000; font-weight: 800; letter-spacing: 1px;'>PROFUNDIDAD DE ITERACIÓN</label>", unsafe_allow_html=True)
        num_iteraciones = st.slider("n", min_value=10, max_value=500, value=50, step=10, label_visibility="collapsed")
        
        st.markdown("<label style='font-size: 0.85rem; color: #000; font-weight: 800; letter-spacing: 1px;'>ORIGEN (x₀)</label>", unsafe_allow_html=True)
        x_inicial = st.number_input("x0", value=8.0, step=0.5, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        ejecutar = st.form_submit_button("INICIAR OPTIMIZACIÓN")

# Execution and Results
if 'hx' not in st.session_state: st.session_state.hx = None

if ejecutar and st.session_state.func_expr.strip():
    hx, hf = descenso_gradiente(x_inicial, learning_rate, num_iteraciones, st.session_state.func_expr)
    if hx:
        st.session_state.hx, st.session_state.hf = hx, hf
        st.session_state.params = {'lr': learning_rate, 'n_iter': num_iteraciones, 'x0': x_inicial, 'func': st.session_state.func_expr}
        st.session_state.error = False
    else:
        st.session_state.error = True

if st.session_state.hx and not st.session_state.get('error'):
    hx, hf = st.session_state.hx, st.session_state.hf
    params = st.session_state.params
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("MÍNIMO f(x)", f"{hf[-1]:.4f}")
    with c2: st.metric("PUNTO ÓPTIMO x*", f"{hx[-1]:.4f}")
    with c3: st.metric("ITERACIONES", f"{len(hx)-1}")

    st.markdown("<br><hr style='border: 0; border-top: 3px solid #000; margin: 3rem 0;'><br>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    
    x_range = np.linspace(min(hx)-2, max(hx)+2, 500)
    y_func = [evaluar_funcion(x, params['func']) for x in x_range]
    
    # Chart 1
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x_range, y=y_func, mode='lines', name='Función', line=dict(color='#cccccc', width=2)))
    fig1.add_trace(go.Scatter(x=hx, y=hf, mode='markers+lines', name='Trayectoria', marker=dict(color='#000000', size=6), line=dict(color='#000000', width=1.5)))
    fig1.add_trace(go.Scatter(x=[hx[-1]], y=[hf[-1]], mode='markers', name='Resultado', marker=dict(color='#ff0000', size=14, symbol='circle-open', line=dict(width=2.5))))
    fig1.update_layout(
        title="Topología de la Función",
        template="plotly_white",
        font=dict(family="Cormorant Garamond, serif", size=14, color="#000000"),
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    axis_style = dict(showgrid=True, gridcolor='#eeeeee', zeroline=True, zerolinecolor='#000000', tickfont=dict(color="#000000", size=12))
    fig1.update_xaxes(title="Eje X", **axis_style)
    fig1.update_yaxes(title="f(x)", **axis_style)
    g1.plotly_chart(fig1, use_container_width=True)

    # Chart 2
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=list(range(len(hf))), y=hf, mode='lines', name='Pérdida', line=dict(color='#000000', width=2)))
    fig2.update_layout(
        title="Curva de Convergencia",
        template="plotly_white",
        font=dict(family="Cormorant Garamond, serif", size=14, color="#000000"),
        height=450,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig2.update_xaxes(title="Iteración", **axis_style)
    fig2.update_yaxes(title="Valor", **axis_style)
    g2.plotly_chart(fig2, use_container_width=True)

    # Table Section
    st.markdown('<div class="section-header">Registro de Iteraciones</div>', unsafe_allow_html=True)
    df = pd.DataFrame({
        'Paso': range(len(hx)), 
        'Vector x': hx, 
        'Valor f(x)': hf,
        'Δ x': [hx[i] - hx[i-1] if i > 0 else 0.0 for i in range(len(hx))],
        'Δ f(x)': [hf[i] - hf[i-1] if i > 0 else 0.0 for i in range(len(hf))]
    })
    st.dataframe(df.style.format("{:.6f}"), use_container_width=True, hide_index=True)

st.markdown("""
<div style='text-align: center; margin-top: 8rem; padding: 4rem 2rem; border-top: 1px solid #000000; background-color: #f9fafb;'>
    <div style='font-family: Playfair Display, serif; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem;'>
        Creado por: Diego Magdaleno, Christopher Aladair
    </div>
    <div style='font-family: Cormorant Garamond, serif; font-size: 1.1rem; color: #374151; margin-bottom: 1.5rem;'>
        Materia: Métodos Numéricos | Maestría en Inteligencia Artificial | EdgeHub
    </div>
    <div style='font-family: Inter, sans-serif; font-size: 0.85rem; letter-spacing: 1px; color: #6b7280; text-transform: uppercase;'>
        Hecho con ❤️ y: 
        <span style='font-weight: 700; color: #000;'>Planeación: Gemini 3.1 Pro</span> • 
        <span style='font-weight: 700; color: #000;'>Programación: Claude Opus 4.6</span>
    </div>
</div>
""", unsafe_allow_html=True)
