
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from io import BytesIO
import base64
from streamlit.components.v1 import html

st.title("📈 Growth Model: Δ(t) and G(t) with Animation")

# --- Inputs ---
x = st.slider("x (Core Effort)", 0, 100, 42)
R = st.slider("R (Resources)", 0, 100, 36)
E = st.slider("Efficiency", 0.1, 3.0, 1.2)
T = st.slider("Time Influence", 0.1, 5.0, 1.0)
C = st.slider("Cost / Friction", 0, 500, 100)
Vmax = st.slider("Max Variables (Complexity Cap)", 1, 30, 12)

# --- Time Axis ---
t = np.linspace(0, 30, 300)

# --- Strategic Boost Components ---
R_t = np.where(t >= 5, 40, 0)
B_t = 10 * (np.sin(0.9 * t) > 0)
V_t = np.clip(0.5 * t, 0, Vmax)
S_t = (R_t * B_t) * (1 - V_t / Vmax)

# --- Model Calculations ---
I = 9 * x + 9 * R
M = E / T
F = C + 612 * np.pi
Delta_t = (M * (I + S_t) - F) / 51
G_t = 3 * Delta_t

# --- Static Plot ---
fig_static, ax_static = plt.subplots(figsize=(10, 4))
ax_static.plot(t, Delta_t, label="Δ(t)", color='blue')
ax_static.plot(t, G_t, label="G(t)", color='green')
ax_static.axhline(0, linestyle='--', color='gray')
ax_static.set_title("Δ(t) and G(t) Over Time")
ax_static.set_xlabel("Time (t)")
ax_static.set_ylabel("Value")
ax_static.legend()
ax_static.grid(True)
st.pyplot(fig_static)

# --- Animation ---
fig_anim, ax_anim = plt.subplots()
line1, = ax_anim.plot([], [], 'b-', label='Δ(t)')
line2, = ax_anim.plot([], [], 'g-', label='G(t)')
ax_anim.set_xlim(0, 30)
ax_anim.set_ylim(min(np.min(Delta_t), np.min(G_t)) - 10, max(np.max(Delta_t), np.max(G_t)) + 10)
ax_anim.set_xlabel("Time (t)")
ax_anim.set_ylabel("Value")
ax_anim.set_title("Animated Growth Model")
ax_anim.legend()
ax_anim.grid(True)

xdata, ydata1, ydata2 = [], [], []

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

def update(frame):
    t_point = t[frame]
    delta_val = Delta_t[frame]
    g_val = G_t[frame]

    xdata.append(t_point)
    ydata1.append(delta_val)
    ydata2.append(g_val)

    line1.set_data(xdata, ydata1)
    line2.set_data(xdata, ydata2)
    return line1, line2

ani = FuncAnimation(fig_anim, update, frames=len(t), init_func=init, blit=True)

# Convert to gif and embed
buf = BytesIO()
ani.save(buf, format='gif', fps=30)
data = base64.b64encode(buf.getbuffer()).decode("utf-8")
html_gif = f'<img src="data:image/gif;base64,{data}"/>'
st.markdown("### 🌀 Animated Growth Progression")
html(html_gif, height=400)
