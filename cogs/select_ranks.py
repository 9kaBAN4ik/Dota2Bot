import disnake
from disnake.ext import commands

EMOJI_IMMORTAL = "Emoji_for_rank"
EMOJI_DIVINE = "Emoji_for_rank"
EMOJI_ANCIENT = "Emoji_for_rank"
EMOJI_LEGEND = "Emoji_for_rank"
EMOJI_ARCHON = "Emoji_for_rank"
EMOJI_CRUSADER = "Emoji_for_rank"
EMOJI_GUARDIAN = "Emoji_for_rank"
EMOJI_HERALD = "Emoji_for_rank"

class SelectGames(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="Immortal",
                value="1078503866439581747",
                emoji=EMOJI_IMMORTAL
            ),
            disnake.SelectOption(
                label="Divine",
                value="1078503943220506634",
                emoji=EMOJI_DIVINE
            ),
            disnake.SelectOption(
                label="Ancient",
                value="1078503971074867271",
                emoji=EMOJI_ANCIENT
            ),
            disnake.SelectOption(
                label="Legend",
                value="1078503992247726232",
                emoji=EMOJI_LEGEND
            ),
            disnake.SelectOption(
                label="Archon",
                value="1079098936993779823",
                emoji=EMOJI_ARCHON
            ),
            disnake.SelectOption(
                label="Crusader",
                value="1254058951272693780",
                emoji=EMOJI_CRUSADER
            ),
            disnake.SelectOption(
                label="Guardian",
                value="1254059051550244934",
                emoji=EMOJI_GUARDIAN
            ),
            disnake.SelectOption(
                label="Herald",
                value="1254059048500989972",
                emoji=EMOJI_HERALD
            ),
        ]
        super().__init__(placeholder="Выберите ваш ранг", options=options, custom_id="games", min_values=1, max_values=1)

    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

        all_roles = {1078503866439581747, 1078503943220506634, 1078503971074867271, 1078503992247726232, 1079098936993779823, 1254058951272693780, 1254059051550244934, 1254059048500989972}

        to_remove = []
        to_add = []

        if not interaction.values:
            for role_id in all_roles:
                role = interaction.guild.get_role(role_id)
                to_remove.append(role)

            await interaction.author.remove_roles(*to_remove, reason="Удаление ролей")

        else:
            chosen_roles = {int(value) for value in interaction.values}

            ids_to_remove = all_roles - chosen_roles

            for role_id in ids_to_remove:
                role = interaction.guild.get_role(role_id)
                to_remove.append(role)

            for role_id in chosen_roles:
                role = interaction.guild.get_role(role_id)
                to_add.append(role)

            await interaction.author.remove_roles(*to_remove, reason="Удаление ролей")
            await interaction.author.add_roles(*to_add, reason="Добавление ролей")


class SelectRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False

    @commands.command()
    async def games(self, ctx):
        view = disnake.ui.View(timeout=None)
        view.add_item(SelectGames())
        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name="Игровые ранги:")
        embed.description = (
            "В этом посте Вы можете выбрать свой ранг, нажав на кнопку "
            "соответствующего ранга в меню выбора.\n\n"
            f"{EMOJI_IMMORTAL} - Immortal\n"
            f"{EMOJI_DIVINE} - Divine\n"
            f"{EMOJI_ANCIENT} - Ancient\n"
            f"{EMOJI_LEGEND} - Legend\n"
            f"{EMOJI_ARCHON} - Archon\n"
            f"{EMOJI_CRUSADER} - Crusader\n"
            f"{EMOJI_GUARDIAN} - Guardian\n"
            f"{EMOJI_HERALD} - Herald"
        )
        embed.set_image(url="https://i.imgur.com/QzB7q9J.png")
        await ctx.send(embed=embed, view=view)

@disnake.ext.commands.Cog.listener()
async def on_ready(self):
    if self.persistent_views_added:
        return

    channel = self.bot.get_channel(1254051951193231371)
    view = disnake.ui.View(timeout=None)
    view.add_item(SelectGames())
    await channel.send("Выберите ваш ранг", view=view)
    self.persistent_views_added = True

    view = disnake.ui.View(timeout=None)
    view.add_item(SelectGames())
    self.bot.add_view(view, message_id=1254109356538986547)

def setup(bot):
    bot.add_cog(SelectRoles(bot))
