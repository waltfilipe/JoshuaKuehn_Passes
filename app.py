import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

st.set_page_config(layout="wide")

st.title("Pass Map + Statistics")

# ==========================
# Coordinates
# ==========================
cords = [
    # GAME 1
    (111.86,67.93),(112.36,77.90),
    (89.09,35.51),(117.68,18.72),
    (116.19,73.25),(105.88,72.42),
    (100.39,64.77),(104.88,57.29),
    (91.58,59.28),(81.61,68.92),
    (114.86,58.78),(109.21,47.65),
    (103.05,64.77),(99.73,77.90),
    (115.02,69.26),(109.70,20.22),
    (85.27,50.14),(75.79,41.83),
    (76.29,26.37),(65.98,22.38),
    (66.48,48.48),(73.13,73.25),
    (56.18,46.48),(66.98,67.10),
    (117.85,9.25),(101.06,4.92),
    (67.81,43.16),(66.65,55.79),
    (99.06,50.31),(95.41,57.29),
    (91.25,46.98),(104.22,27.70),

    # GAME 2
    (49.53,75.24),(41.05,75.41),
    (87.26,60.61),(73.13,59.12),
    (110.87,50.81),(110.37,36.68),
    (93.08,73.25),(85.77,64.10),
    (89.09,51.97),(91.75,36.18),
    (65.15,26.20),(57.67,34.68),
    (84.10,9.08),(79.95,10.58),
    (78.12,3.26),(76.29,7.09),
    (94.91,60.11),(101.56,49.64),
    (84.27,62.44),(75.46,74.91),
    (103.22,45.15),(103.39,32.52),
    (88.59,62.94),(97.24,76.07),
    (111.86,36.01),(110.87,41.50),
    (105.05,24.21),(98.57,40.17),
    (108.04,40.33),(109.37,28.36),
    (78.29,30.52),(92.75,6.42)
]

# ==========================
# Classification
# ==========================
game1_labels = [
    "certo","certo","errado","errado",
    "certo","errado","certo","errado",
    "certo","certo","certo","errado",
    "certo","errado","errado","certo"
]

game2_labels = [
    "errado","certo","assist","certo",
    "certo","certo","errado","errado",
    "errado","certo","certo","certo",
    "assist","certo","certo","certo"
]

all_labels = game1_labels + game2_labels

# ==========================
# DataFrame
# ==========================
passes = []

for i in range(0, len(cords), 2):
    start = cords[i]
    end = cords[i+1]
    numero = int(i/2)
    
    passes.append({
        "numero": numero + 1,
        "x_start": start[0],
        "y_start": start[1],
        "x_end": end[0],
        "y_end": end[1],
        "label": all_labels[numero]
    })

df = pd.DataFrame(passes)

# ==========================
# Metrics
# ==========================
goal_x, goal_y = 120, 40

df["dist_inicio"] = np.sqrt((goal_x - df.x_start)**2 + (goal_y - df.y_start)**2)
df["dist_fim"] = np.sqrt((goal_x - df.x_end)**2 + (goal_y - df.y_end)**2)

df["ganho"] = df["dist_inicio"] - df["dist_fim"]

df["progressivo"] = df["ganho"] >= 10

# A pass is considered successful if it is "certo" or an "assist"
df["certo"] = df["label"].isin(["certo", "assist"])
df["errado"] = df["label"] == "errado"
df["assist"] = df["label"] == "assist"

# ==========================
# Classifications
# ==========================
df["direita"] = df["x_end"] > df["x_start"]
df["esquerda"] = df["x_end"] < df["x_start"]

df["proprio_campo"] = df["x_start"] < 60
df["campo_adversario"] = df["x_start"] >= 60

df["ultimo_terco"] = df["x_end"] >= 80

# ==========================
# Plot
# ==========================
pitch = Pitch(
    pitch_type='statsbomb',
    pitch_color='#f5f5f5',
    line_color='#4a4a4a'
)

fig, ax = pitch.draw(figsize=(10,7))

# Final Third highlight
ax.axvline(x=80, color='#FFD54F', linewidth=1.5, alpha=0.25)

for _, row in df.iterrows():

    # Subtle colors setup
    if row["label"] == "errado":
        color = (0.9, 0.4, 0.4, 0.6)  # Subtle light red
        width = 1.6
    elif row["label"] == "assist":
        color = (0.4, 0.6, 1.0, 0.9)  # Subtle light blue
        width = 2.5
    else:  # "certo"
        color = (0.4, 0.8, 0.4, 0.7)  # Subtle light green
        width = 1.8

    pitch.arrows(
        row.x_start, row.y_start,
        row.x_end, row.y_end,
        color=color,
        width=width,
        headwidth=3,
        headlength=3,
        ax=ax
    )

ax.set_title("Pass Map", fontsize=16, fontweight='bold', pad=10)

# Attack Arrow
ax.annotate('', xy=(70, 83), xytext=(50, 83),
    arrowprops=dict(arrowstyle='->', color='#4a4a4a', lw=1.2))
ax.text(60, 86, "Attack Direction", ha='center', va='center', 
    fontsize=8, color='#4a4a4a', fontweight='bold')

# ==========================
# Legend
# ==========================
legend_elements = [
    Line2D([0], [0], color=(0.4, 0.8, 0.4, 0.7), lw=3, label='Successful Pass'),
    Line2D([0], [0], color=(0.9, 0.4, 0.4, 0.6), lw=3, label='Unsuccessful Pass'),
    Line2D([0], [0], color=(0.4, 0.6, 1.0, 0.9), lw=3, label='Assist'),
]

ax.legend(
    handles=legend_elements,
    loc='upper left',
    frameon=True,
    facecolor='white',
    edgecolor='black',
    framealpha=1
)

# ==========================
# Render Plot
# ==========================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.pyplot(fig)

# ==========================
# Dashboard Statistics
# ==========================
total = len(df)

passes_certos = df["certo"].sum()
passes_errados = df["errado"].sum()
total_assists = df["assist"].sum()
perc_certos = passes_certos / total * 100 if total > 0 else 0

prog = df[df["progressivo"]]
prog_total = len(prog)
prog_certos = prog["certo"].sum()
perc_prog = prog_total / total * 100 if total > 0 else 0

passes_direita = df["direita"].sum()
passes_esquerda = df["esquerda"].sum()

ultimo_terco_certos = df[df["ultimo_terco"] & df["certo"]].shape[0]

pc = df[df["proprio_campo"]]
pc_certos = pc["certo"].sum()
pc_errados = pc["errado"].sum()
pc_perc = pc_certos / len(pc) * 100 if len(pc) > 0 else 0

ca = df[df["campo_adversario"]]
ca_certos = ca["certo"].sum()
ca_errados = ca["errado"].sum()
ca_perc = ca_certos / len(ca) * 100 if len(ca) > 0 else 0

# ==========================
# Dashboard Layout
# ==========================
st.subheader("📊 Pass Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Passes", total)
col2.metric("% Accuracy", f"{perc_certos:.1f}%")
col3.metric("Progressive Passes", prog_total)
col4.metric("% Progressive", f"{perc_prog:.1f}%")

st.divider()

col5, col6, col7, col8 = st.columns(4)

col5.metric("→ Right", passes_direita)
col6.metric("← Left", passes_esquerda)
col7.metric("Final Third Passes", ultimo_terco_certos)
col8.metric("Assists", total_assists)  # Added metric for Assists

st.divider()

col9, col10 = st.columns(2)

with col9:
    st.markdown("### Own Field")
    st.metric("% Accuracy", f"{pc_perc:.1f}%")
    st.write(f"Acc: {pc_certos} | Inacc: {pc_errados}")

with col10:
    st.markdown("### Opponent Field")
    st.metric("% Accuracy", f"{ca_perc:.1f}%")
    st.write(f"Acc: {ca_certos} | Inacc: {ca_errados}")
