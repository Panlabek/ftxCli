import ccxt
import sys
from pprint import pprint
import time
from decouple import config
key = config('API_KEY')
secret = config('API_SECRET') 
colors = {"green": "\u001b[32m",
          "black": "\u001b[30m",
            "red": "\u001b[31m",
        "magenta": "\u001b[35m",
         "yellow": "\u001b[33m",
           "blue": "\u002b[34m",
           "cyan": "\u001b[36m",
          "white": "\u001b[37m",
          "reset": "\u001b[0m",
          "bright_black": "\u001b[30;1m",
            "bright_red": "\u001b[31;1m",
          "bright_green": "\u001b[32;1m",
          "bright_yellow": "\u001b[33;1m",
          "bright_blue": "\u001b[34;1m",
          "bright_magenta": "\u001b[35;1m",
          "bright_cyan": "\u001b[36;1m",
          "bright_white": "\u001b[37;1m",
          }
exchange = ccxt.ftx({
    "apiKey": str(key),
    "secret": str(secret),

})
exchange.load_markets() 
def cancel_all_orders(symbol: str=None) -> None:
    res = exchange.cancel_all_orders(symbol)
    green = colors["bright_green"]
    reset = colors["reset"]
    print(f"{green}{res}{reset}")

def scaled_order(symbol: str, side: str, total: float, start_price: float, end_price: float, num_orders: int) -> None:
    total = float(total)
    start_price = float(start_price)
    end_price = float(end_price)
    num_orders = int(num_orders)
    params = {"postOnly": True}
    order_amount = total / num_orders
    step_size = (end_price - start_price)/(num_orders-1)
    green = colors["bright_green"]
    reset = colors["reset"]
    blue = colors["bright_blue"]
    magenta = colors["bright_magenta"]
    for order_num in range(num_orders):
        order_price = start_price + step_size * order_num
        exchange.create_order(symbol, "limit", side, order_amount, order_price, params)
        print(f"{green}Order{reset} {blue}{order_num+1}{reset} {green}placed at price:{reset} {magenta}{order_price}${reset}")

def limit_order(symbol: str, side: str, amount: float, price: float) -> None:
    amount = float(amount)
    price = float(price)
    params = {"postOnly": True}
    response = exchange.create_limit_order(symbol, side, amount, price, params)
    order_id = response["info"]["id"]
    green = colors["bright_green"]
    blue = colors["bright_blue"]
    reset = colors["reset"]
    print(f"{green}Limit order{reset} {blue}{order_id}{reset} {green}has been placed successfully!{reset}")

def market_order(symbol: str, side: str, amount: float) -> None:
    amount = float(amount)
    response = exchange.create_market_order(symbol, side, amount)
    order_id = response["info"]
    green = colors["bright_green"]
    blue = colors["bright_blue"]
    reset = colors["reset"]
    print(f"{green}Market order{reset} {blue}{order_id}{reset} {green}has been placed successfully!{reset}")

def fetch_top_orderbook(symbol: str) -> list[float]:
    res = exchange.fetch_order_book(symbol)
    top_bid = res["bids"][0][0]
    top_ask = res["asks"][0][0]
    return [top_bid, top_ask]

def limit_chaser(symbol: str, side: str, amount: float, offset: float) -> None:
    amount = float(amount)
    offset = float(offset)
    side = side.lower()
    params = {"postOnly": True}
    last_order = None
    remaining = amount
    green = colors["bright_green"]
    reset = colors["reset"]
    yellow = colors["bright_yellow"]
    try:
        while(True):
            top_of_book = fetch_top_orderbook(symbol)
            if(side == "sell"):
                price = top_of_book[0] + offset
                if(not last_order):
                    last_order = exchange.create_order(symbol, "limit", side, remaining, price, params)
                else:
                    last_order = exchange.fetch_order(last_order["id"])
                if last_order["status"] == "closed":
                    order_market = last_order["symbol"]
                    print(f"{green}Limit chased on market{reset} {yellow}{order_market}{reset} {green}Successfully{reset}")
                    return
                if top_of_book[0] + offset < last_order["price"]:
                    print(f"{yellow}Resubmitting order{reset}")
                    exchange.cancel_order(last_order["id"])
                    last_order = exchange.fetch_order(last_order["id"])
                    remaining = last_order["remaining"]
                    last_order = exchange.create_order(symbol, "limit", side, remaining, price, params)
            elif(side == "buy"):
                price = top_of_book[1] - offset
                if(not last_order):
                    last_order = exchange.create_order(symbol, "limit", side, remaining, price, params)
                else:
                    last_order = exchange.fetch_order(last_order["id"])
                if last_order["status"] == "closed":
                    order_market = last_order["symbol"]
                    print(f"{green}Limit chased on market{reset} {yellow}{order_market}{reset} {green}Successfully{reset}")
                    return
                if top_of_book[1] - offset > last_order["price"]:
                    print(f"{yellow}Resubmitting order{reset}")
                    exchange.cancel_order(last_order["id"])
                    last_order = exchange.fetch_order(last_order["id"])
                    remaining = last_order["remaining"]
                    last_order = exchange.create_order(symbol, "limit", side, remaining, price, params)
            time.sleep(2)
    except KeyboardInterrupt as e:
        if(last_order):
            exchange.cancel_order(last_order["id"])
        raise e
    except Exception as e:
        if(last_order):
            exchange.cancel_order(last_order["id"])
        raise e
def list_all_active_orders(symbol=None) -> None:
    green = colors["bright_green"]
    reset = colors["reset"]
    red = colors["bright_red"]
    cyan = colors["bright_cyan"]
    yellow = colors["bright_yellow"]
    magenta = colors["bright_magenta"]
    blue = colors["bright_blue"]
    if symbol == None:
        res = exchange.fetch_open_orders()
        choice = input(f"{cyan}Do you want to get shortened version of open orders data ({reset}{green}Y{reset}/{red}N{reset}{cyan}):{reset} ")
        if choice.lower() == "y":
            for order in res:
                market = order["symbol"]
                amount = order["amount"]
                order_id = order["id"]
                filled = order["filled"]
                price = order["price"]
                liquidation = order["info"]["liquidation"]
                print(f"order market: {yellow}{market}{reset}, order amount: {magenta}{amount}{reset}, order id: {blue}{order_id}{reset}, how much filled: {magenta}{filled}{reset},"
                      f"order price: {magenta}{price}{reset}, order liquidation: {magenta}{liquidation}{reset}")
        else:
            pprint(res)
    else:
        res = exchange.fetch_open_orders(symbol)
        choice = input(f"{cyan}Do you want to get shortened version of {yellow}{symbol}{reset} open orders data ({reset}{green}Y{reset}/{red}N{reset}{cyan}):{reset} ")
        if choice == "y":
            for order in res:
                amount = order["amount"]
                order_id = order["id"]
                filled = order["filled"]
                price = order["price"]
                liquidation = order["info"]["liquidation"]
                print(f"order amount: {magenta}{amount}{reset}, order id: {blue}{order_id}{reset}, how much filled: {magenta}{filled}{reset},"
                      f"order price: {magenta}{price}{reset}, order liquidation: {magenta}{liquidation}{reset}")
        else:
            pprint("res")

def list_positions() -> None:
    #BASICALY FUNCTION CHECKS FOR FRESH POSITIONS
    res = exchange.fetch_positions()
    magenta = colors["bright_magenta"]
    yellow = colors["bright_yellow"]
    blue = colors["bright_blue"]
    reset = colors["reset"]
    for position in res:
        if position["info"]["recentPnl"] != None:
            market = position["symbol"]
            side = position["info"]["side"]
            markPrice = position["markPrice"]
            notional_value = position["notional"]
            prcnt_gain_lose = position["percentage"]
            pnl = position["info"]["recentPnl"]
            entry_price = position["info"]["entryPrice"]
            liquidation = position["info"]["estimatedLiquidationPrice"]
            if side == "buy":
                side_color = colors["bright_green"]
            else:
                side_color = colors["bright_red"]
            if prcnt_gain_lose > 0:
                prcnt_color = colors["green"]
            else:
                prcnt_color = colors["red"]
            print(f"Position Market: {yellow}{market}{reset}, Side: {side_color}{side}{reset}, MarkPrice: {magenta}{markPrice}{reset},"
                  f"Notional Value: {magenta}{notional_value}{reset}, Percent Change: {prcnt_color}{prcnt_gain_lose}{reset}%,"
                  f"PNL: {prcnt_color}{pnl}{reset}, Entry Price: {magenta}{entry_price}{reset}, liquidation: {blue}{liquidation}{reset}")
        else:
            pass
def market_close_all_positions(symbol: str=None) -> None:
    res = exchange.fetch_positions(symbol)
    for position in res:
        if position["info"]["recentPnl"] != None:
            market = position["symbol"]
            side = position["info"]["side"]
            amount = position["info"]["size"]
            pnl = position["info"]["recentPnl"]
            notional_value = position["notional"]
            reset = colors["reset"]
            yellow = colors["yellow"]
            magenta = colors["magenta"] 
            if side == "buy":
                side_color = colors["bright_green"]
                exchange.create_market_order(market, "sell", amount)
                print(f"Position on {yellow}{market}{reset} has been closed, Side: {side_color}{side}{reset}, Notional Value: {magenta}{notional_value}{reset}, PNL: {magenta}{pnl}{reset}")
            else:
                side_color = colors["bright_red"]
                exchange.create_market_order(market, "buy", amount)
                print(f"Position on {yellow}{market}{reset} has been closed, Side: {side_color}{side}{reset}, Notional Value: {magenta}{notional_value}{reset}, PNL: {magenta}{pnl}{reset}")
def chase_close_all_positions(symbol: str=None) -> None:
    res = exchange.fetch_positions(symbol)
    for position in res:
        if position["info"]["recentPnl"] != None:
            market = position["symbol"]
            side = position["info"]["side"]
            amount = position["info"]["size"]
            notional_value = position["notional"]
            pnl = position["info"]["recentPnl"]
            offset = float(position["markPrice"]) * 0.003
            reset = colors["reset"]
            yellow = colors["yellow"]
            magenta = colors["magenta"] 
            if side == "buy":
                side_color = colors["bright_green"]
                limit_chaser(market, "sell", amount, offset)
                print(f"Position on {yellow}{market}{reset} has been closed, Side: {side_color}{side}{reset}, Notional Value: {magenta}{notional_value}{reset}, PNL: {magenta}{pnl}{reset}")
            else:
                side_color = colors["bright_red"]
                limit_chaser(market, "buy", amount, offset)
                print(f"Position on {yellow}{market}{reset} has been closed, Side: {side_color}{side}{reset}, Notional Value: {magenta}{notional_value}{reset}, PNL: {magenta}{pnl}{reset}")
def help() -> None:
    # MAKE A DICT FOR FUNCTION NAMES AND ARGS THAT THEY TAKE
    # THIS WILL BE EASIER FOR THE FUTURE MANAGEMENT
    cyan = colors["bright_cyan"]
    reset = colors["reset"]
    magenta = colors["bright_magenta"]
    yellow = colors["bright_yellow"]
    available_functions = {"cancel_all_orders": ["symbol: str Default=None"],
                           "scaled_order": ["symbol: str", "side: str", "total_amount_to_buy: float", "start_price: float", "end_price: float", "number_of_orders: int"],
                           "limit_order": ["symbol: str", "side: str", "amount_to_buy: float", "price: float"],
                           "market_order": ["symbol: str", "side: str", "amount_to_buy: flaot"],
                           "limit_chaser": ["symbol: str", "side: str", "amount_to_buy: float", "offset: float"],
                           "list_all_active_orders": ["symbol: str Default=None"],
                           "list_positions": [None],
                           "market_close_all_positions": ["symbol: str Default=None"],
                           "chase_close_all_positions": ["symbol: str Default=None"]}
    for key, value in available_functions.items():
        print(f"function: {cyan}{key}{reset} | args: {magenta}{value}{reset}")
    print(f"{yellow}How to use a function(mini tutorial): for example. cancel_all_orders AVAX-PERP{reset}")
    pass
def main():
    func_name = sys.argv[1]
    args = sys.argv[2:]
    globals()[func_name](*args)

if __name__ == "__main__":
    main()
