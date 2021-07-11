#weather bot

import logging
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp 

logging.basicConfig(level=logging.WARNING)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
WEATHER_API = os.getenv("WEATHER_API")
CHANNEL = int(os.getenv("DISCORD_CHANNEL"))
URL = "https://api.openweathermap.org/data/2.5/weather?"

async def async_weather(params):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.openweathermap.org/data/2.5/weather?", params=params) as response:
            weather = await response.json()
            return weather

def main():

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is ready to Discord!')

    @bot.event
    async def on_connect():
        channel = bot.get_channel(CHANNEL)
        print(channel)
        await channel.send("Entti is here!")
        print(f'{bot.user.name} has connected to Discord!')

    @bot.command(name="weather")
    async def weather(ctx, arg):
        author = ctx.author
        city = arg
        #isalpha() checks that all characters are letters
        if city.isalpha():
            params = {"q":city, "units": "metric", "appid":WEATHER_API}
            res = await async_weather(params)
            weather = res["main"]
            temp = weather["temp"]
            humidity = weather["humidity"]
            feel = weather["feels_like"]
            await ctx.send(f"""Hey {author} Here is the weather in {city}:
            temperature: {temp} 
            feels like: {feel}
            humidity: {humidity}""")
        else: 
            await ctx.send("Check city name")

    @weather.error
    async def weather_error(ctx, error):
        await ctx.send("Give the city -> !weather city")

    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        bot.close()
    finally:
        print("Disconnected")

if __name__ == "__main__":
    main()