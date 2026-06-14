import re
import pandas as pd


def _shorten(col: str) -> str:
    """Kürzt SPS-Spaltennamen: extrahiert Einheit, entfernt DB-Adresse."""
    unit = re.search(r'\[([^\]]+)\]', col)
    suffix = f' [{unit.group(1)}]' if unit else ''
    return re.sub(r'\s*\|.*$', '', col).strip() + suffix


def _dedupe(names: list[str]) -> list[str]:
    """Fügt bei doppelten Namen einen Zähler an (1), (2) ... an."""
    counts: dict[str, int] = {}
    for n in names:
        counts[n] = counts.get(n, 0) + 1
    seen: dict[str, int] = {}
    result = []
    for n in names:
        if counts[n] == 1:
            result.append(n)
        else:
            idx = seen.get(n, 1)
            result.append(f'{n} ({idx})')
            seen[n] = idx + 1
    return result


def load_data(path: str) -> pd.DataFrame:
    """Lädt SPS-Export-CSV und gibt DataFrame mit DatetimeIndex zurück."""
    df = pd.read_csv(
        path,
        sep=';',
        decimal=',',
        encoding='utf-8-sig',
        on_bad_lines='warn',
        index_col=False,  # Trailing-Semikolon in Datenzeilen verhindert Auto-Index-Shift
    )
    # Uhrzeit: "HH:MM:SS.mmm,d" → Teil vor dem Komma nehmen
    time_clean = df['Uhrzeit'].str.replace(r',\d+$', '', regex=True)
    df.index = pd.to_datetime(
        df['Datum'] + ' ' + time_clean,
        format='%d.%m.%Y %H:%M:%S.%f',
        errors='coerce',
    )
    df.index.name = 'Zeit'
    df = df.drop(columns=['Relativzeit', 'Datum', 'Uhrzeit'], errors='ignore')
    df.columns = _dedupe([_shorten(c) for c in df.columns])
    return df.sort_index()


def valve_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith('Ventil')]


def analog_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if not c.startswith('Ventil')]
