import numpy as np
from fasthtml.common import *
import plotly.graph_objects as go

from fh_plotly import plotly2fasthtml, plotly_headers

app, rt = fast_app(hdrs=plotly_headers)

single_qubit_gates = {
    "H": np.array([[1, 1],
                   [1, -1]]) / np.sqrt(2),
    "X": np.array([[0, 1],
                   [1, 0]]),
    "Y": np.array([[0, -1j],
                   [1j, 0]]),
    "Z": np.array([[1, 0],
                   [0, -1]]),
    "S": np.array([[1, 0],
                   [0, 1j]]),
    "T": np.array([[1, 0],
                   [0, np.exp(1j * np.pi / 4)]])
}

def plot_bloch(state):
    alpha, beta = state[0], state[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    phi, theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
    xs = np.sin(theta) * np.cos(phi)
    ys = np.sin(theta) * np.sin(phi)
    zs = np.cos(theta)
    state_annotation = display_state(state)

    fig = go.Figure()
    fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.5, colorscale='Blues', showscale=False))
    fig.add_trace(go.Scatter3d(
        x=[0, x],
        y=[0, y],
        z=[0, z],
        mode='lines+markers+text',
        marker=dict(size=5, color='green'),
        line=dict(color='green', width=5),
        textposition="top center",
        name=state_annotation,
        showlegend=True
    ))

    fig.update_layout(
    legend=dict(
        font=dict(size=20),
        x=0.05,        
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)', 
    ),
    margin=dict(l=0, r=0, t=0, b=0)  
    )

    fig.add_trace(go.Scatter3d(
        x=[0, 0, 1, -1, 0, 0],
        y=[0, 0, 0, 0, 1, -1],
        z=[1, -1, 0, 0, 0, 0],
        mode='markers',
        marker=dict(size=5, color='black'),
        hovertext=['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|i⟩', '|-i⟩'],
        showlegend=False
    ))

    boundary_phi = np.linspace(0, 2 * np.pi, 100)
    coords = [
        (np.cos(boundary_phi), np.sin(boundary_phi), np.zeros_like(boundary_phi)),
        (np.zeros_like(boundary_phi), np.cos(boundary_phi), np.sin(boundary_phi)),
        (np.cos(boundary_phi), np.zeros_like(boundary_phi), np.sin(boundary_phi)) 
    ]
    for x, y, z in coords:
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False
        ))

    fig.add_trace(go.Scatter3d(
        x=[x], 
        y=[y], 
        z=[z], 
        mode='markers',
        marker=dict(size=10, color='green', symbol='diamond-open'),
        showlegend=False
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', range=[-1.2, 1.2], tickvals=[-1, 0, 1], 
                       ticktext=["|-⟩", "1/√2", "|+⟩"]),
            yaxis=dict(title='Y', range=[-1.2, 1.2], tickvals=[-1, 0, 1], 
                       ticktext=["|-i⟩", "i/√2", "|i⟩"]),
            zaxis=dict(title='Z', range=[-1.2, 1.2], tickvals=[-1, 0, 1], 
                       ticktext=["|1⟩", "1/√2", "|0⟩"]),
            aspectmode='cube',
        ),
    )
    return plotly2fasthtml(fig)

gates = []

def display_state(state):
    """ Convert a quantum state vector to a LaTeX string. """
    alpha, beta = state[0], state[1]
    return f"{alpha:.2f}|0⟩ + {beta:.2f}|1⟩"

def construct_state(gates):
    # |0> basis state
    state = np.array([1, 0])
    for gate in gates:
        state = single_qubit_gates[gate] @ state
    return state

def apply_gate(gate=None):
    global gates
    if gate:
        gates.append(gate)
    state = construct_state(gates)
    return Div(
        Div(display_state(state)),
        Div(visualize_circuit(gates)),
        plot_bloch(state),
        id="chart"
    )

@app.get('/reset')
def reset():
    global gates
    gates = []
    return apply_gate()

def visualize_circuit(gates):
    circuit = "|ψ⟩" 
    for gate in gates:
        circuit += f"─[{gate}]─"
    return circuit + "| " 

for gate in single_qubit_gates.keys():
    def create_apply_func(gate_name):
        def apply_func():
            return apply_gate(gate_name)
        return apply_func
    func = create_apply_func(gate)
    route_path = f'/{gate.lower()}'
    app.get(route_path)(func)

buttons = [
    Button(gate, hx_get=f"/{gate.lower()}", hx_target="#chart", hx_swap="innerHTML")
    for gate in single_qubit_gates.keys()
] + [Button("Reset", hx_get="/reset", hx_target="#chart", hx_swap="innerHTML")]

@app.get('/')
def homepage():
    return Main(Title("Interactive Bloch Sphere"),
                Div(apply_gate(), id="chart"), *buttons)

serve()
