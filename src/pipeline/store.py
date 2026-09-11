"""Tiny SQLite persistence — three tables.

Schema:
  runs       — one row per pipeline execution (mirrors RunSummary fields)
  answers    — one row per LLM call, FK-linked to runs.id
  eval_runs  — one row per evaluation run/result
"""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Iterable


from .pipeline import Answer
from .settings import RunSummary


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at       REAL    NOT NULL,
    elapsed_seconds  REAL    NOT NULL,
    n_questions      INTEGER NOT NULL,
    n_succeeded      INTEGER NOT NULL,
    n_retries_total  INTEGER NOT NULL,
    total_cost_usd   REAL    NOT NULL,
    fail_rate        REAL    NOT NULL,
    use_fake         INTEGER NOT NULL                       -- 0 / 1 (SQLite has no native bool)
);

CREATE TABLE IF NOT EXISTS answers (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id    INTEGER NOT NULL,                             -- ties an answer to its run
    question  TEXT    NOT NULL,
    answer    TEXT    NOT NULL,
    cost_usd  REAL    NOT NULL,
    retries   INTEGER NOT NULL DEFAULT 0,
    ts        REAL    NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE TABLE IF NOT EXISTS eval_runs (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    golden_id         TEXT NOT NULL,
    question          TEXT NOT NULL,
    candidate_answer  TEXT NOT NULL,
    ideal_answer      TEXT NOT NULL,
    candidate_model   TEXT NOT NULL,
    judge_model       TEXT NOT NULL,
    accuracy          INTEGER NOT NULL,
    groundedness      INTEGER NOT NULL,
    format            INTEGER NOT NULL,
    reasoning         TEXT NOT NULL,
    eval_run_label    TEXT DEFAULT 'eval-run-001',
    created_at        TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(path: str | Path = "results.db") -> sqlite3.Connection:
    """Open (or create) the database, ensure all tables exist, return the connection."""
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.commit()
    return con


def write_run(con: sqlite3.Connection, summary: RunSummary) -> int:
    """Insert one row into `runs`. Returns the new row id (use for write_answers)."""
    cur = con.execute(
        "INSERT INTO runs (started_at, elapsed_seconds, n_questions, n_succeeded, "
        "                  n_retries_total, total_cost_usd, fail_rate, use_fake) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            summary.started_at,
            summary.elapsed_seconds,
            summary.n_questions,
            summary.n_succeeded,
            summary.n_retries_total,
            summary.total_cost_usd,
            summary.fail_rate,
            1 if summary.use_fake else 0,
        ),
    )
    con.commit()
    return cur.lastrowid


def write_answers(
    con: sqlite3.Connection,
    run_id: int,
    answers: Iterable[Answer],
) -> int:
    """Bulk-insert all answers for a given run. Returns the number of rows inserted."""
    ts = time.time()
    rows = [
        (run_id, a.question, a.text, a.cost_usd, a.retries, ts)
        for a in answers
    ]

    con.executemany(
        "INSERT INTO answers (run_id, question, answer, cost_usd, retries, ts) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    con.commit()
    return len(rows)


def write_eval_run(
    con: sqlite3.Connection,
    golden_id: str,
    question: str,
    candidate_answer: str,
    ideal_answer: str,
    candidate_model: str,
    judge_model: str,
    accuracy: int,
    groundedness: int,
    format: int,
    reasoning: str,
    eval_run_label: str = "eval-run-001",
) -> int:
    """Insert one row into `eval_runs`. Returns the new row id."""

    cur = con.execute(
        """
        INSERT INTO eval_runs (
            golden_id,
            question,
            candidate_answer,
            ideal_answer,
            candidate_model,
            judge_model,
            accuracy,
            groundedness,
            format,
            reasoning,
            eval_run_label
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            golden_id,
            question,
            candidate_answer,
            ideal_answer,
            candidate_model,
            judge_model,
            accuracy,
            groundedness,
            format,
            reasoning,
            eval_run_label,
        ),
    )

    con.commit()
    return cur.lastrowid


def read_eval_runs(
    con: sqlite3.Connection,
    eval_run_label: str | None = None,
) -> list[sqlite3.Row]:
    """Read evaluation results, optionally filtered by eval_run_label."""

    con.row_factory = sqlite3.Row

    if eval_run_label is None:
        cur = con.execute(
            """
            SELECT
                id,
                golden_id,
                question,
                candidate_answer,
                ideal_answer,
                candidate_model,
                judge_model,
                accuracy,
                groundedness,
                format,
                reasoning,
                eval_run_label,
                created_at
            FROM eval_runs
            ORDER BY id
            """
        )
    else:
        cur = con.execute(
            """
            SELECT
                id,
                golden_id,
                question,
                candidate_answer,
                ideal_answer,
                candidate_model,
                judge_model,
                accuracy,
                groundedness,
                format,
                reasoning,
                eval_run_label,
                created_at
            FROM eval_runs
            WHERE eval_run_label = ?
            ORDER BY id
            """,
            (eval_run_label,),
        )

    return cur.fetchall()