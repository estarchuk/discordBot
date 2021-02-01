from discord.ext import commands
import stonkPrice


class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def price(self, ctx, market, stock):
        stock = stock.upper()
        if market == "c":
            crypto_price = stonkPrice.getCrypto(stock)
            full = crypto_price
            data = full['data']
            quote = data['quote']
            name = data['name']
            local_currency = quote['CAD']
            coin_price = '{:.2f}'.format(local_currency['price'])
            currency = 'CAD'
            await ctx.send('The current price of ' + name + ' is ' + coin_price + " " + currency)
        elif market == 's':
            stock_price = stonkPrice.getStock(stock)
            share_price = '{:.2f}'.format(stock_price)
            name = stock
            currency = 'USD'

            await ctx.send(
                'The current price of ' + name + ' is ' + share_price + ' ' + currency
            )


def setup(bot):
    bot.add_cog(StockCog(bot))
