# -*- coding: utf-8 -*-
from packet import Packet
import state


def is_new_ask(pkt: Packet) -> bool:
    if pkt.pkt_id in state.seen_asks:
        return False
    state.seen_asks.add(pkt.pkt_id)
    return True


def should_forward(pkt: Packet) -> bool:
    # 実機初期確認はまず常に通す。
    # 今後ここに TTL / hop数 / target判定 を追加する。
    return True


def is_new_delivered_reply(pkt: Packet) -> bool:
    if pkt.pkt_id in state.delivered_replies:
        return False
    state.delivered_replies.add(pkt.pkt_id)
    return True
