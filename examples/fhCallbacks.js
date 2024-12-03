const fhPlotlyRegisterOnClick = (plotId, hxPostEndpoint, hxTarget) => {
    const plotlyPlot = document.getElementById(plotId);
    plotlyPlot.on('plotly_click', (data) => {
        const point = data.points[0];
        const x = point.x;
        const y = point.y;
        const payload = new FormData();
        payload.append('x', x);
        payload.append('y', y);
        payload.append('plot_id', plotId);
        htmx.ajax("POST", hxPostEndpoint, {values: payload, target: hxTarget});
    });
};