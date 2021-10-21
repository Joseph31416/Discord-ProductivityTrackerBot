import discord


class Response:

    def __init__(self):
        self.color = discord.Color.blue()

    def generate_embed(self, ui):
        return self.get_method_from_msg(ui)

    def get_method_from_msg(self, ui):
        msg = ui.msg
        if "$clockin" in msg:
            return self.clocked_in(ui=ui)

        elif "$clockout" in msg:
            return self.clocked_out(ui=ui)

        elif "$time" in msg:
            return self.time(ui=ui)

        elif "$sync" in msg:
            return self.sync(ui=ui)

        elif "$" in msg:
            return self.help(ui=ui)

    def help(self, **kwargs):
        ui = kwargs.get("ui")
        user_name = ui.user_name
        embed = discord.Embed(
            title="Menu",
            description=f"Hello, {user_name}! These are the commands that you'll need",
            color=self.color)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/7d/56/62/7d5662301d9573e3f30bfdbbe401e911.jpg")
        embed.add_field(name="$clockin", value="To clock in", inline=False)
        embed.add_field(name="$clockout", value="To clock out", inline=False)
        embed.add_field(name="$time", value="To access command to see study time", inline=False)
        return embed

    def sync(self, **kwargs):
        ui = kwargs.get("ui")
        user_name = ui.user_name
        embed = discord.Embed(
            title="Sync complete!",
            description=f"Initiated by {user_name}!",
            color=self.color)
        return embed

    def clocked_in(self, **kwargs):
        ui = kwargs.get("ui", None)
        status = ui.status
        user_name = ui.user_name
        if status == 1:
            embed = discord.Embed(
                title=f"{user_name} has clocked in!",
                color=self.color)
        elif status == 0:
            embed = discord.Embed(
                title=f"{user_name} is already clocked in!",
                color=self.color)
        else:
            embed = None
        return embed

    def clocked_out(self, **kwargs):
        ui = kwargs.get("ui", None)
        status = ui.status
        user_name = ui.user_name
        if status == 1:
            embed = discord.Embed(
                title=f"{user_name} has clocked out!",
                color=self.color)
        elif status == 0 or status is None:
            embed = discord.Embed(
                title=f"{user_name} has yet to clock in!",
                color=self.color)
        else:
            embed = None
        return embed

    def time(self, **kwargs):
        ui = kwargs.get("ui", None)
        status = ui.status
        title = ui.title
        name_duration = ui.name_duration

        if status == 1:
            embed = discord.Embed(
                title=f"{title} Study Time",
                color=self.color)
            for name in name_duration:
                duration = name_duration[name]
                embed.add_field(name=name, value=f"Duration: {duration[0]}h {duration[1]} min {duration[2]} sec",
                                inline=False)
        elif status == 2:
            embed = discord.Embed(
                title="No records found",
                description="Try clocking in!",
                color=self.color)

        else:
            embed = discord.Embed(
                title="Time commands",
                description="These are the commands to access study time",
                color=self.color)
            embed.add_field(name="$time total <name>", value="Get total study time", inline=False)
            embed.add_field(name="$time weekly <name>", value="Get weekly study time", inline=False)
            embed.add_field(name="$time daily <name>", value="Get total study time", inline=False)
            embed.set_footer(text="<name> is optional")

        return embed
