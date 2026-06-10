# -*- coding: utf-8 -*-

# =========================================================
# Node settings
# ここだけ各ノードで変更
# =========================================================
NODE_ID = 0
MY_BST_ID = 100
IS_SOURCE = True

# sourceノードだけ意味あり
SOURCE_ASK_TARGET_BST_ID = 300
SOURCE_ASK_DATA_ID = "a"

# 自分が持っているデータID
MY_DATA_IDS = set()

# ES920LR ownid（各ノードでユニーク）
OWN_ID_HEX = "0001"

# UART
SERIAL_PORT = "COM3"   # Windowsなら "COM3" / Raspberry Piなら例: "/dev/ttyUSB0"
BAUDRATE = 115200
SER_TIMEOUT = 0.1

# LoRa module config
PAN_ID_HEX = "1234"
CHANNEL = 1
SPREADING_FACTOR = 8

# =========================================================
# Radio / timing parameters
# =========================================================
SLOT_MS = 2000
GUARD_MS = 300

P_TX_SOURCE = 1.0
P_TX_RELAY = 1.0
P_TX_REPLY = 1.0

SOURCE_INTERVAL_MIN_SEC = 8.0
SOURCE_INTERVAL_MAX_SEC = 12.0
MAIN_LOOP_SLEEP_SEC = 0.02

# 半二重の都合でREPLYを少し遅らせる
REPLY_DELAY_MIN_SEC = 0.25
REPLY_DELAY_MAX_SEC = 0.45

NTP_STABILIZE_SEC = 20
