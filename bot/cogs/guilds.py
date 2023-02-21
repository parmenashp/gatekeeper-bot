from typing import TYPE_CHECKING

import discord
from core import models
from core.l10n import Localization
from discord import Embed, app_commands
from discord.ext import commands
from helpers.emojis import Emojis
from helpers.utils import get_bot_from_interaction
from loguru import logger

if TYPE_CHECKING:
    from main import GatekeeperBot

REQUIRED_PERMISSIONS = [
    "kick_members",
    "create_instant_invite",
    "manage_webhooks",
    "read_messages",
    "send_messages",
    "send_messages_in_threads",
    "use_external_emojis",
    "add_reactions",
]

VIEWS_TIMEOUT = 600


class SetupBaseView(discord.ui.View):
    """Base view for the setup process.
    Used to display the cancel button in all views.
    """

    def __init__(self, *, last_interaction: discord.Interaction | None = None):
        self.last_interaction = last_interaction
        _ = None
        if last_interaction:
            bot = get_bot_from_interaction(last_interaction)
            _ = bot.l10n.get_localization(last_interaction.locale).format

        # This is a workaround to make the cancel button always the last button.
        for index, item in enumerate(self.__view_children_items__):
            if "style" not in item.__discord_ui_model_kwargs__:
                continue
            if item.__discord_ui_model_kwargs__["style"] == discord.ButtonStyle.red:
                self.__view_children_items__.append(self.__view_children_items__.pop(index))
                break

        super().__init__(timeout=VIEWS_TIMEOUT)

        # Translate the labels of the buttons and selects
        for index, item in enumerate(self.children):
            if _ is None:
                break
            if isinstance(item, discord.ui.Button):
                item.label = _(item.label)  # type: ignore
            if isinstance(item, discord.ui.ChannelSelect):
                item.placeholder = _(item.placeholder)  # type: ignore

    def disable_timeout(self):
        """Disable the timeout of the view."""
        self.timeout = None

    async def on_timeout(self) -> None:
        """Called when the view times out."""
        # Disable all buttons
        if self.last_interaction is not None:
            for item in self.children:
                item.disabled = True  # type: ignore
            await self.last_interaction.edit_original_response(view=self)

    @discord.ui.button(label="setup_cancel_button", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = get_bot_from_interaction(interaction)
        _ = bot.l10n.get_localization(interaction.locale).format
        await interaction.response.edit_message(content=_("setup_cancel_button.pressed"), embed=None, view=None)


class SetupLogChannelView(SetupBaseView):
    def __init__(
        self,
        *,
        is_missing_permissions: bool = False,
        channel: app_commands.AppCommandChannel | app_commands.AppCommandThread | None = None,
        last_interaction: discord.Interaction | None = None,
    ):
        super().__init__(last_interaction=last_interaction)
        self.is_missing_permissions = is_missing_permissions
        self.channel = channel

        if self.is_missing_permissions:
            self.remove_item(self.log_channel_select)
        else:
            self.remove_item(self.retry_button)

    def embed(self, l10n: Localization, locale: discord.Locale):
        """Create the embed for this view."""
        _ = l10n.get_localization(locale).format
        if not self.is_missing_permissions:
            embed = discord.Embed(title="setup_log_view.title", description="setup_log_view.description")
            embed.set_footer(text="setup_log_view.footer")
        else:
            embed = discord.Embed(
                title="setup_log_view.title", description="setup_log_view.description_missing_permissions"
            )
            embed.set_footer(text="setup_log_view.footer_missing_permissions")
        return embed

    def _check_permissions(self, guild: discord.Guild, channel_id: int):
        """Check if the bot has the required permissions in the selected channel."""
        resolved_channel = guild.get_channel_or_thread(channel_id)
        if resolved_channel:
            return resolved_channel.permissions_for(guild.me).manage_webhooks
        else:
            # TODO: Send some kind of error
            return False

    def update_guild_config(self, guild_id: int, channel_id: int):
        pass

    @discord.ui.select(cls=discord.ui.ChannelSelect, placeholder="setup_log_view.placeholder")
    async def log_channel_select(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        """Called when the user selects a channel."""
        bot = get_bot_from_interaction(interaction)
        self.channel = select.values[0]

        if not self._check_permissions(interaction.guild, self.channel.id):  # type: ignore
            view = SetupLogChannelView(is_missing_permissions=True, channel=self.channel, last_interaction=interaction)
            embed = view.embed(bot.l10n, interaction.locale)

            await interaction.response.edit_message(
                embed=embed,
                view=view,
            )

        await interaction.response.edit_message(
            content=f"Canal selecionado de primeira: {self.channel.mention}",  # type: ignore
            embed=None,
            view=None,
        )

    @discord.ui.button(label="setup_retry_button", style=discord.ButtonStyle.grey)
    async def retry_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self._check_permissions(self.channel.guild, self.channel.id):  # type: ignore
            await interaction.response.edit_message(
                content=f"Canal seleccionado: {self.channel.mention}",  # type: ignore
                embed=None,
                view=None,
            )
        else:
            await interaction.response.defer()
            # TODO: Maybe alert the user that is sill missing permissions


class SetupPermissionsView(SetupBaseView):
    """View used to check if the bot has the required permissions."""

    def embed(self, l10n: Localization, locale: discord.Locale):
        _ = l10n.get_localization(locale).format
        missing_permissions = self._check_missing_permissions()
        if missing_permissions:
            self.remove_item(self.continue_button)
            return discord.Embed(
                title=_("setup_permissions_embed.title"),
                description=_(
                    "setup_permissions_embed.description_missing_permissions",
                    {"permissions": self._format_permissions(l10n, locale)},
                ),
                color=discord.Color.red(),
            ).set_footer(text=_("setup_permissions_embed.footer_missing_permissions"))
        else:
            self.remove_item(self.retry_button)
            return discord.Embed(
                title=_("setup_permissions_embed.title"),
                description=_(
                    "setup_permissions_embed.description_has_permissions",
                    {"permissions": self._format_permissions(l10n, locale)},
                ),
                color=discord.Color.green(),
            ).set_footer(text=_("setup_permissions_embed.footer_has_permissions"))

    def _format_permissions(self, localization: Localization, locale: discord.Locale):
        _ = localization.get_localization(locale).format
        missing_permissions = self._check_missing_permissions()

        list_to_join = []
        for permission in REQUIRED_PERMISSIONS:
            localizated_permission = _(f"permissions.{permission}")

            if permission in missing_permissions:
                list_to_join.append(f"{Emojis.small_x_mark()} {localizated_permission}")
            else:
                list_to_join.append(f"{Emojis.small_check_mark()} {localizated_permission}")

        return "\n".join(list_to_join)

    def _check_missing_permissions(self):
        """Check which permissions are missing and return a list of them."""
        guild_permissions = self.last_interaction.guild.me.guild_permissions  # type: ignore
        return [permission for permission in REQUIRED_PERMISSIONS if not getattr(guild_permissions, permission)]

    @discord.ui.button(label="setup_continue_button", style=discord.ButtonStyle.green)
    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = get_bot_from_interaction(interaction)
        view = SetupLogChannelView(last_interaction=interaction)
        embed = view.embed(bot.l10n, interaction.locale)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="setup_retry_button", style=discord.ButtonStyle.grey)
    async def retry_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = get_bot_from_interaction(interaction)
        view = SetupPermissionsView(last_interaction=interaction)
        embed = view.embed(bot.l10n, interaction.locale)

        self.disable_timeout()

        await interaction.response.edit_message(embed=embed, view=view)


class SetupIntroView(SetupBaseView):
    """View used to display the intro of the setup process."""

    @staticmethod
    def embed(l10n: Localization, locale: discord.Locale):
        _ = l10n.get_localization(locale).format
        return (
            discord.Embed(
                title=_("setup_intro_embed.title"),
                description=_("setup_intro_embed.description"),
                color=discord.Color.yellow(),
            )
            .add_field(
                name=_("setup_intro_embed.step_1_name"),
                value=_("setup_intro_embed.step_1_value"),
                inline=False,
            )
            .add_field(
                name=_("setup_intro_embed.step_2_name"),
                value=_("setup_intro_embed.step_2_value"),
                inline=False,
            )
            .add_field(
                name=_("setup_intro_embed.step_3_name"),
                value=_("setup_intro_embed.step_3_value"),
                inline=False,
            )
            .set_footer(text=_("setup_intro_embed.footer"))
        )

    @discord.ui.button(label="setup_continue_button", style=discord.ButtonStyle.green)
    async def continue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        bot = get_bot_from_interaction(interaction)
        view = SetupPermissionsView(last_interaction=interaction)
        embed = view.embed(bot.l10n, interaction.locale)
        # Disable the timeout because we don't want this view to expire anymore
        # We will handle the timeout only in the next view
        self.disable_timeout()

        await interaction.response.edit_message(embed=embed, view=view)


def thank_you_embed(l10n: Localization, locale: discord.Locale):
    _ = l10n.get_localization(locale).format
    return discord.Embed(
        title=_("thank_you_embed_title"),
        description=_("thank_you_embed_description"),
    )


class Guilds(commands.Cog):
    def __init__(self, bot: "GatekeeperBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        guild_config = await models.GuildConfig.get(self.bot.pool, guild.id)
        first_time = False

        if guild_config is None:
            first_time = True
            guild_config = models.GuildConfig(guild_id=guild.id)
            await guild_config.save(self.bot.pool)

        # Try to send a message to the user who invited the bot by looking at the audit logs.
        if guild.me.guild_permissions.view_audit_log:
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.bot_add, oldest_first=False):
                if entry.target.id == self.bot.user.id and entry.user is not None:  # type: ignore
                    logger.info(
                        f"Joined guild {guild.name} ({guild.id}) {'for the first time ' if first_time else ''}"
                        f"invited by {entry.user.name} ({entry.user.id})"
                    )
                    try:
                        return await entry.user.send(embed=thank_you_embed(self.bot.l10n, guild.preferred_locale))
                    except discord.Forbidden:
                        pass

        logger.info(
            f"Joined guild {guild.name} ({guild.id}) {'for the first time ' if first_time else ''}"
            "but could not find a user who invited"
        )

        # If the bot doesn't have permission to view audit logs,
        # send a message to the public updates channel, if it exists.
        if guild.public_updates_channel is not None:
            try:
                return await guild.public_updates_channel.send(
                    embed=thank_you_embed(self.bot.l10n, guild.preferred_locale)
                )
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        logger.info(f"Left guild {guild.name} ({guild.id})")

    @app_commands.command(name="setup")
    @app_commands.guilds(296214474791190529)  # For testing purposes only
    async def setup_command(self, interaction: discord.Interaction) -> None:
        view = SetupIntroView(last_interaction=interaction)
        embed = view.embed(self.bot.l10n, interaction.locale)

        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: "GatekeeperBot"):
    await bot.add_cog(Guilds(bot))
