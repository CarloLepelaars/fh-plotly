# fh-plotly

![Downloads](https://img.shields.io/pypi/dm/fh-plotly)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Use Plotly charts with [FastHTML](https://github.com/AnswerDotAI/fasthtml).


## Installation

```bash
pip install fh-plotly
```

Make sure to add the right headers to your FastHTML app:

```python
from fasthtml.common import fast_app
from fh_plotly import plotly_headers

app, rt = fast_app(hdrs=plotly_headers)
```

This ensures that the required javascript and css files are always loaded.

## Examples

Run `examples/test_app.py` to see some basic plots.

```bash
python examples/test_app.py
```

The gist of conversion to Plotly is the `plotly2fasthtml` function.

```python
from fh_plotly import plotly2fasthtml

def generate_line_chart():
    df = pd.DataFrame({'y': [1, 2, 3, 2], 'x': [3, 1, 2, 4]})
    fig = px.line(df, x='x', y='y')
    return plotly2fasthtml(fig)
```

## Contributing

Feel free to open an issue or a pull request. 
Make sure to do an editable install with dev dependencies when working on contributions.

```bash
pip install uv
uv sync
```

To run tests:

```bash
pytest -s
```

The goal is to keep `fh-plotly` lightweight and compatible with Python 3.10+.
