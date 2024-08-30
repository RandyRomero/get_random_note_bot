from good_advice_bot.bot.repository import Entities


async def get_a_random_note(entities: Entities) -> str:
    """Get a formatted string with a random note."""
    random_line = await entities.notes.get_random_one()
    note = random_line["note"]
    topic = random_line["topic"]
    author = random_line["author"]
    info = random_line["info"]
    reply = f"Note: {note}\nTopic: {topic}\nAuthor: {author}"
    if info:
        reply = f"{reply}\nAdditional info: {info}"
    return reply
