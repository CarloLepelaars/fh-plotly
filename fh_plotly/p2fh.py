from uuid import uuid4
from plotly.io import to_json
from fasthtml.common import Div, Script

plotly_headers = [
    Script(src="https://cdn.plot.ly/plotly-latest.min.js")
]

def plotly2fasthtml(chart):
    chart_id = f'uniq-{uuid4()}'
    chart_json = to_json(chart)
    return Div(Script(f"""
        var plotly_data = {chart_json};
        Plotly.newPlot('{chart_id}', plotly_data.data, plotly_data.layout);
    """), id=chart_id)
