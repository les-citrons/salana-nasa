import discord
from discord.ext import commands
import functools
from functools import lru_cache

import econ

CURRENCY = "mani"

def setup(client):
    client.add_cog(econ_cog(client))

@lru_cache(maxsize=None)
class econ_cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pay(self, ctx, who: discord.User, what: float):
        if who == ctx.author:
            await ctx.send("You cannot pay yourself.")
            return
        if what <= 0:
            await ctx.send("Invalid amount.")
            return
        
        from_acc = econ.get_account(ctx.author.id)
        to_acc = econ.get_account(who.id)

        if from_acc.balance < what:
            await ctx.send("Insufficient funs.")
            return
        
        from_acc.transact(-what)
        to_acc.transact(what)

        econ.save_bank()

        await ctx.send(f"You have transfered {what} {CURRENCY} to {who.name}.")

    @commands.command()
    async def give(self, ctx, who: discord.User, what: int, collection="default"):
        if who == ctx.author:
            await ctx.send("You cannot give a number to yourself.")
            return

        what = round(what, 2)
        
        from_acc = econ.get_account(ctx.author.id)
        to_acc = econ.get_account(who.id)

        if not collection in from_acc.number_collection.keys():
            await ctx.send(f"Collection '{collection}' does not exist.")
            return
        if not what in from_acc.number_collection[collection]:
            await ctx.send(f"Number '{what}' is not in collection '{collection}'.")
            return

        from_acc.remove_number(what, collection)
        to_acc.add_number(what, "default")
        
        econ.save_bank()

        await ctx.send(
                f"You have transfered '{what}' from your collection '{collection}' to {who.name}.")

    @commands.command()
    async def balance(self, ctx):
        balance = econ.get_account(ctx.author.id).balance
        embed = discord.Embed()
        embed.add_field(name='Balance:', value=f"{balance} {CURRENCY}")

        await ctx.send(embed=embed)

    @commands.command(aliases=['ls'])
    async def numbers(self, ctx, collection="default"):
        number_collection = econ.get_account(ctx.author.id).number_collection
        if collection in number_collection.keys():
            if len(number_collection[collection]) > 0:
                numbers = [str(x) for x in number_collection[collection]]
                embed = discord.Embed(title=f"Numbers in your collection '{collection}':",
                        description="\n".join(numbers))
                await ctx.send(embed=embed)
            else:
                await ctx.send("There are no numbers in your collection.")
        else:
            await ctx.send("That collection does not exist.")

    @commands.command(aliases=['nc','new'])
    async def newcollection(self, ctx, name):
        acc = econ.get_account(ctx.author.id)
        if name in acc.number_collection.keys():
            await ctx.send("You already have a collection with this name.")
            return
        acc.create_collection(name)
        await ctx.send("Collection created.")

        econ.save_bank()

    @commands.command(aliases=['lsc'])
    async def collections(self, ctx):
        acc = econ.get_account(ctx.author.id)
        embed = discord.Embed(title=f"Your collections:")
        for collection in acc.number_collection.keys():
            n_count = len(acc.number_collection[collection])
            embed.add_field(name=collection,value=f"{n_count} numbers")

        await ctx.send(embed=embed)

    @commands.command(aliases=['rmc','delc'])
    async def delcollection(self, ctx, collection):
        acc = econ.get_account(ctx.author.id)
        if not name in acc.number_collection.keys():
            await ctx.send("That collection does not exist.")
            return
        acc.remove_collection(name)
        await ctx.send(f"Collection '{name}' has been removed. \
                Its numbers are now in your default collection.")
        
        econ.save_bank()

    @commands.command(aliases=['mv', 'move'])
    async def movenumber(self, ctx, number: int, destination, source="default"):
        acc = econ.get_account(ctx.author.id)
        if not source in acc.number_collection.keys() and \
                destination in acc.number_collection.keys():
            await ctx.send("Invalid source or destination.")
            return
        if not number in acc.number_collection[source]:
            await ctx.send(f"Number {number} is not in source.")
            return
        acc.remove_number(source, number)
        acc.add_number(destination, number)
        await ctx.send("Number moved.")

        econ.save_bank()
