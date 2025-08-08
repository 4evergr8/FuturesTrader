import getpass
import time
from binance.um_futures import UMFutures
from alart import alart
from config import load_config
from dec import decrypt




proxies = { 'https': 'http://127.0.0.1:7890' }
password = getpass.getpass("密码：")
config=load_config()
api_secret = decrypt(config['api_secret'],password)
api_key = decrypt(config['api_key'],password)
sendkey = decrypt(config['sendkey'],password)
percent = config['percent']
symbol = config['symbol']
leverage = config['leverage']
usdt = config['usdt']
timeout = config['timeout']

while True:


    client = UMFutures(key=api_key, secret=api_secret,proxies=proxies)
    client.change_leverage(symbol=symbol, leverage=leverage)
    positions = client.get_position_risk(symbol=symbol)
    orders = client.get_orders(symbol=symbol)
    amt = 0.00


    if positions:
        for pos in positions:
            amt = float(pos['positionAmt'])
            entryPrice = float(pos['entryPrice'])
            unRealizedProfit = float(pos['unRealizedProfit'])  # 未实现盈亏
            isolatedWallet = float(pos['isolatedWallet'])  # 仓位初始保证金
            positionSide = pos.get('positionSide', 'N/A')  # 多空方向，有的接口有这个字段
            pnlRatio = unRealizedProfit / isolatedWallet if isolatedWallet != 0 else 0

            print(f"数量: {amt:.4f} | 均价: {entryPrice:.4f} | 未实现盈亏: {unRealizedProfit:.4f} | "
                  f"保证金: {isolatedWallet:.4f} | 盈亏比例: {pnlRatio:.2%} | 方向: {positionSide}")

            if unRealizedProfit <= 0 and abs(pnlRatio) >= 0.2:
                alart(sendkey=sendkey,
                      title="亏损告警",
                      content=(f"数量: {amt:.4f} | 均价: {entryPrice:.4f} | "
                               f"未实现盈亏: {unRealizedProfit:.4f} | 盈亏比例: {pnlRatio:.2%}"))




    if orders:
        for order in orders:
            side = order['side']
            origQty = float(order['origQty'])
            executedQty = float(order['executedQty'])
            activatePrice = float(order.get('activatePrice', 0) or 0)
            stopPrice = float(order.get('stopPrice', 0) or 0)
            priceRate = float(order.get('priceRate', 0) or 0)
            status = order.get('status', '未知状态')

            print(f"方向: {side} | 总数量: {origQty:.4f} | 已成交: {executedQty:.4f} | 状态: {status} | "
                  f"触发价: {activatePrice:.4f} | 回调比例: {priceRate:.2f}% | 止损价: {stopPrice:.4f}")

    if not orders and not positions:
        alart(sendkey=sendkey, title="无仓位,无挂单", content="无仓位,无挂单")
        price = float(client.ticker_price(symbol=symbol)['price'])
        quantity = round(usdt / price, 2)
        order = client.new_order(
            symbol=symbol,
            side='BUY',
            type="TRAILING_STOP_MARKET",
            quantity=quantity,
            callbackRate=percent,
            workingType="MARK_PRICE"
        )

        print(
            f"订单ID: {order.get('orderId')} | 类型: {order.get('type')} | 方向: {order.get('side')} | 位置方向: {order.get('positionSide')} | "
            f"状态: {order.get('status')} | 原始价格: {float(order.get('price', 0)):.4f} | 平均成交价: {float(order.get('avgPrice', 0)):.4f} | "
            f"原始数量: {float(order.get('origQty', 0)):.4f} | 已成交数量: {float(order.get('executedQty', 0)):.4f} | "
            f"触发价: {float(order.get('activatePrice', 0)):.4f} | 回调比例: {float(order.get('priceRate', 0)):.2f}% | 止损价: {float(order.get('stopPrice', 0)):.4f} | "
            f"时间限制: {order.get('timeInForce')} | 工作类型: {order.get('workingType')} | 限价保护: {order.get('priceProtect')}"
        )
        order = client.new_order(
            symbol=symbol,
            side='SELL',
            type="TRAILING_STOP_MARKET",
            quantity=quantity,
            callbackRate=percent,
            workingType="MARK_PRICE"
        )
        print(
            f"订单ID: {order.get('orderId')} | 类型: {order.get('type')} | 方向: {order.get('side')} | 位置方向: {order.get('positionSide')} | "
            f"状态: {order.get('status')} | 原始价格: {float(order.get('price', 0)):.4f} | 平均成交价: {float(order.get('avgPrice', 0)):.4f} | "
            f"原始数量: {float(order.get('origQty', 0)):.4f} | 已成交数量: {float(order.get('executedQty', 0)):.4f} | "
            f"触发价: {float(order.get('activatePrice', 0)):.4f} | 回调比例: {float(order.get('priceRate', 0)):.2f}% | 止损价: {float(order.get('stopPrice', 0)):.4f} | "
            f"时间限制: {order.get('timeInForce')} | 工作类型: {order.get('workingType')} | 限价保护: {order.get('priceProtect')}"
        )


    has_buy_order = any(order['side'].upper() == 'BUY' for order in orders)
    has_sell_order = any(order['side'].upper() == 'SELL' for order in orders)

    if amt < 0 and not has_buy_order:
        order = client.new_order(
            symbol=symbol,
            side='BUY',
            type="TRAILING_STOP_MARKET",
            quantity=2 * abs(amt),
            callbackRate=percent,
            activationPrice=round(entryPrice / (1 + (percent + 0.5) / 100),2),
            workingType="MARK_PRICE"
        )

        print(
            f"订单ID: {order.get('orderId')} | 类型: {order.get('type')} | 方向: {order.get('side')} | 位置方向: {order.get('positionSide')} | "
            f"状态: {order.get('status')} | 原始价格: {float(order.get('price', 0)):.4f} | 平均成交价: {float(order.get('avgPrice', 0)):.4f} | "
            f"原始数量: {float(order.get('origQty', 0)):.4f} | 已成交数量: {float(order.get('executedQty', 0)):.4f} | "
            f"触发价: {float(order.get('activatePrice', 0)):.4f} | 回调比例: {float(order.get('priceRate', 0)):.2f}% | 止损价: {float(order.get('stopPrice', 0)):.4f} | "
            f"时间限制: {order.get('timeInForce')} | 工作类型: {order.get('workingType')} | 限价保护: {order.get('priceProtect')}"
        )

    if amt > 0 and not has_sell_order:
        order = client.new_order(
            symbol=symbol,
            side='SELL',
            type="TRAILING_STOP_MARKET",
            quantity=2 * abs(amt),
            callbackRate=percent,
            activationPrice=round(entryPrice / (1 - (percent + 0.5) / 100),2),
            workingType="MARK_PRICE"
        )
        print(
            f"订单ID: {order.get('orderId')} | 类型: {order.get('type')} | 方向: {order.get('side')} | 位置方向: {order.get('positionSide')} | "
            f"状态: {order.get('status')} | 原始价格: {float(order.get('price', 0)):.4f} | 平均成交价: {float(order.get('avgPrice', 0)):.4f} | "
            f"原始数量: {float(order.get('origQty', 0)):.4f} | 已成交数量: {float(order.get('executedQty', 0)):.4f} | "
            f"触发价: {float(order.get('activatePrice', 0)):.4f} | 回调比例: {float(order.get('priceRate', 0)):.2f}% | 止损价: {float(order.get('stopPrice', 0)):.4f} | "
            f"时间限制: {order.get('timeInForce')} | 工作类型: {order.get('workingType')} | 限价保护: {order.get('priceProtect')}"
        )

    time.sleep(timeout)

