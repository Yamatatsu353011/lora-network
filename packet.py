# -*- coding: utf-8 -*-
import random
import time
from dataclasses import dataclass
from typing import Optional
import config


@dataclass
class Packet:
    msg_type: str      # "ASK" or "REPLY"
    pkt_id: str
    target_bst: int
    data_id: str
    source_bst: int = -1   # ASKだけで使う
    responder_bst: int = -1　#REPLY


def encode(pkt: Packet) -> str:
    if pkt.msg_type == "ASK":
        return f"A,{pkt.pkt_id},{pkt.target_bst},{pkt.data_id},{pkt.source_bst}"
    return f"R,{pkt.pkt_id},{pkt.target_bst},{pkt.data_id},{pkt.responder_bst}"


def decode(line: str) -> Optional[Packet]:
    try:
        parts = [p.strip() for p in line.split(",")]
        if not parts:
            return None

        if parts[0] == "A":
            if len(parts) < 5:
                return None
            return Packet(
                msg_type="ASK",
                pkt_id=parts[1],
                target_bst=int(parts[2]),
                data_id=parts[3],
                source_bst=int(parts[4]),
            )

        if parts[0] == "R":
            if len(parts) < 4:
                return None
            return Packet(
                msg_type="REPLY",
                pkt_id=parts[1],
                target_bst=int(parts[2]),
                data_id=parts[3],
                source_bst=-1,
            )

        return None
    except Exception:
        return None


def make_ask_packet(seq: int) -> Packet:
    return Packet(
        msg_type="ASK",
        pkt_id=f"{config.NODE_ID}-{seq}",
        target_bst=config.SOURCE_ASK_TARGET_BST_ID,
        data_id=config.SOURCE_ASK_DATA_ID,
        source_bst=config.MY_BST_ID,
        responder_bst=-1,
    )


def make_reply_packet(ask_pkt: Packet) -> Packet:
    time.sleep(random.uniform(config.REPLY_DELAY_MIN_SEC, config.REPLY_DELAY_MAX_SEC))
    return Packet(
        msg_type="REPLY",
        pkt_id=ask_pkt.pkt_id,
        target_bst=ask_pkt.source_bst,
        data_id=ask_pkt.data_id,
        source_bst=-1,
        responder_bst=config.MY_BST_ID
    )
