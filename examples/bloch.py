import numpy as np
from fasthtml.common import *
import plotly.graph_objects as go

from fh_plotly import plotly2fasthtml, plotly_headers


app, rt = fast_app(hdrs=plotly_headers)

# Define the T gate
H_gate = np.array([[1, 1],
                   [1, -1j]]) / np.sqrt(2)

Y_gate = np.array([[0, -1j],
                     [1j, 0]])

Z_gate = np.array([[1, 0],
                     [0, -1]])

state_0 = np.array([1, 0])

new_state = H_gate @ state_0

def bloch_coords(state):
    alpha, beta = state[0], state[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return x, y, z

x, y, z = bloch_coords(new_state)
phi, theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
xs = np.sin(theta) * np.cos(phi)
ys = np.sin(theta) * np.sin(phi)
zs = np.cos(theta)

alpha = new_state[0]
beta = new_state[1]
state_annotation = f"|ψ> = {alpha:.2f}|0> + {beta:.2f}|1>"


fig = go.Figure()
fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.5, colorscale='Blues', showscale=False))
fig.add_trace(go.Scatter3d(
    x=[0, x],
    y=[0, y],
    z=[0, z],
    mode='lines+markers+text',
    marker=dict(size=5, color='red'),
    line=dict(color='red', width=5),
    # text=["", state_annotation],
    textposition="top center",
    name=state_annotation
))

fig.add_trace(go.Scatter3d(
    x=[0, 0],
    y=[0, 0],
    z=[1, -1],
    mode='markers',
    marker=dict(size=5, color='black'),
    hovertext=['Basis State |0>', 'Basis state: |1>'],
    showlegend=False
))

boundary_phi = np.linspace(0, 2 * np.pi, 100)
boundary_x = np.cos(boundary_phi)
boundary_y = np.sin(boundary_phi)
boundary_z = np.zeros_like(boundary_phi)

fig.add_trace(go.Scatter3d(
    x=boundary_x,
    y=boundary_y,
    z=boundary_z,
    mode='lines',
    line=dict(color='black', width=2),
    showlegend=False
))

fig.add_trace(go.Scatter3d(
    x=[-1, 1],
    y=[0, 0],
    z=[0, 0],
    mode='lines',
    line=dict(color='black', width=2),
    showlegend=False
))

fig.add_trace(go.Scatter3d(
    x=[0, 0],
    y=[-1, 1],
    z=[0, 0],
    mode='lines',
    line=dict(color='black', width=2),
    showlegend=False
))

fig.add_trace(go.Scatter3d(
    x=[0, 0],
    y=[0, 0],
    z=[-1, 1],
    mode='lines',
    line=dict(color='black', width=2),
    showlegend=False
))

fig.update_layout(
    title='Bloch Sphere',
    scene=dict(
        xaxis=dict(title='X', range=[-1.2, 1.2], tickvals=[-1, 0, 1], ticktext=["|-⟩", "+/sqrt(2)", "|+⟩"]),
        yaxis=dict(title='Y', range=[-1.2, 1.2], tickvals=[-1, 0, 1], ticktext=["|-i⟩", "i/sqrt(2)" "|i⟩"]),
        zaxis=dict(title='Z', range=[-1.2, 1.2], tickvals=[-1, 0, 1], ticktext=["|1⟩", "1/sqrt(2)", "|0⟩"]),
        aspectmode='cube'
    )
)
bloch_plot = plotly2fasthtml(fig)

@app.get('/')
def home():
    return Div(bloch_plot)

serve()
