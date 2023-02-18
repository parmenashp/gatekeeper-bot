import discord
from pathlib import Path
from fluent.runtime import FluentLocalization as FluentLocalizationBase
from fluent.runtime import FluentResourceLoader


class FluentLocalization(FluentLocalizationBase):
    def format(self, message_id: str, args: dict = {}) -> str:
        """Get a message from the localization and format it.
        It will try to find the message in the first locale, then the second, etc.

        Notes:
            Has a fallback to the message ID if the message is not found.
            Attributes can be accessed by appending a dot and the attribute name to the message ID.

        Args:
            message_id (str): The ID of the message to format.
            args (dict, optional): The arguments to format the message with.

        Returns:
            str: The formatted message.
        """
        message_id, _, attribute_id = message_id.partition(".")

        for bundle in self._bundles():
            if not bundle.has_message(message_id):
                continue

            message = bundle.get_message(message_id)
            if not message.value and not attribute_id:
                continue

            if attribute_id:
                if attribute_id not in message.attributes:
                    continue

                pattern = message.attributes[attribute_id]

            else:
                if not message.value:
                    continue

                pattern = message.value

            value, errors = bundle.format_pattern(pattern, args)
            return value

        if attribute_id:
            return f"{message_id}.{attribute_id}"
        return message_id


class Localization:
    def __init__(self) -> None:
        """A class to manage localizations for the bot."""

        l10n_root_path = str(Path(__file__).parent.parent / "l10n" / "{locale}")
        self._loader = FluentResourceLoader(l10n_root_path)
        self._file_names: list = ["main.ftl"]
        self._localizations: dict[str, FluentLocalization] = {}
        self._default_locale: str = "en-US"

    def load_localization(self, locales: list) -> None:
        """Load a localization for a list of locales.
        The first locale in the list is the default locale.

        Args:
            locales (list): A list of locales to load.
                The first being the desired locale, with fallbacks after that, if any.
        """
        self._localizations[locales[0]] = FluentLocalization(locales, self._file_names, self._loader)

    def get_localization(self, locale: str | discord.Locale) -> FluentLocalization:
        """Get a localization for a locale.

        Args:
            locale (str | discord.Locale): The locale to get the localization for.

        Returns:
            FluentLocalization: The localization for the locale.
        """
        if isinstance(locale, discord.Locale):
            locale = str(locale)
        if locale in self._localizations:
            return self._localizations[locale]
        return self._localizations[self._default_locale]

    def set_default_locale(self, locale: str) -> None:
        """Set the default locale for the bot.

        Args:
            locale (str): The locale to set as the default.
        """
        self._default_locale = locale
