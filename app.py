Python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página en Streamlit
st.title("Simulador de Intercepción de Proyectiles 🚀")
st.markdown("Calcula la velocidad requerida para que dos objetos colisionen en el aire.")

# Parámetros en la barra lateral
st.sidebar.header("Parámetros de Lanzamiento")
g = 9.8134  # El valor calculado en tu tablero

# Objeto 1 (Izquierda)
v1 = st.sidebar.slider("Velocidad Inicial Objeto 1 (m/s)", 10.0, 50.0, 25.0)
alpha1 = st.sidebar.slider("Ángulo Objeto 1 (grados)", 10, 80, 45)

# Configuración del Objeto 2 (Derecha)
distancia = st.sidebar.slider("Distancia entre objetos (m)", 20.0, 100.0, 50.0)
alpha2 = st.sidebar.slider("Ángulo Objeto 2 (grados)", 10, 80, 60)

# --- CÁLCULOS MATEMÁTICOS ---
# Convertir ángulos a radianes
rad1 = np.radians(alpha1)
rad2 = np.radians(alpha2)

# Para que se intercepten en X e Y al mismo tiempo:
# v1*cos(a1)*t = d - v2*cos(a2)*t  => t_choque = d / (v1*cos(a1) + v2*cos(a2))
# Pero también v1*sin(a1)*t = v2*sin(a2)*t => v2 = v1 * sin(a1) / sin(a2)

# 1. Calcular la velocidad requerida para el objeto 2
v2_requerida = v1 * np.sin(rad1) / np.sin(rad2)

# 2. Calcular el tiempo exacto del choque
t_choque = distancia / (v1 * np.cos(rad1) + v2_requerida * np.cos(rad2))

# 3. Calcular las coordenadas del choque
x_choque = v1 * np.cos(rad1) * t_choque
y_choque = v1 * np.sin(rad1) * t_choque - 0.5 * g * (t_choque**2)

# --- GENERAR TRAYECTORIAS PARA GRAFICAR ---
t_total = np.linspace(0, t_choque, 100)

# Trayectoria 1
x1 = v1 * np.cos(rad1) * t_total
y1 = v1 * np.sin(rad1) * t_total - 0.5 * g * (t_total**2)

# Trayectoria 2
x2 = distancia - (v2_requerida * np.cos(rad2) * t_total)
y2 = v2_requerida * np.sin(rad2) * t_total - 0.5 * g * (t_total**2)

# --- MOSTRAR RESULTADOS ---
st.subheader("Resultados del Cálculo")
if y_choque > 0:
    st.success(f"¡Intercepción exitosa! El Objeto 2 necesita una velocidad inicial de: **{v2_requerida:.2f} m/s**")
    st.info(f"Colisionan en el punto **({x_choque:.2f}m, {y_choque:.2f}m)** a los **{t_choque:.2f} segundos**.")
else:
    st.error("Con estos ángulos, el choque ocurriría bajo el suelo. ¡Ajusta los parámetros!")

# --- GRÁFICO ESTILIZADO ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x1, y1, label="Objeto 1 (Izquierda)", color="#1f77b4", linewidth=2, linestyle="--")
ax.plot(x2, y2, label="Objeto 2 (Derecha)", color="#ff7f0e", linewidth=2, linestyle="--")
ax.scatter([x_choque], [y_choque], color="red", s=100, zorder=5, label="Punto de Impacto 💥")

# Estética del gráfico
ax.set_title("Trayectorias de Intercepción", fontsize=14, fontweight='bold')
ax.set_xlabel("Distancia Horizontal (m)")
ax.set_ylabel("Altura (m)")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
ax.set_ylim(bottom=0)

st.pyplot(fig)
