from asyncpg.protocol.protocol import Record

from good_advice_bot.backend.db import db, DB


class NoteEntity:
    """Provides methods to work with notes table."""

    def __init__(self, database: DB) -> None:
        """Initializes the class."""
        self.database = database

    async def get_random_one(self) -> Record:
        """Get a random row from the notes table."""
        async with self.database.get_connection() as conn:
            result = await conn.fetchrow(
                """
            SELECT
                notes.id,
                notes.text AS note,
                notes.additional_info AS info,
                topics.text AS topic,
                authors.name AS author
            FROM notes
            LEFT JOIN authors ON authors.id = notes.author_id
            JOIN notes_topics ON notes.id = public.notes_topics.note_id
            JOIN topics ON notes_topics.topic_id = topics.id
            ORDER BY random() limit 1;
            """,
            )
        return result


note_entity = NoteEntity(db)
