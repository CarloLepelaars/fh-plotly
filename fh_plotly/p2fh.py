from dataclasses import dataclass
from typing import Optional
from uuid import uuid4
from plotly.io import to_json
from fasthtml.common import Div, Script

plotly_headers = [
    Script(src="https://cdn.plot.ly/plotly-latest.min.js"),
    Script(src="/fhCallbacks.js"),
]


def plotly2fasthtml(chart, callbacks=None):
    chart_id = f"uniq-{uuid4()}"
    chart_json = to_json(chart)
    if callbacks:
        for callback in callbacks:
            callback.register_plot(chart_id)

    return Div(
        Script(
            f"""
        var plotly_data = {chart_json};
        Plotly.newPlot('{chart_id}', plotly_data.data, plotly_data.layout);
    """
        ),
        *(callbacks or []),
        id=chart_id,
    )


@dataclass
class OnClick:
    hx_post: str
    hx_target: str
    plot_id: Optional[str] = None

    def register_plot(self, plot_id):
        self.plot_id = plot_id

    def __ft__(self):
        if self.plot_id is None:
            raise ValueError(
                "The 'plot_id' needs to be set on initialization or the callback must "
                "be passed to the 'plotly2fasthtml' function in the 'callbacks' "
                "argument."
            )

        return Script(
            f"""
            fhPlotlyRegisterOnClick('{self.plot_id}', '{self.hx_post}', '{self.hx_target}');
        """
        )
