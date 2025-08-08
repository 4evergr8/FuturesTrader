import os
from binance.um_futures import UMFutures
import re
import requests





api_secret = os.getenv("API_SECRET")
api_key = os.getenv("API_KEY")
sendkey = os.getenv("SENDKEY")








def alart(sendkey,title,content):

    print(content)

    num = re.search(r'sctp(\d+)t', sendkey).group(1)
    url = f'https://{num}.push.ft07.com/send/{sendkey}.send'

    data = {
        'title': title,
        'desp': content,
    }

    print(requests.post(url, json=data).json())






amt = 0.00
percent = 0.8
symbol = 'SOLUSDT'
client = UMFutures(key=api_key, secret=api_secret)
client.change_leverage(symbol=symbol, leverage=20)
positions = client.get_position_risk(symbol=symbol)
orders = client.get_orders(symbol=symbol)




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
    exit(0)

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
        f"订单ID: {order.get('orderId')} | 符号: {order.get('symbol')} | 类型: {order.get('type')} | 方向: {order.get('side')} | 位置方向: {order.get('positionSide')} | "
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
        f"订单ID: {order.get('orderId')} | 符号: {order.get('symbol')} | 类型: {order.get('type')} | 方向: {order.get('side')} | 位置方向: {order.get('positionSide')} | "
        f"状态: {order.get('status')} | 原始价格: {float(order.get('price', 0)):.4f} | 平均成交价: {float(order.get('avgPrice', 0)):.4f} | "
        f"原始数量: {float(order.get('origQty', 0)):.4f} | 已成交数量: {float(order.get('executedQty', 0)):.4f} | "
        f"触发价: {float(order.get('activatePrice', 0)):.4f} | 回调比例: {float(order.get('priceRate', 0)):.2f}% | 止损价: {float(order.get('stopPrice', 0)):.4f} | "
        f"时间限制: {order.get('timeInForce')} | 工作类型: {order.get('workingType')} | 限价保护: {order.get('priceProtect')}"
    )



