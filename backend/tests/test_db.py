import os
import tempfile
import sqlite3
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.app.db import DatabaseManager


def test_update_process_sets_end_time_on_completed():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        db_path = tf.name
    try:
        db = DatabaseManager(db_path)
        meeting_id = "meeting1"

        async def run():
            await db.create_process(meeting_id)
            await db.update_process(meeting_id, "completed")

        import asyncio
        asyncio.run(run())

        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT end_time FROM summary_processes WHERE meeting_id = ?",
                (meeting_id,)
            )
            row = cursor.fetchone()
            assert row is not None
            assert row[0] is not None
    finally:
        os.remove(db_path)
