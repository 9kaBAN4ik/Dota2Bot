import disnake
from disnake.ext import commands

event_participants = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "all": []
}

user_roles = {}

class SelectGames(disnake.ui.View):
    def __init__(self, event_cog):
        super().__init__()
        self.event_cog = event_cog

    @disnake.ui.button(label="Carry", style=disnake.ButtonStyle.secondary, emoji="Your_EMOJI_ID_FOR_POS1")
    async def carry_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.event_cog.select_callback(interaction, "1")

    @disnake.ui.button(label="Midlaner", style=disnake.ButtonStyle.secondary, emoji="Your_EMOJI_ID_FOR_POS2")
    async def midlaner_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.event_cog.select_callback(interaction, "2")

    @disnake.ui.button(label="Hard Laner", style=disnake.ButtonStyle.secondary, emoji="Your_EMOJI_ID_FOR_POS3")
    async def hard_laner_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.event_cog.select_callback(interaction, "3")

    @disnake.ui.button(label="Soft Support", style=disnake.ButtonStyle.secondary, emoji="Your_EMOJI_ID_FOR_POS4")
    async def soft_support_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.event_cog.select_callback(interaction, "4")

    @disnake.ui.button(label="Hard Support", style=disnake.ButtonStyle.secondary, emoji="Your_EMOJI_ID_FOR_POS5")
    async def hard_support_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.event_cog.select_callback(interaction, "5")

class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="close")
    async def close_command(self, ctx, *, action: str):
        if action == "create" and any(role.name == "NAME_ROLE_FOR_available_COMMAND" for role in ctx.author.roles) and ctx.author == ctx.message.author:
            view = SelectGames(self)
            embed = self.generate_event_embed()
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send("У вас нет прав для выполнения этой команды.")

    async def select_callback(self, interaction: disnake.MessageInteraction, role_value):
        try:
            user_id = interaction.user.id

            if user_id in user_roles:
                if user_roles[user_id] == role_value:
                    event_participants[role_value].remove(user_id)
                    event_participants["all"].remove(user_id)
                    del user_roles[user_id]
                    await interaction.response.send_message(
                        content=f"Вы выписаны из роли {self.role_name(role_value)}.",
                        ephemeral=True
                    )
                else:
                    prev_role = user_roles[user_id]
                    event_participants[prev_role].remove(user_id)
                    event_participants[role_value].append(user_id)
                    user_roles[user_id] = role_value
                    await interaction.response.send_message(
                        content=f"Вы переведены с {self.role_name(prev_role)} на {self.role_name(role_value)}.",
                        ephemeral=True
                    )
            else:
                if len(event_participants[role_value]) < 2 and len(event_participants["all"]) < 10:
                    event_participants[role_value].append(user_id)
                    event_participants["all"].append(user_id)
                    user_roles[user_id] = role_value
                    participants_mentions = ", ".join([f"<@{user_id}>" for user_id in event_participants[role_value]])
                    await interaction.response.send_message(
                        content=f"Вы записаны на ивент как {self.role_name(role_value)}: {participants_mentions}.",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        content="На выбранной вами роли уже лимит игроков, пожалуйста, выберите другую.",
                        ephemeral=True
                    )

            embed = self.generate_event_embed()
            await self.update_event_embed(interaction, embed)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            raise e

    def role_name(self, role_value):
        role_names = {
            "1": "Легкая линия",
            "2": "Мид",
            "3": "Сложная линия",
            "4": "Частичная поддержка",
            "5": "Полная поддержка"
        }
        return role_names.get(role_value, "")

    def generate_event_embed(self):
        embed = disnake.Embed(title="Запись на Dota Positions", color=disnake.Color.blue())
        total_players = 0

        for role, participants in event_participants.items():
            role_name = self.role_name(role)
            if role_name:
                participants_mentions = "\n".join([f"<@{user_id}>" for user_id in participants])
                embed.add_field(name=f"{role_name}", value=participants_mentions or "Нет участников", inline=False)
                total_players += len(participants)

        embed.add_field(name="Количество участников", value=f"{total_players} из 10", inline=False)
        embed.add_field(name="Для начала игры необходимо еще", value=f"{10 - total_players} игроков!", inline=False)

        return embed

    async def update_event_embed(self, interaction, embed):
        try:
            await interaction.message.edit(embed=embed)
        except Exception as e:
            print(f"Ошибка при обновлении сообщения с информацией о событии: {e}")

def setup(bot):
    bot.add_cog(EventCog(bot))
