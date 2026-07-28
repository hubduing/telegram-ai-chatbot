import aiosqlite

DB_PATH = "chat_history.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS history (
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_history_user_id
            ON history (user_id)
        """)
        await db.commit()


async def add_message(user_id: int, role: str, content: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content),
        )
        await db.commit()


async def get_history(user_id: int, limit: int = 15) -> list[dict[str, str]]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT role, content FROM history
            WHERE user_id = ?
            ORDER BY timestamp ASC
            """,
            (user_id,),
        )
        rows = await cursor.fetchall()

    rows = rows[-limit:]

    return [{"role": role, "content": content} for role, content in rows]


async def clear_history(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM history WHERE user_id = ?",
            (user_id,),
        )
        await db.commit()


async def trim_history(user_id: int, max_messages: int = 15) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM history WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        count = row[0] if row else 0

        if count > max_messages:
            to_delete = count - max_messages
            await db.execute(
                """
                DELETE FROM history
                WHERE user_id = ? AND timestamp IN (
                    SELECT timestamp FROM history
                    WHERE user_id = ?
                    ORDER BY timestamp ASC
                    LIMIT ?
                )
                """,
                (user_id, user_id, to_delete),
            )
            await db.commit()