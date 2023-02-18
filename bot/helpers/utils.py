from asyncio.log import logger
import discord
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GatekeeperBot


class ProgressBar:
    """A simple progress bar class that can be used to generate a progress bar string"""

    def __init__(self, total, bar_length, full_char="▰", empty_char="▱", start_char="[", end_char="]"):
        """Initializes the progress bar

        Args:
            total (int): The total value of the progress bar
            bar_length (int): The length of the progress bar
            full_char (str, optional): The character to use for the filled part of the progress bar.
                Defaults to "▰".
            empty_char (str, optional): The character to use for the empty part of the progress bar.
                Defaults to "▱".
            start_char (str, optional): The character to use for the start of the progress bar.
                Defaults to "[".
            end_char (str, optional): The character to use for the end of the progress bar.
                Defaults to "]".

        Examples:
            >>> bar = ProgressBar(100, 10)
            >>> bar.bar
            "[▱▱▱▱▱▱▱▱▱]"
            >>> bar.next(40)
            >>> bar.bar
            "[▰▰▰▰▱▱▱▱▱]"
            >>> bar.percentage
            40.0
        """
        self.total = total
        self.bar_length = bar_length
        self.current_value = 0
        self.full_char = "▰"
        self.empty_char = "▱"
        self.start_char = "["
        self.end_char = "]"

    @property
    def bar(self):
        """Returns the current progress bar string"""
        filled_length = int(self.percentage / (100.0 / self.bar_length))
        bar = self.full_char * filled_length + self.empty_char * (self.bar_length - filled_length)
        return self.start_char + bar + self.end_char

    @property
    def percentage(self):
        """Returns the current progress as a percentage value"""
        return 100.0 * self.current_value / self.total

    def next(self, value: int = 1):
        """Advances the progress bar by a given value

        Args:
            value (int, optional): The value to advance the progress bar by. Defaults to 1.
        """
        self.current_value += value


async def is_dm_open(user: discord.User | discord.Member) -> bool:
    """Checks if a user has DMs open

    Args:
        user (discord.User | discord.Member): The user to check

    Returns:
        bool: True if DMs are open, False otherwise

    Raises:
        discord.HTTPException: If one unexpected error occurs
    """

    try:
        await user.send()
        return True  # Just because the type checker doesn't know that the above line will raise an exception
    except discord.HTTPException as e:
        if e.code == 50006:  # cannot send an empty message
            return True
        elif e.code == 50007:  # cannot send messages to this user
            return False
        else:
            raise


async def guess_if_user_is_nitro(
    bot: GatekeeperBot,
    user: discord.User | discord.Member,
    fetch: bool = True,
) -> bool:
    """Guesses if an user or member has Discord Nitro by
    checking if user has any of the following:
    - Animated avatar
    - Nitro boost
    - Guild avatar
    - Banner*

    *The user has to be fetched to check the banner

    Args:
        bot (GatekeeperBot): The bot instance
        user (discord.User | discord.Member): The user or member to check
        fetch (bool, optional): If the user should be fetched for checking the banner.
        Defaults to True.

    Returns:
        bool: True if user has any of the above, False otherwise
    """

    if user.display_avatar.is_animated():
        return True

    if isinstance(user, discord.Member):
        for activity in user.activities:
            if isinstance(activity, discord.CustomActivity) and activity.emoji is not None:
                if activity.emoji.is_custom_emoji():
                    return True
        if any([user.display_avatar.is_animated(), user.premium_since, user.guild_avatar]):
            return True

    if fetch:
        try:
            if (await bot.fetch_user(user.id)).banner:
                return True
        except discord.HTTPException:
            logger.exception("Failed to fetch user for nitro check")
            pass

    return False


def get_bot_from_interaction(interaction: discord.Interaction) -> "GatekeeperBot":
    """Get the bot (GatekeeperBot) from an interaction.
    This is a workaround for the fact that interaction.client is typed as Client.

    Args:
        interaction (discord.Interaction): The interaction to get the bot from.

    Returns:
        GatekeeperBot: The bot.
    """

    return interaction.client  # type: ignore
