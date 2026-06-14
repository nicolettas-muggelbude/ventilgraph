import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

_VALVE_COLORS = [
    'rgba(33,150,243,0.85)',   # blau
    'rgba(76,175,80,0.85)',    # grün
    'rgba(255,152,0,0.85)',    # orange
    'rgba(156,39,176,0.85)',   # lila
    'rgba(244,67,54,0.85)',    # rot
    'rgba(0,188,212,0.85)',    # cyan
    'rgba(139,195,74,0.85)',   # hellgrün
    'rgba(255,87,34,0.85)',    # tiefrot
    'rgba(63,81,181,0.85)',    # indigo
    'rgba(0,150,136,0.85)',    # teal
    'rgba(255,193,7,0.85)',    # gelb
    'rgba(233,30,99,0.85)',    # pink
]
_ANALOG_COLORS = [
    '#E53935', '#1E88E5', '#43A047', '#FB8C00',
    '#8E24AA', '#00ACC1', '#6D4C41', '#546E7A',
]

_BAR = 0.82   # Füllhöhe pro Ventilzeile (0.0 = AUS, _BAR = EIN)
_BG = '#16213e'
_GRID = '#2a3a5c'


def build_figure(df: pd.DataFrame, valves: list[str], analogs: list[str]) -> go.Figure:
    n = len(valves)
    total_height = max(600, n * 32 + 380)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[n * 32, 340],
        vertical_spacing=0.04,
        subplot_titles=['Ventile', 'Analogwerte'],
    )

    # --- Ventile: Gantt-Balken via tonexty ---
    for i, col in enumerate(valves):
        color = _VALVE_COLORS[i % len(_VALVE_COLORS)]
        x = df.index
        baseline = [i] * len(df)
        signal = (df[col].fillna(0) * _BAR + i).tolist()
        state = df[col].fillna(0).astype(int).map({0: 'AUS', 1: 'EIN'})

        # Unsichtbare Basislinie als tonexty-Referenz
        fig.add_trace(go.Scatter(
            x=x, y=baseline, mode='lines',
            line=dict(width=0), showlegend=False, hoverinfo='skip',
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=x, y=signal, mode='lines',
            line=dict(shape='hv', width=0.5, color=color),
            fill='tonexty', fillcolor=color,
            name=col,
            customdata=state,
            hovertemplate='%{customdata}<extra>' + col + '</extra>',
        ), row=1, col=1)

    # --- Analogwerte: Linien ---
    for i, col in enumerate(analogs):
        color = _ANALOG_COLORS[i % len(_ANALOG_COLORS)]
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col],
            mode='lines', line=dict(width=1.5, color=color),
            name=col,
            hovertemplate='%{y:.2f}<extra>' + col + '</extra>',
        ), row=2, col=1)

    fig.update_layout(
        height=total_height,
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode='x unified',
        legend=dict(orientation='v', x=1.01, xanchor='left', y=1),
        paper_bgcolor='#0f0f1a',
        plot_bgcolor=_BG,
        font=dict(color='#d0d0e0', size=11),
    )

    fig.update_yaxes(
        tickvals=[i + _BAR / 2 for i in range(n)],
        ticktext=valves,
        range=[-0.15, n + 0.15],
        showgrid=False, zeroline=False,
        row=1, col=1,
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=_GRID, zeroline=False,
        row=2, col=1,
    )
    fig.update_xaxes(showgrid=True, gridcolor=_GRID, tickformat='%H:%M:%S')

    return fig
