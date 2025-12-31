# Breakout Game 打磚塊遊戲

使用 Python Turtle 製作的經典 80 年代 Breakout 打磚塊遊戲。

![遊戲截圖](https://github.com/appfromapexxx/Breakout-Game-Python-Turtle/blob/master/1.png)

## 功能特色

- 🎮 經典 Breakout 遊戲玩法
- 🧱 50 個彩色磚塊（5 排 × 10 個）
- ❤️ 3 條生命
- 🏆 計分系統
- 🎯 勝利與失敗判定

## 安裝與執行

### 使用 uv（推薦）

```bash
# 安裝 uv（如果尚未安裝）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 執行遊戲
uv run python main.py
```

### 使用 Python

```bash
python main.py
```

## 操作說明

| 按鍵     | 動作           |
|----------|----------------|
| ← / A    | 向左移動擋板   |
| → / D    | 向右移動擋板   |
| R        | 重新開始遊戲   |

## 遊戲規則

1. 使用擋板反彈球，擊破所有磚塊
2. 每擊破一個磚塊得 10 分
3. 球落地會失去一條生命
4. 生命歸零則遊戲結束
5. 消除所有磚塊即獲勝

## 系統需求

- Python 3.10 或以上版本
