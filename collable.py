import discord
import asyncio
from discord.ext import commands
from re import sub

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help') #removing the default help command
channel = role = embed = embed_message = artist = None
index = 0
full_squares = ""

@bot.event
async def on_ready():
    print("Connected\n")

@bot.command()
async def select(ctx, *, arg):
    if ctx.message.author.id != 455301777055547394:
        return

    global channel, role
    args = arg.split()
    channel = bot.get_channel(int(args[0]))
    role = ctx.guild.get_role(int(args[1]))
    await ctx.send(f"{channel.mention} and \"@{role.name}\" selected.")

@bot.command()
async def start(ctx, *, arg):
    if ctx.message.author.id != 455301777055547394:
        return

    global channel, embed, embed_message, artist
    artist = arg.upper()
    blanks = sub(r"\w","_ ",artist)
    blanks = sub(r" ","  ",blanks)
    embed_title = discord.Embed(title="HEALTH COLLABLE", description= " ", color= 0xff0000)
    embed = discord.Embed(title="GUESS A COLLABORATION FROM DISCO4 :: PART II", description=f"Type the name of the artist```{blanks}```", color=0xff0000)
    await channel.send(embed= embed_title)
    embed_message = await channel.send(embed= embed)

def check_word(guess, artist):
    print(guess, artist)
    visited = dict()
    green = "🟩"
    yellow = "🟨"
    black = "⬛"
    guess_split = guess.split()
    artist_split = artist.split()
    squares = list()

    for guess_word, artist_word in zip(guess_split, artist_split):
        if len(guess_word) != len(artist_word):
            return "error"

    for guess_word, artist_word in zip(guess_split, artist_split):
        visited_aux, squares_word = zip(*[((letter,artist_word.count(letter) - 1), green) if letter == real_letter else ((letter,artist_word.count(letter)), black) for letter, real_letter in zip(guess_word, artist_word)])
        visited_aux = list(visited_aux)
        squares_word = list(squares_word)
        
        for letter,count in visited_aux:
            if letter not in visited:
                visited[letter] = count

        for i, (letter, real_letter) in enumerate(zip(guess_word, artist_word)):
            if letter == real_letter:
                continue

            if letter in artist and visited[letter] > 0:
                squares_word[i] = yellow
                visited[letter] -= 1

        squares.append(str().join(squares_word))

    return '  '.join(squares)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    global channel, role, embed, index, embed_message, artist, full_squares
    if channel and message.channel == channel:
        error_embed = discord.Embed(title="Please enter the correct number of characters.", description= " ")
        if len(message.content) != len(artist):
            error_embed = discord.Embed(title="Please enter the correct number of characters.")
            error_message = await channel.send(embed= error_embed)
            await message.delete()
            await asyncio.sleep(3)
            await error_message.delete()
        else:
            index += 1
            if index > 6:
                await channel.send("WRONG ARTIST NAME. SEE YOU NEXT TIME.")
                await message.author.remove_roles(role)
            else:
                squares = check_word(message.content.upper(), artist)
                if squares != "error":
                    full_squares += squares + "\n"
                    embed.add_field(name=squares, value=message.content.upper(), inline=False)
                    await embed_message.edit(embed= embed)
                    if "🟨" not in squares and "⬛" not in squares:
                        full_squares = full_squares.replace("  ",".")
                        full_squares = full_squares.replace(" ","")
                        full_squares = full_squares.replace(".","   ")
                        success_embed = discord.Embed(title="YOU DID A HEALTH OF A JOB", description=f"COLLABLE 2 {str(index)}/6\n\n{full_squares}")
                        await channel.send(embed= success_embed)
                        await message.author.remove_roles(role)
                else:
                    error_message = await channel.send(embed= error_embed)
                    await message.delete()
                    await asyncio.sleep(3)
                    await error_message.delete()

bot.run("bot-token")