import numpy as np
from fasthtml.common import *
import plotly.graph_objects as go

from fh_plotly import plotly2fasthtml, plotly_headers


app, rt = fast_app(hdrs=plotly_headers)

def plot_bloch(state: np.array):
    fig = go.Figure()

    # State vector coordinates
    alpha, beta = state[0], state[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    # Surface coordinates
    surface_phi, surface_theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
    xs = np.sin(surface_theta) * np.cos(surface_phi)
    ys = np.sin(surface_theta) * np.sin(surface_phi)
    zs = np.cos(surface_theta)
    fig.add_trace(go.Surface(x=xs, y=ys, z=zs, opacity=0.5, colorscale='Blues', showscale=False))

    fig.add_trace(go.Scatter3d(
        x=[0, x],
        y=[0, y],
        z=[0, z],
        mode='lines+markers+text',
        marker=dict(size=10, color='green'),
        line=dict(color='green', width=8),
        textposition="top center",
        showlegend=True,
        name=f"{alpha:.2f}|0⟩ + {beta:.2f}|1⟩"
    ))

    # Mark basis states
    fig.add_trace(go.Scatter3d(
        x=[0, 0, 1, -1, 0, 0],
        y=[0, 0, 0, 0, 1, -1],
        z=[1, -1, 0, 0, 0, 0],
        mode='markers',
        marker=dict(size=5, color='black'),
        hovertext=['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|i⟩', '|-i⟩'],
        showlegend=False,
        name="Basis states"
    ))

    # Add lines across axes
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
            showlegend=False,
            name="Axes"
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title=dict(text='X', font=dict(size=25)), 
                       range=[-1.2, 1.2], tickvals=[-1, 1], 
                       ticktext=["|-⟩", "|+⟩"],
                       tickfont=dict(size=15)),
            yaxis=dict(title=dict(text='Y', font=dict(size=25)), 
                       range=[-1.2, 1.2], tickvals=[-1, 1], 
                       ticktext=["|-i⟩", "|i⟩"],
                       tickfont=dict(size=15)),
            zaxis=dict(title=dict(text='Z', font=dict(size=25)), 
                       range=[-1.2, 1.2], tickvals=[-1, 1], 
                       ticktext=["|1⟩", "|0⟩"],
                       tickfont=dict(size=15)),
            aspectmode='cube',
        ),
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
    return plotly2fasthtml(fig)

def construct_state(gates: list[str]):
    state = np.array([1, 0]) # |0> basis state
    for gate in gates:
        state = single_qubit_gates[gate] @ state
    return state

def visualize_circuit(gates: list[str]):
    circuit = "|0⟩-" 
    for gate in gates:
        circuit += f"[{gate}]─"
    return circuit + "|" 

single_qubit_gates = {
    # Hadamard
    "H": np.array([[1, 1],
                   [1, -1]]) / np.sqrt(2),
    # Pauli matrices
    "X": np.array([[0, 1],
                   [1, 0]]),
    "Y": np.array([[0, -1j],
                   [1j, 0]]),
    "Z": np.array([[1, 0],
                   [0, -1]]),
    # Phase gates
    "S": np.array([[1, 0],
                   [0, 1j]]),
    "T": np.array([[1, 0],
                   [0, np.exp(1j * np.pi / 4)]])
}

def apply_gate(gate: str = None):
    global gates
    if gate:
        gates.append(gate)
    state = construct_state(gates)
    return Div(
        plot_bloch(state),
        H4(f"Quantum Circuit: {visualize_circuit(gates)}"),
        id="chart"
    )

# Construct gate routing and buttons for each qubit gate
gates = []
for gate in single_qubit_gates.keys():
    def create_apply_func(gate_name):
        def apply_func():
            return apply_gate(gate_name)
        return apply_func
    func = create_apply_func(gate)
    route_path = f'/{gate.lower()}'
    app.get(route_path)(func)

@app.get('/reset')
def reset():
    global gates
    gates = []
    return apply_gate()

buttons = [
    Button(gate, hx_get=f"/{gate.lower()}", hx_target="#chart", hx_swap="innerHTML",
           title=f"Apply {gate} gate")
    for gate in single_qubit_gates.keys()
] + [Button("Reset", hx_get="/reset", hx_target="#chart", hx_swap="innerHTML",
            title="Reset the circuit")]

desc = """
The Bloch Sphere is a 3D visualization of a quantum state. 
You can interact with the buttons (Qubit gates) to see how the state changes.
"""

@app.get('/')
def homepage():
    return Title("Interactive Bloch Sphere"), Main(P(desc),
                                                   *buttons, 
                                                   Div(apply_gate(), id="chart"),
                                                   H4("Available gates"),
                                                   P("- H: Hadamard gate. Puts the state in superposition. "),
                                                   P("- X: Pauli-X (NOT) gate. Flip around the X-Axis."),
                                                   P("- Y: Pauli-Y (\"bit-flip\") gate. Flip around the Y-Axis."),
                                                   P("- Z: Pauli-Z (\"phase-flip\") gate. Flip around the Z-Axis."),
                                                   P("- S: Phase gate. Rotates around the Z-axis by 90 degrees."),
                                                   P("- T: π/8 gate. Rotates around the Z-axis by 45 degrees."),)

serve()
