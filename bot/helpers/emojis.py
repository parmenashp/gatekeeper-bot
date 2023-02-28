import discord
from dataclasses import dataclass


class ConcatenatablePartialEmoji(discord.PartialEmoji):
    """A partial emoji that can be concatenated with strings."""

    def __add__(self, other):
        return str(self) + str(other)


@dataclass(frozen=True, init=False)
class Emojis:
    small_x_mark = ConcatenatablePartialEmoji(name="small_x_mark", id=1039023797396848730)
    small_check_mark = ConcatenatablePartialEmoji(name="small_check_mark", id=1039025339436908544)
