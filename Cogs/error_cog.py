from discord import Emoji
from discord.ext.commands import (
    Cog,
    Bot,
    Context,
    HelpCommand,
    command,
    is_owner,
    Group,
    Command,
)
from Cogs.app import table, make_embed as me

EMBED_IDENTIFIER = "ERROR_CMD_HELP"
E_CH_REACTION_ACCEPT = "๐"


async def era_e_ch(bot: Bot, usr_id: int, ctx: Context, react: Emoji, arg: list):
    if str(react) == E_CH_REACTION_ACCEPT:
        usr = bot.get_user(usr_id)
        target = arg[1]
        bot.config[str(ctx.guild.id)]["help_author"].update(
            {ctx.channel.id: {target: usr.mention}}
        )
        await ctx.send_help(target)
        await ctx.message.delete()
    else:
        pass


class OutputError(Cog):
    qualified_name = "hide"

    def __init__(self, bot):
        self.bot = bot
        self.owner = None
        self.db_cmd = table.Cmdtb()
        self.__error_title = "ใณใใณใใจใฉใผ"
        self.__error_fotter = ""
        self.__undefine_error_title = "ไบๆใใฌใจใฉใผ"
        self.__notice_owner_message = "ใใใใใจใฉใผใฃใฆใใใงใใใฉใโโ"
        self.__missing_arg_message = "ใใฎใณใใณใใซๅฟ่ฆใช่ฆ็ด ๆๅฎใ่ถณใใฆใใพใใ\r" "ใณใใณใใฎ่ฉณ็ดฐใ่กจ็คบใใพใใ๏ผ"
        self.__permission_message = "๐ขๆๅฎใใใใณใใณใใๅฎ่กใใๆจฉ้ใ่ฒดๆนใซใใใพใใ\rๅฟ่ฆใใใใฐใ็ฎก็่ใพใงๅใๅใใใใ ใใ"

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if not (self.owner):
            self.owner = self.bot.get_user(self.bot.owner_id)
            if self.owner:
                self.__notice_owner_message = (
                    self.owner.mention + self.__notice_owner_message
                )
        cmd = str()
        embed = me.MyEmbed(ctx)
        try:
            cmd = ((str(error)).split('"', maxsplit=2))[1]
            result = self.db_cmd.tbselect(cmd)
            if result:
                await ctx.send(result[0].body)
                return
            else:
                dubleq = str(error).split('"')
                embed.default_embed(
                    footer=self.__error_fotter, title=self.__error_title
                )
                if dubleq:
                    if dubleq[0] == "Command " and dubleq[2] == " is not found":
                        # await ctx.message.add_reaction("โ๐โ")
                        await ctx.message.add_reaction("โ")
                        return
                    else:
                        embed.add(
                            name=self.__undefine_error_title,
                            value=f"```{str(error)}```",
                            greeting=self.__notice_owner_message,
                        )
                else:
                    embed.add(
                        name=self.__undefine_error_title,
                        value=f"```{str(error)}```",
                        greeting=self.__notice_owner_message,
                    )
        except IndexError:
            embed.default_embed(
                footer=self.__error_fotter,
                title=self.__error_title,
                greeting=f"{ctx.author.mention}",
                time=False,
            )
            if "required argument that is missing." in str(error):
                string = f"{ctx.command}"
                # if ctx.invoked_subcommand:
                #     string = (ctx.invoked_subcommand).name
                # else:
                #     string = f"{ctx.command}"
                embed.change(
                    description=self.__missing_arg_message,
                    footer_arg=f"{EMBED_IDENTIFIER} {string}",
                    bottoms=[E_CH_REACTION_ACCEPT],
                )
            elif "You do not own this bot." in str(error):
                embed.change_description(self.__permission_message)
            elif "The check functions for command cmd failed." in str(error):
                embed.change_description(self.__permission_message)
            else:
                embed.add(
                    name=self.__undefine_error_title,
                    value=f"```{str(error)}```",
                    greeting=self.__notice_owner_message,
                )
        await embed.sendEmbed()


def setup(bot):
    bot.config["funcs"].update(
        {
            EMBED_IDENTIFIER: era_e_ch,
        }
    )
    return bot.add_cog(OutputError(bot))
    pass
