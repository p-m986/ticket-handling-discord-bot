import discord

class create_embed():
    def __init__(self):
        self.errorColor = 0xff7575
        self.waitColor = 0xffe100

    async def confirmMmReq(self):
        res = discord.Embed(
            title = "PLEASE CONFIRM",
            description = "Are you sure you want to request for a middle man?",
            color = self.waitColor
        )
        res.set_footer(
            text = "*Misusing this command will lead to warning*"
        )
        return res

    async def createErrorEmbed(self, title, message):
        res = discord.Embed(
            title = f"{title}",
            description = f"{message}",
            color = self.errorColor,
            timestamp = discord.utils.utcnow()
        )
        return res