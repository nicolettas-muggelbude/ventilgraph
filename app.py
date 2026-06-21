import io
import base64
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd

from data_loader import load_data, valve_cols, analog_cols
from charts import build_figure

DEFAULT_PATH = 'assets/sps-export-demo.csv'

app = dash.Dash(__name__, title='Ventilgraph')

# Initiale Daten
_df0 = load_data(DEFAULT_PATH)
_v0  = valve_cols(_df0)
_a0  = analog_cols(_df0)
_fig0 = build_figure(_df0, _v0, _a0)
_status0 = f'{DEFAULT_PATH}  ·  {len(_df0)} Zeilen  ·  {_df0.index[0]:%d.%m.%Y %H:%M} – {_df0.index[-1]:%H:%M}'
_df0_json = _df0.to_json(orient='split', date_format='iso')


def _opts(cols):
    return [{'label': c, 'value': c} for c in cols]


_S = {
    'header': {
        'display': 'flex', 'alignItems': 'center', 'gap': '16px',
        'padding': '10px 20px', 'backgroundColor': '#07070f',
        'borderBottom': '1px solid #1e2a4a', 'flexWrap': 'wrap',
    },
    'filter_bar': {
        'display': 'flex', 'gap': '16px', 'padding': '8px 20px',
        'backgroundColor': '#09091a', 'borderBottom': '1px solid #1e2a4a',
        'flexWrap': 'wrap', 'alignItems': 'flex-end',
    },
    'title':    {'margin': 0, 'fontSize': '20px', 'color': '#c8d8ff'},
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
    'status':    {'color': '#88aacc', 'fontSize': '12px', 'marginLeft': 'auto'},
    'label':     {'color': '#8aadff', 'fontSize': '11px', 'marginBottom': '2px'},
    'filter_col': {'flex': '1', 'minWidth': '280px'},
}

app.layout = html.Div([
    # Header
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
        html.Span(_status0, id='status', style=_S['status']),
    ], style=_S['header']),

    # Filterleiste
    html.Div([
        html.Div([
            html.Div('Ventile', style=_S['label']),
            dcc.Dropdown(
                id='valve-filter', options=_opts(_v0), value=_v0,
                multi=True, clearable=False, placeholder='Alle Ventile',
                style={'fontSize': '12px'},
            ),
        ], style=_S['filter_col']),
        html.Div([
            html.Div('Analogwerte', style=_S['label']),
            dcc.Dropdown(
                id='analog-filter', options=_opts(_a0), value=_a0,
                multi=True, clearable=False, placeholder='Alle Analogwerte',
                style={'fontSize': '12px'},
            ),
        ], style=_S['filter_col']),
    ], style=_S['filter_bar']),

    # Graph
    dcc.Graph(
        id='main-graph',
        figure=_fig0,
        style={'height': f'{_fig0.layout.height}px'},
        config={'scrollZoom': True, 'displaylogo': False},
    ),

    dcc.Download(id='export-download'),
    dcc.Store(id='df-store', data=_df0_json),
], style={'backgroundColor': '#0f0f1a', 'minHeight': '100vh', 'fontFamily': 'sans-serif'})


@app.callback(
    Output('df-store', 'data'),
    Output('valve-filter', 'options'),
    Output('valve-filter', 'value'),
    Output('analog-filter', 'options'),
    Output('analog-filter', 'value'),
    Output('status', 'children'),
    Input('upload', 'contents'),
    State('upload', 'filename'),
    prevent_initial_call=True,
)
def load_csv(contents, filename):
    _, b64 = contents.split(',', 1)
    raw = base64.b64decode(b64)
    df = load_data(io.BytesIO(raw))
    v = valve_cols(df)
    a = analog_cols(df)
    status = f'{filename}  ·  {len(df)} Zeilen  ·  {df.index[0]:%d.%m.%Y %H:%M} – {df.index[-1]:%H:%M}'
    return df.to_json(orient='split', date_format='iso'), _opts(v), v, _opts(a), a, status


@app.callback(
    Output('main-graph', 'figure'),
    Output('main-graph', 'style'),
    Input('valve-filter', 'value'),
    Input('analog-filter', 'value'),
    State('df-store', 'data'),
)
def update_figure(selected_valves, selected_analogs, df_json):
    df = pd.read_json(io.StringIO(df_json), orient='split')
    df.index = pd.to_datetime(df.index)
    fig = build_figure(df, selected_valves or [], selected_analogs or [])
    return fig, {'height': f'{fig.layout.height}px'}


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
