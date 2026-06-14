import io
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

from data_loader import load_data, valve_cols, analog_cols
from charts import build_figure

DATA_PATH = 'assets/sps-export-demo.csv'

df = load_data(DATA_PATH)
valves = valve_cols(df)
analogs = analog_cols(df)
fig = build_figure(df, valves, analogs)

app = dash.Dash(__name__, title='Ventilgraph')

_header_style = {
    'display': 'flex',
    'alignItems': 'center',
    'gap': '16px',
    'padding': '10px 20px',
    'backgroundColor': '#07070f',
    'borderBottom': '1px solid #1e2a4a',
}
_btn_style = {
    'backgroundColor': '#1e3a6e',
    'color': '#d0d0e0',
    'border': '1px solid #2a5298',
    'borderRadius': '4px',
    'padding': '6px 14px',
    'cursor': 'pointer',
    'fontSize': '13px',
}

app.layout = html.Div([
    html.Div([
        html.H1('Ventilgraph', style={'margin': 0, 'fontSize': '20px', 'color': '#c8d8ff'}),
        html.Span('CIP-Prozessdaten', style={'color': '#667799', 'fontSize': '13px'}),
        html.Button('📷 Ausschnitt exportieren', id='export-btn', style=_btn_style),
    ], style=_header_style),

    dcc.Graph(
        id='main-graph',
        figure=fig,
        style={'height': f'{fig.layout.height}px'},
        config={'scrollZoom': True, 'displaylogo': False},
    ),

    dcc.Download(id='export-download'),
], style={'backgroundColor': '#0f0f1a', 'minHeight': '100vh', 'fontFamily': 'sans-serif'})


@app.callback(
    Output('export-download', 'data'),
    Input('export-btn', 'n_clicks'),
    State('main-graph', 'relayoutData'),
    State('main-graph', 'figure'),
    prevent_initial_call=True,
)
def export_png(n_clicks, relayout, fig_dict):
    out = go.Figure(fig_dict)
    if relayout:
        x0 = relayout.get('xaxis.range[0]') or relayout.get('xaxis2.range[0]')
        x1 = relayout.get('xaxis.range[1]') or relayout.get('xaxis2.range[1]')
        if x0 and x1:
            out.update_xaxes(range=[x0, x1])
    buf = io.BytesIO()
    out.write_image(buf, format='png', width=1600, height=out.layout.height or 800)
    buf.seek(0)
    return dcc.send_bytes(buf.read(), 'ventilgraph_export.png')


if __name__ == '__main__':
    app.run(debug=True)
