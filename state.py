# -*- coding: utf-8 -*-
from typing import Dict, Set
from packet import Packet

# 今はPythonメモリ上で管理。
# 将来的にはこのファイルをSQLite/Redisに置き換える。
queued_packets: Dict[str, Packet] = {}
seen_asks: Set[str] = set()
seen_replies: Set[str] = set()
delivered_replies: Set[str] = set()

next_seq = 0
next_inject_time = 0.0
