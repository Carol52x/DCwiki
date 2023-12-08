from datetime import datetime
import discord
from discord.ext import commands
import requests
from selectolax.parser import HTMLParser

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.command(name="get", aliases=['Get', 'GET'])
async def get(ctx, *args):
    name = '_'.join(args).title()
    top_role = ctx.author.top_role
    url = f'https://www.detectiveconanworld.com/wiki/{name}'

    response = requests.get(url)
    spoiler_keywords = ["Akai_family%27s_middle_brother", "Akai_family%27s_mother", "Scotch", "Old_man", "Bourbon", "Unknown_Child", "The_Boss", "Rum"]

    if not any(keyword in name for keyword in spoiler_keywords):
        if response.ok:
            html = HTMLParser(response.text)
            try:
                p_elements = html.css('div.mw-parser-output > p')
                description = p_elements[0].text(deep=True) + p_elements[1].text(deep=True)

                image_elements = html.css('img')
                image_src = None

                for element in image_elements:
                    src = element.attributes.get('src')
                    if src and "/wiki/images/thumb/6/65/Detective_boys_badge2.png/80px-Detective_boys_badge2.png" not in src and "/wiki/images/f/f4/Ambox_content.png" not in src:
                        image_src = src
                        break

                user = ctx.author
                embed = discord.Embed(title=name.replace('_', ' '), description=description, color=top_role.color)
                embed.add_field(name="More Info", value=f"[Find more info]({url})", inline=False)
                if image_src:
                    embed.set_thumbnail(url=f"https://www.detectiveconanworld.com/{image_src}")
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text=f"Requested by {user.name} (ID: {user.id})")
                await ctx.send(embed=embed)
            except IndexError:
                await ctx.send("Please write the full name if possible")
        else:
            await ctx.send('Sorry, I could not find that content.')
    else:
        user = ctx.author
        embed = discord.Embed(title='Spoiler',
                              description="The content you're searching for is probably a spoiler. Click the link below to reveal the spoiler!",
                              color=top_role.color)
        embed.add_field(name="More Info", value=f"[Click here]({url})", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f"Requested by {user.name} (ID: {user.id})")
        embed.set_thumbnail(url="https://www.detectiveconanworld.com/wiki/images/f/f4/Ambox_content.png")
        await ctx.send(embed=embed)




bot.run('')
