import typing as tp

from asyncpg.protocol.protocol import Record

from good_advice_bot.backend.entities import note_entity


class NoteSourceType(tp.Protocol):
    async def get_random_one(self) -> Record:
        pass


class Notes:
    """Provides methods to work with the Note entity."""

    def __init__(self, note_source: NoteSourceType) -> None:
        """Initializes the Notes class."""
        self.source = note_source

    async def get_random_one(self) -> Record:
        """Returns a random note."""
        return await self.source.get_random_one()


class Entities:
    """Includes all the entities the bot is working with."""

    def __init__(self) -> None:
        self.notes = Notes(note_source=note_entity)
