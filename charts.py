import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

_VALVE_COLORS = [
    '#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336',
    '#00BCD4', '#8BC34A', '#FF5722', '#3F51B5', '#009688',
    '#FFC107', '#E91E63',
]
_ANALOG_COLORS = [
    '#E53935', '#1E88E5', '#43A047', '#FB8C00',
    '#8E24AA', '#00ACC1', '#6D4C41', '#546E7A',
]

_BG   = '#16213e'
_GRID = '#2a3a5c'
_ROW_H = 0.80   # Balkenhöhe innerhalb einer Ventilzeile (0..1)
_PAD   = 0.10   # Abstand oben und unten


def _on_periods(series: pd.Series) -> list[tuple]:
    """Gibt (start, end) für alle EIN-Perioden zurück."""
    vals = series.ffill().fillna(0).astype(int)
    periods, start = [], None
    for t, v in zip(series.index, vals):
        if v == 1 and start is None:
            start = t
        elif v == 0 and start is not None:
            periods.append((start, t))
            start = None
    if start is not None:
        periods.append((start, series.index[-1]))
    return periods


def _rect_trace(periods, row_i, color, name) -> go.Scatter:
    """Einzelner Scatter-Trace mit allen EIN-Rechtecken (None-Trenner)."""
    x, y = [], []
    y0, y1 = row_i + _PAD, row_i + _PAD + _ROW_H
    for t0, t1 in periods:
        x += [t0, t0, t1, t1, t0, None]
        y += [y0, y1, y1, y0, y0, None]
    return go.Scatter(
        x=x, y=y,
        mode='lines', fill='toself',
        fillcolor=color, line=dict(width=0, color=color),
        name=name, showlegend=True, hoverinfo='skip',
    )


def _hover_trace(df_col: pd.Series, row_i: int, name: str, show_legend: bool) -> go.Scatter:
    """Unsichtbare Linie in Zeilenmitte – liefert Hover-Text."""
    state = df_col.fillna(0).astype(int).map({0: 'AUS', 1: 'EIN'})
    return go.Scatter(
        x=df_col.index,
        y=[row_i + _PAD + _ROW_H / 2] * len(df_col),
        mode='lines', line=dict(width=0),
        customdata=state,
        hovertemplate='%{customdata}<extra>' + name + '</extra>',
        name=name, showlegend=show_legend,
    )


def build_figure(df: pd.DataFrame, valves: list[str], analogs: list[str]) -> go.Figure:
    n = len(valves)
    total_height = max(600, n * 36 + 380)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[n * 36, 340],
        vertical_spacing=0.04,
        subplot_titles=['Ventile', 'Analogwerte'],
    )

    # --- Ventile: Rechteck-Balken ---
    for i, col in enumerate(valves):
        color = _VALVE_COLORS[i % len(_VALVE_COLORS)]
        periods = _on_periods(df[col])

        if periods:
            fig.add_trace(_rect_trace(periods, i, color, col), row=1, col=1)
            fig.add_trace(_hover_trace(df[col], i, col, show_legend=False), row=1, col=1)
        else:
            fig.add_trace(_hover_trace(df[col], i, col, show_legend=True), row=1, col=1)

    # --- Analogwerte: ein gemeinsamer Graph ---
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
        tickvals=[i + _PAD + _ROW_H / 2 for i in range(n)],
        ticktext=valves,
        range=[-0.1, n + 0.1],
        showgrid=False, zeroline=False,
        row=1, col=1,
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=_GRID, zeroline=False,
        row=2, col=1,
    )
    fig.update_xaxes(showgrid=True, gridcolor=_GRID, tickformat='%H:%M:%S')

    return fig
