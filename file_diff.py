"""
file_diff.py
============
Compares two DataFrames (old vs. new upload) and renders a highlighted diff
in Streamlit with the app's existing teal/dark aesthetic.

Usage — add to streamlit_app.py:
────────────────────────────────
    from file_diff import store_snapshot, show_file_diff

    # Before overwriting session_state with new files:
    store_snapshot("daily")
    store_snapshot("employees")

    # After loading the new DataFrames, call inside a try block:
    show_file_diff("סידור יומי",   "daily_snap",     flights_df)
    show_file_diff("עובדים",       "employees_snap",  employees_df)

Integration patch for streamlit_app.py
────────────────────────────────────────
Find the `if sidebar_confirm:` block and add TWO lines at the TOP of that block,
BEFORE the existing `if sidebar_daily:` line:

    if sidebar_confirm:
        # ── NEW: store snapshots of current data before overwriting ──
        store_snapshot("daily")
        store_snapshot("employees")
        # ... rest of existing code unchanged ...

Find the main try block that loads DataFrames and add at the END (before except):

    show_file_diff("📋 שינויים בסידור יומי",    "daily_snap",     flights_df)
    show_file_diff("👥 שינויים בקובץ עובדים",   "employees_snap",  employees_df)
"""

from __future__ import annotations

import hashlib
import io
import pickle
from typing import Optional

import pandas as pd
import streamlit as st

# ── Colours (match app theme) ────────────────────────────────────────────────
_ADDED_BG   = "rgba(0, 201, 190, 0.15)"   # teal – new row
_CHANGED_BG = "rgba(250, 174, 50, 0.18)"  # amber – changed cell
_DELETED_BG = "rgba(220, 50, 50, 0.13)"   # red   – deleted row
_ADDED_FG   = "#00c9be"
_CHANGED_FG = "#e0901a"
_DELETED_FG = "#dc2626"


# ─────────────────────────────────────────────────────────────────────────────
#  Snapshot helpers
# ─────────────────────────────────────────────────────────────────────────────

def store_snapshot(key: str) -> None:
    """
    Pickle the current DataFrame stored in session_state[f"{key}_df_snap"]
    into session_state[f"{key}_prev_snap"].  Call this BEFORE loading new data.
    """
    current_key = f"{key}_df_snap"
    prev_key    = f"{key}_prev_snap"

    current_df = st.session_state.get(current_key)
    if current_df is not None and isinstance(current_df, pd.DataFrame):
        st.session_state[prev_key] = current_df.copy()


def save_current(key: str, df: pd.DataFrame) -> None:
    """
    After loading a new DataFrame, persist it so future uploads can diff against it.
    Call once per DataFrame after it's been built:

        save_current("daily",     flights_df)
        save_current("employees", employees_df)
    """
    st.session_state[f"{key}_df_snap"] = df.copy()


# ─────────────────────────────────────────────────────────────────────────────
#  Core diff logic
# ─────────────────────────────────────────────────────────────────────────────

def _df_hash(df: pd.DataFrame) -> str:
    return hashlib.md5(
        pd.util.hash_pandas_object(df, index=True).values.tobytes()
    ).hexdigest()


def _align_columns(df_old: pd.DataFrame, df_new: pd.DataFrame):
    """Return (old, new) with a shared column set (union, preserving new order)."""
    new_cols = list(df_new.columns)
    old_cols = list(df_old.columns)
    all_cols = new_cols + [c for c in old_cols if c not in new_cols]
    return (
        df_old.reindex(columns=all_cols, fill_value=""),
        df_new.reindex(columns=all_cols, fill_value=""),
    )


def compute_diff(
    df_old: pd.DataFrame,
    df_new: pd.DataFrame,
    key_col: Optional[str] = None,
) -> dict:
    """
    Compare df_old vs df_new.

    Returns a dict with:
        result_df  – combined DataFrame (added + changed + deleted + unchanged)
        style_df   – same shape, values are CSS strings for each cell
        stats      – {"added": int, "changed": int, "deleted": int, "unchanged": int}
        changed    – bool (True if anything differs)
    """
    df_old, df_new = _align_columns(df_old.copy(), df_new.copy())
    cols = list(df_new.columns)

    # Pick a key column: first column by default, or caller's choice
    if key_col is None and cols:
        key_col = cols[0]

    old_map = {}
    new_map = {}

    if key_col and key_col in df_old.columns:
        for _, row in df_old.iterrows():
            k = str(row[key_col])
            old_map[k] = row
        for _, row in df_new.iterrows():
            k = str(row[key_col])
            new_map[k] = row
    else:
        # Fall back: compare by position
        for i, row in df_old.iterrows():
            old_map[str(i)] = row
        for i, row in df_new.iterrows():
            new_map[str(i)] = row

    result_rows   = []
    style_rows    = []
    stats = {"added": 0, "changed": 0, "deleted": 0, "unchanged": 0}

    # Added or changed
    for k, new_row in new_map.items():
        if k not in old_map:
            result_rows.append(new_row)
            style_rows.append(
                {c: f"background-color:{_ADDED_BG};color:{_ADDED_FG};font-weight:600" for c in cols}
            )
            stats["added"] += 1
        else:
            old_row = old_map[k]
            cell_changed = any(
                str(new_row.get(c, "")) != str(old_row.get(c, "")) for c in cols
            )
            result_rows.append(new_row)
            if cell_changed:
                style = {}
                for c in cols:
                    if str(new_row.get(c, "")) != str(old_row.get(c, "")):
                        style[c] = (
                            f"background-color:{_CHANGED_BG};"
                            f"color:{_CHANGED_FG};font-weight:600"
                        )
                    else:
                        style[c] = ""
                style_rows.append(style)
                stats["changed"] += 1
            else:
                style_rows.append({c: "" for c in cols})
                stats["unchanged"] += 1

    # Deleted
    for k, old_row in old_map.items():
        if k not in new_map:
            result_rows.append(old_row)
            style_rows.append(
                {c: f"background-color:{_DELETED_BG};color:{_DELETED_FG};text-decoration:line-through" for c in cols}
            )
            stats["deleted"] += 1

    result_df = pd.DataFrame(result_rows, columns=cols) if result_rows else df_new.copy()
    style_df  = pd.DataFrame(style_rows,  columns=cols) if style_rows  else pd.DataFrame(index=result_df.index, columns=cols).fillna("")

    changed = stats["added"] + stats["changed"] + stats["deleted"] > 0
    return dict(result_df=result_df, style_df=style_df, stats=stats, changed=changed)


# ─────────────────────────────────────────────────────────────────────────────
#  Streamlit renderer
# ─────────────────────────────────────────────────────────────────────────────

def show_file_diff(
    label: str,
    snapshot_key: str,
    df_new: pd.DataFrame,
    key_col: Optional[str] = None,
    max_rows: int = 500,
) -> None:
    """
    Render a diff expander.

    Parameters
    ----------
    label        : Title shown in the expander (e.g. "📋 שינויים בסידור יומי")
    snapshot_key : Key used with store_snapshot() (e.g. "daily")
    df_new       : The freshly-loaded DataFrame
    key_col      : Column to use as row identity (None = first column)
    max_rows     : Truncate displayed rows for performance
    """
    # Always persist the current version for next time
    save_current(snapshot_key, df_new)

    df_old = st.session_state.get(f"{snapshot_key}_prev_snap")
    if df_old is None or not isinstance(df_old, pd.DataFrame):
        return   # first upload – nothing to compare yet

    # Skip if identical
    if _df_hash(df_old) == _df_hash(df_new):
        return

    diff = compute_diff(df_old, df_new, key_col=key_col)
    if not diff["changed"]:
        return

    stats   = diff["stats"]
    result  = diff["result_df"].head(max_rows)
    styles  = diff["style_df"].head(max_rows)

    # ── Legend badges ────────────────────────────────────────────────────────
    badge_style = "display:inline-block;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;margin-left:6px;"
    badge_html  = ""
    if stats["added"]:
        badge_html += f'<span style="{badge_style}background:{_ADDED_BG};color:{_ADDED_FG}">+{stats["added"]} חדש</span>'
    if stats["changed"]:
        badge_html += f'<span style="{badge_style}background:{_CHANGED_BG};color:{_CHANGED_FG}">~{stats["changed"]} שונה</span>'
    if stats["deleted"]:
        badge_html += f'<span style="{badge_style}background:{_DELETED_BG};color:{_DELETED_FG}">–{stats["deleted"]} נמחק</span>'

    with st.expander(f"{label} {badge_html}", expanded=True):
        st.markdown(
            "<div dir='rtl' style='font-size:12px;color:#888;margin-bottom:8px;'>"
            "תאים מודגשים מציגים שינויים ביחס לגרסה הקודמת."
            "</div>",
            unsafe_allow_html=True,
        )

        # Apply per-cell styles
        def _styler(row):
            idx = row.name
            if idx < len(styles):
                return [styles.iloc[idx].get(c, "") for c in row.index]
            return [""] * len(row)

        styled = (
            result.style
            .apply(_styler, axis=1)
            .set_properties(**{"direction": "rtl", "text-align": "right", "font-size": "12px"})
        )
        st.dataframe(styled, use_container_width=True, hide_index=True)

        if len(diff["result_df"]) > max_rows:
            st.caption(f"מוצגות {max_rows} שורות ראשונות מתוך {len(diff['result_df'])}")
