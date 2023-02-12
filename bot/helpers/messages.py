import discord


def guild_join_message(language: discord.Locale) -> discord.Embed:
    if language == discord.Locale.brazil_portuguese:
        title = "Obrigado por me escolher!"
        description = """
Olá, eu sou o Gatekeeper, um bot anti bot!

Para começar, você precisa configurar algumas coisas para o meu funcionamento.
Use o comando /setup e siga as instruções.
"""
    else:
        title = "Thank you for choosing me!"
        description = """
Hello, I am the Gatekeeper, an anti bot bot!

To start, you need to set up some things before I can do my job.
Use the /setup command and follow the instructions.
"""

    return discord.Embed(
        title=title,
        description=description,
    )
