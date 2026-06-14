import io
import base64
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

from data_loader import load_data, valve_cols, analog_cols
from charts import build_figure

DEFAULT_PATH = 'assets/sps-export-demo.csv'

app = dash.Dash(__name__, title='Ventilgraph')

_S = {
    'header': {
        'display': 'flex', 'alignItems': 'center', 'gap': '16px',
        'padding': '10px 20px', 'backgroundColor': '#07070f',
        'borderBottom': '1px solid #1e2a4a', 'flexWrap': 'wrap',
    },
    'title': {'margin': 0, 'fontSize': '20px', 'color': '#c8d8ff'},
    'subtitle': {'color': '#667799', 'fontSize': '13px'},
    'btn': {
        'backgroundColor': '#1e3a6e', 'color': '#d0d0e0',
        'border': '1px solid #2a5298', 'borderRadius': '4px',
        'padding': '6px 14px', 'cursor': 'pointer', 'fontSize': '13px',
    },
    'upload': {
        'display': 'flex', 'alignItems': 'center', 'gap': '8px',
        'padding': '5px 12px', 'border': '1px dashed #2a5298',
        'borderRadius': '4px', 'cursor': 'pointer', 'color': '#8aadff',
        'fontSize': '13px', 'backgroundColor': '#0a1428',
    },
    'status': {'color': '#88aacc', 'fontSize': '12px', 'marginLeft': 'auto'},
}

def _make_graph(path_or_content, filename=None):
    if isinstance(path_or_content, bytes):
        df = load_data(io.BytesIO(path_or_content))
    else:
        df = load_data(path_or_content)
    v = valve_cols(df)
    a = analog_cols(df)
    fig = build_figure(df, v, a)
    label = filename or path_or_content
    return fig, f'{label}  ·  {len(df)} Zeilen  ·  {df.index[0]:%d.%m.%Y %H:%M} – {df.index[-1]:%H:%M}'

initial_fig, initial_status = _make_graph(DEFAULT_PATH)

app.layout = html.Div([
    html.Div([
        html.H1('Ventilgraph', style=_S['title']),
        html.Span('CIP-Prozessdaten', style=_S['subtitle']),

        dcc.Upload(
            id='upload',
            children=html.Span('📂 CSV laden'),
            style=_S['upload'],
            accept='.csv',
        ),

        html.Button('📷 Ausschnitt exportieren', id='export-btn', style=_S['btn']),
        html.Span(initial_status, id='status', style=_S['status']),
    ], style=_S['header']),

    dcc.Graph(
        id='main-graph',
        figure=initial_fig,
        style={'height': f'{initial_fig.layout.height}px'},
        config={'scrollZoom': True, 'displaylogo': False},
    ),

    dcc.Download(id='export-download'),
], style={'backgroundColor': '#0f0f1a', 'minHeight': '100vh', 'fontFamily': 'sans-serif'})


@app.callback(
    Output('main-graph', 'figure'),
    Output('main-graph', 'style'),
    Output('status', 'children'),
    Input('upload', 'contents'),
    State('upload', 'filename'),
    prevent_initial_call=True,
)
def load_csv(contents, filename):
    _, b64 = contents.split(',', 1)
    raw = base64.b64decode(b64)
    fig, status = _make_graph(raw, filename)
    return fig, {'height': f'{fig.layout.height}px'}, status


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
