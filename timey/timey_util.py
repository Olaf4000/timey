import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def aggregate_df_with_duration(df: pd.DataFrame) -> pd.DataFrame:
    required = {"description", "type", "timestamp"}
    if not required.issubset(df.columns):
        raise ValueError("Benötige Spalten: 'description', 'type', 'timestamp'")

    work = (
        df.assign(timestamp=pd.to_datetime(df["timestamp"], utc=True, errors="coerce"))
        .dropna(subset=["timestamp"])
        .copy()
    )
    work["type"] = work["type"].str.lower().str.strip()

    out_records = []

    # Pro description abarbeiten, chronologisch
    for desc, grp in work.sort_values("timestamp").groupby("description", sort=False):
        grp = grp.sort_values("timestamp", kind="stable")
        pending_starts = []
        session = 1

        for _, row in grp.iterrows():
            t = row["type"]
            ts = row["timestamp"]

            if t == "start":
                pending_starts.append(ts)

            elif t == "end":
                if pending_starts:
                    start_ts = pending_starts.pop(0)  # FIFO: ältester offener Start
                    end_ts = ts
                else:
                    # End ohne vorherigen Start
                    start_ts = pd.NaT
                    end_ts = ts

                duration = end_ts - start_ts if pd.notna(start_ts) and pd.notna(end_ts) else pd.NaT
                # Negative Dauer (sollte bei FIFO nicht vorkommen) absichern
                if pd.notna(duration) and duration < pd.Timedelta(0):
                    duration = pd.NaT

                out_records.append({
                    "description": desc,
                    "session": session,
                    "start": start_ts,
                    "end": end_ts,
                    "duration": duration,
                })
                session += 1

        # Verbleibende Starts ohne End erzeugen
        for start_ts in pending_starts:
            out_records.append({
                "description": desc,
                "session": session,
                "start": start_ts,
                "end": pd.NaT,
                "duration": pd.NaT,
            })
            session += 1

    out = pd.DataFrame(out_records, columns=["description", "session", "start", "end", "duration"])
    if not out.empty:
        out = out.sort_values(["description", "session"], kind="stable").reset_index(drop=True)
    else:
        out = pd.DataFrame(columns=["description", "session", "start", "end", "duration"])

    return out


def generate_progress_bar(bar_length, percent_completed):
    vis_percent_completed = percent_completed

    bar_length -= 9
    bar_character_1 = os.getenv("BAR_CHARACTER_1")
    bar_character_2 = os.getenv("BAR_CHARACTER_2")

    if 100 <= percent_completed < 200:
        percent_completed = percent_completed - 100
        bar_character_2 = bar_character_1
        bar_character_1 = os.getenv("BAR_CHARACTER_OVERLOAD_1")

    if 200 <= percent_completed < 300:
        percent_completed = percent_completed - 200
        bar_character_2 = bar_character_1
        bar_character_1 = os.getenv("BAR_CHARACTER_OVERLOAD_2")

    if percent_completed >= 300:
        output_string = "["
        for i in range(bar_length):
            output_string += os.getenv("BAR_CHARACTER_1")
        output_string += "] "
        output_string += f"{str(round(percent_completed))}%"
        return output_string

    completed_section = round(bar_length * (percent_completed / 100))

    output_string = "["

    for i in range(completed_section):
        output_string += bar_character_1

    for i in range(bar_length - completed_section):
        output_string += bar_character_2

    output_string += "] "

    if vis_percent_completed < 100:
        output_string += " "
        output_string += f"{str(round(vis_percent_completed))}%"

    elif vis_percent_completed < 10:
        output_string += " "
        output_string += f" {str(round(vis_percent_completed))}%"

    else:
        output_string += f"{str(round(vis_percent_completed))}%"

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


def filter_df_on_dates(df, date):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    mask = df["timestamp"].dt.date == pd.to_datetime(date).date()
    df_filtered_to_day = df.loc[mask]
    return df_filtered_to_day


def filter_df_on_description(df, description):
    return df[df["description"] == description]
