import plotly.data
import plotly.express as px
from fasthtml import serve, ft
from fasthtml.fastapp import fast_app
from fh_plotly import plotly_headers, plotly2fasthtml
from fh_plotly.p2fh import OnClick

app, rt = fast_app(hdrs=(plotly_headers,), live=True)


@rt("/", methods=["GET"])
def _():
    data = plotly.data.iris()
    plot = px.scatter(data, x="sepal_width", y="sepal_length", color="species")

    return ft.Main(
        ft.H1("Plotly Callback Example"),
        plotly2fasthtml(
            plot,
            callbacks=[OnClick(hx_post="/click", hx_target="#callback-display")],
        ),
        ft.H2("Click a marker to trigger a callback!"),
        ft.P(id="callback-display"),
        cls="container",
    )


@rt("/click", methods=["POST"])
def _(x: float, y: float, plot_id: str):
    return f"Server received click on ({x}, {y}) from plot: {plot_id}."


serve()
