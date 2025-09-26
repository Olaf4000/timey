import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def aggregate_df_with_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Erwartet ein DataFrame mit Spalten:
      - 'description' : Kennung der Session/Aktion
      - 'type'        : 'start' oder 'end'
      - 'timestamp'   : Zeitstempel (str, datetime oder numpy datetime64)

    Ergebnis:
      pro 'description' je ein 'start', 'end' und 'duration' (end - start).
      Bei mehreren Starts/Ends wird standardmäßig der früheste Start und der
      späteste Endzeitpunkt verwendet.
    """
    if not {"description", "type", "timestamp"} <= set(df.columns):
        raise ValueError("Benötige Spalten: 'description', 'type', 'timestamp'")

    # Timestamps sicher nach datetime konvertieren (UTC-tolerant, NaT für unlesbare Werte)
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    work = df.assign(timestamp=ts).dropna(subset=["timestamp"])

    # Frühester Start pro description
    starts = (
        work[work["type"].eq("start")]
        .groupby("description", as_index=False)["timestamp"].min()
        .rename(columns={"timestamp": "start"})
    )

    # Spätester Endzeitpunkt pro description
    ends = (
        work[work["type"].eq("end")]
        .groupby("description", as_index=False)["timestamp"].max()
        .rename(columns={"timestamp": "end"})
    )

    # Outer-Join, damit auch unvollständige Paare sichtbar bleiben
    out = starts.merge(ends, on="description", how="outer")

    # Dauer berechnen (bleibt NaT, wenn start oder end fehlt)
    out["duration"] = out["end"] - out["start"]

    # Optional: negative Dauern (falls Daten verdreht) auf NaT setzen
    mask_bad = out["duration"].notna() & (out["duration"] < pd.Timedelta(0))
    if mask_bad.any():
        out.loc[mask_bad, "duration"] = pd.NaT

    # Aufräumen & sortieren
    return out.sort_values("description", kind="stable").reset_index(drop=True)


def generate_progress_bar(bar_length, percent_completed):
    bar_length -= 9

    if percent_completed >= 100:
        output_string = "["
        for i in range(bar_length):
            output_string += os.getenv("BAR_CHARACTER_1")
        output_string += "] "
        output_string += f"{str(round(percent_completed))}%"
        return output_string

    completed_section = round(bar_length * (percent_completed / 100))

    output_string = "["

    for i in range(completed_section):
        output_string += os.getenv("BAR_CHARACTER_1")

    for i in range(bar_length - completed_section):
        output_string += os.getenv("BAR_CHARACTER_2")

    output_string += "] "
    if percent_completed < 100:
        output_string += " "
        output_string += f"{str(round(percent_completed))}%"
    elif percent_completed < 10:
        output_string += " "
        output_string += f"{str(round(percent_completed))}%"
    else:
        output_string += f"{str(round(percent_completed))}%"

    return output_string


def pair_start_end(df: pd.DataFrame) -> pd.DataFrame:
    """
    Erwartet ein DataFrame mit Spalten ['timestamp', 'type', 'description'].
    Kombiniert jeweils aufeinanderfolgende 'start' und 'end'-Einträge in ein neues DataFrame
    mit Spalten ['start', 'end'].
    Rundet die Zeitstempel auf volle Sekunden.
    """
    # sicherstellen, dass nach Zeit sortiert
    df = df.sort_values("timestamp").reset_index(drop=True)

    # auf volle Sekunden runden
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.round("S")

    # nur start- und end-Zeilen paaren
    starts = df[df["type"] == "start"].reset_index(drop=True)
    ends = df[df["type"] == "end"].reset_index(drop=True)

    # beide DataFrames zusammenführen
    result = pd.DataFrame({
        "start": starts["timestamp"],
        "end": ends["timestamp"]
    })

    return result


def pair_df_to_list(df: pd.DataFrame) -> list[str]:
    """
    Erwartet ein DataFrame mit Spalten ['start', 'end'].
    Gibt eine Liste von Strings zurück der Form:
    '> datum und daran X Stunden Y Minuten gearbeitet'
    """
    result = []
    for _, row in df.iterrows():
        datum = row["start"].date()
        diff = row["end"] - row["start"]
        minuten_total = int(diff.total_seconds() // 60)
        stunden, minuten = divmod(minuten_total, 60)
        result.append(f"> {datum}: {stunden}h {minuten}min")
    return result
