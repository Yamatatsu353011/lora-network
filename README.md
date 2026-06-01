# lora-network
Distributed UAS Traffic Management using LoRa communication

# lora_ws_split


## 実行

```bash
python main.py
```

## 各ファイルの役割

- `config.py`: ノードID、BST-ID、COMポート、LoRa設定など
- `packet.py`: ASK/REPLYパケットの生成・エンコード・デコード
- `radio.py`: ES920LRの初期化、送信、受信
- `node.py`: ASK/REPLYを受け取った後のノード処理
- `routing.py`: 重複除去、中継判断。今後TTLやhop数を入れる場所
- `state.py`: 現在はPythonメモリ上の状態管理。将来SQLite/Redisに置き換える候補
- `logger.py`: CSVログ出力
- `time_utils.py`: 時刻同期、スロット判定

## ノードごとの変更場所

基本的には `config.py` のここだけ変更します。

```python
NODE_ID = 0
MY_BST_ID = 100
IS_SOURCE = True
MY_DATA_IDS = set()
OWN_ID_HEX = "0001"
SERIAL_PORT = "COM3"
```

例：ターゲットノード300が `a` を持つ場合

```python
NODE_ID = 2
MY_BST_ID = 300
IS_SOURCE = False
MY_DATA_IDS = {"a"}
OWN_ID_HEX = "0002"
SERIAL_PORT = "/dev/ttyUSB0"
```
