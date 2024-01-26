from discord.ext import commands
from discord.ext.commands import BucketType
from cogs.controllers.create_embed import create_embed
import discord
import asyncio

# from configuration import blacklist_role_id, allowed_channel_ids
blacklist_role_id=1194577286641492069
allowed_channel_ids=[1194652099494035558, 1194653134811832451]


class confirmView(discord.ui.View):
    def __init__(self, *, timeout=20):
        super().__init__(timeout=timeout)
        self.create_embed = create_embed()

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        
        timeoutEmbed = self.create_embed(title = "Time Out", message = f'User did not react')
        await self.message.edit(content = "", view = self, embed = timeoutEmbed)
    
    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.blurple)
    async def confirm(self,interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user == self.target_user:
            # await self.message.delete()
            await interaction.response.defer()

            for item in self.children:
                item.disabled = True

            button.style = discord.ButtonStyle.green

            self.stop()
    
    
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.danger)
    async def calcel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
            item.style = discord.ButtonStyle.danger
        await self.message.edit(content = "Canceled..", view = self)
        self.stop()

class middleman_req(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.create_embed = create_embed()


    @commands.cooldown(1, 30, BucketType(1))
    @commands.hybrid_command(name="request_mm", with_app_command=True, aliases = ["reqmm"])
    async def reqmm(self, ctx: commands.context):
        """
        How it works
        >who r u dealing with
        >confirm
        >added to ticket
        >whos seller whos buyer
        >2 buttons, im seller, im buyer.
        >confirm
        >how many gems selling
        >input integer that is also round number, (we do not want 15979232) we want (15000000)
        >confirm
        >what are gems being given for
        >input
        >confirm
        >Seller send gems to Robloxaccount, click button to check 
        >button is clicked
        >checking... this may take 5 - 10 minutes
        >> checking calls a function within my devs code
        """
        print("Got Command")
        confirmEmbed = await self.create_embed.confirmMmReq()
        confirmView = confirmView()
        print("Got View object")
        response_message = await ctx.reply(embed = confirmEmbed, view = confirmView)
        await confirmView.wait()
        return


        

    @reqmm.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = await self.create_embed.createErrorEmbed(title = "Command on Cooldown", message = f'This command is on cooldown! Try  again in {round(error.retry_after, 5)} seconds')
            await ctx.reply(embed = cooldown_embed)
        # elif isinstance(error, commands.MemberNotFound):
        #     create_embed = create_embed()
        #     membererror_embed = await create_embed.createFlipErrorEmbed(title = "Not a member", message = "This is not a valid user in server or You entered the command incorrect\n[REFER HERE FOR EXAPLE](https://discord.com/channels/1194563432112996362/1194651573297623081/1195671288681873448)")
        #     await ctx.reply(embed = membererror_embed)


async def setup(bot):
    await bot.add_cog(middleman_req(bot))