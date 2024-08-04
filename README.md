# fh-plotly

Use Plotly charts with [FastHTML](https://github.com/AnswerDotAI/fasthtml).


## Installation

```bash
pip install fh-plotly
```

Make sure to add the right headers to your FastHTML app:

```python
from fasthtml.common import fast_app
from fh_plotly import plotly_headers


app, rt = fast_app(
    hdrs = plotly_headers
)
```

This ensures that the required javascript and css files are always loaded.

## Examples

Run examples/test_app.py to see the examples in action.

```bash
python examples/test_app.py
```

The gist of conversion to Plotly is with the `plotly2fasthtml` function.

```python
from fh_plotly import plotly2fasthtml

def generate_line_chart():
    df = pd.DataFrame({'y': [1, 2, 3, 2], 'x': [3, 1, 2, 4]})
    fig = px.line(df, x='x', y='y')
    return plotly2fasthtml(fig)
```

## Contributing

Feel free to open an issue or a pull request to add FastHTML Plotly functionality.

Please install with `poetry install` for contributing.

```bash
poetry install
```
