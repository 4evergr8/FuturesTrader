
# 🚀 FuturesTrader 自动交易告警脚本

一个基于 Binance 合约 API 的自动仓位监控与亏损告警脚本，结合 Server酱实现APP告警，并自动设置止损追踪单。📈📉

---

## ✨ 功能特点

- 🤖 自动获取指定交易对仓位和挂单信息  
- 📊 计算仓位未实现盈亏及亏损比例  
- 🔔 亏损超过阈值（默认20%）时，推送告警  
- 🎯 自动为无止损挂单仓位下买入或卖出追踪止损单（Trailing Stop）  
- 🖥️ 格式化打印仓位和订单详情，方便查看日志  
- ⏰ 支持 GitHub Actions 定时执行和手动触发  

---

## 🛠️ 环境准备

- Python 3.10+ 🐍  
- 安装依赖包

```bash
pip install requests binance-futures-connector
````

---

## ⚙️ 配置说明

### 环境变量

| 名称          | 说明                    |
| ----------- | --------------------- |
| API\_KEY    | Binance API Key 🔑    |
| API\_SECRET | Binance API Secret 🔐 |
| SENDKEY     | Server酱推送 SendKey 📲  |

可设置于系统环境变量或 GitHub Secrets。

---

## ▶️ 使用方法

1. 克隆代码并进入目录：

```bash
git clone https://github.com/4evergr8/FuturesTrader.git
cd FuturesTrader
```

2. 运行脚本：

```bash
python main.py
```

---

## 🤖 GitHub Actions 自动执行示例

在仓库根目录创建 `.github/workflows/main.yml`：

```yaml
name: main

on:
  workflow_dispatch:
  schedule:
    - cron: '*/10 * * * *'  # 每10分钟执行一次

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 🐍
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies 📦
        run: pip install requests binance-futures-connector

      - name: Run Python script ▶️
        env:
          API_SECRET: ${{ secrets.API_SECRET }}
          API_KEY: ${{ secrets.API_KEY }}
          SENDKEY: ${{ secrets.SENDKEY }}
        run: python main.py
```

---

## 🧩 脚本核心逻辑

* 通过 `binance-futures-connector` 获取仓位和挂单数据
* 计算未实现盈亏比例，达到阈值时发送微信告警 🔔
* 自动创建止损追踪单，帮助控制风险 🎯
* 友好日志格式便于调试和监控 🖥️

---

## 🙋 贡献

欢迎提交 Issues 或 Pull Requests，一起完善功能，增加更多告警渠道（如邮件、Telegram）！

---

## ⚠️ 免责声明

此脚本仅供学习和辅助交易使用，风险自负。请先在模拟环境充分测试，避免实盘损失。

---

如果需要，我可以帮你写更详细的使用示例和部署说明！🚀



