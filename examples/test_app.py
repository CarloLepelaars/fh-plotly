from fasthtml.common import fast_app, serve, Div, H1, P
import pandas as pd
import plotly.express as px

from fh_plotly import plotly2fasthtml, plotly_headers


app, rt = fast_app(hdrs=plotly_headers)


def generate_line_chart():
    df = pd.DataFrame({"y": [1, 2, 3, 2], "x": [3, 1, 2, 4]})
    fig = px.line(df, x="x", y="y")
    return plotly2fasthtml(fig)


def generate_bar_chart():
    df = pd.DataFrame({"y": [1, 2, 3], "x": ["A", "B", "C"]})
    fig = px.bar(df, x="x", y="y")
    return plotly2fasthtml(fig)


def generate_scatter_chart():
    df = pd.DataFrame({"y": [1, 2, 3, 2], "x": [3, 1, 2, 4], "size": [10, 20, 30, 40]})
    fig = px.scatter(df, x="x", y="y", size="size")
    return plotly2fasthtml(fig)


def generate_3d_scatter_chart():
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 11, 12, 13], "z": [100, 110, 120, 130]})
    fig = px.scatter_3d(df, x="x", y="y", z="z")
    return plotly2fasthtml(fig)


@app.get("/")
def home():
    return Div(H1("Plotly Charts Demo with FastHTML"), P("Plot 1: Line Chart"), Div(generate_line_chart()), P("Plot 2: Bar Chart"), Div(generate_bar_chart()), P("Plot 3: Scatter Chart"), Div(generate_scatter_chart()), P("Plot 4: 3D Scatter Chart"), Div(generate_3d_scatter_chart()))


serve()
