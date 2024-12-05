import fastcore
import pandas as pd
import plotly.express as px
import pytest

from fh_plotly import plotly2fasthtml


def test_line():
    df = pd.DataFrame({"y": [1, 2, 3, 2], "x": [3, 1, 2, 4]})
    fig = px.line(df, x="x", y="y")
    html_div = plotly2fasthtml(fig)
    assert isinstance(html_div, fastcore.xml.FT)


def test_bar():
    df = pd.DataFrame({"y": [1, 2, 3], "x": ["A", "B", "C"]})
    fig = px.bar(df, x="x", y="y")
    html_div = plotly2fasthtml(fig)
    assert html_div is not None
    assert isinstance(html_div, fastcore.xml.FT)


def test_scatter():
    df = pd.DataFrame({"y": [1, 2, 3, 2], "x": [3, 1, 2, 4], "size": [10, 20, 30, 40]})
    fig = px.scatter(df, x="x", y="y", size="size")
    html_div = plotly2fasthtml(fig)
    assert html_div is not None
    assert isinstance(html_div, fastcore.xml.FT)


def test_3d_scatter():
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 11, 12, 13], "z": [100, 110, 120, 130]})
    fig = px.scatter_3d(df, x="x", y="y", z="z")
    html_div = plotly2fasthtml(fig)
    assert html_div is not None
    assert isinstance(html_div, fastcore.xml.FT)


def test_3d_surface():
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 11, 12, 13], "z": [100, 110, 120, 130]})
    fig = px.scatter_3d(df, x="x", y="y", z="z")
    fig.update_traces(marker=dict(size=5, opacity=0.8))
    html_div = plotly2fasthtml(fig)
    assert html_div is not None
    assert isinstance(html_div, fastcore.xml.FT)


@pytest.mark.e2e
def test_callback(callback_server, page):
    page.goto("localhost:5001")
    click_layer = page.locator("svg.main-svg rect.nsewdrag.drag")
    click_layer.click(position={"x": 630, "y": 250})
    callback_text = page.get_by_test_id("callback-display").inner_text()

    assert callback_text.startswith("Server received click on (3.6, 5.0) from plot")
