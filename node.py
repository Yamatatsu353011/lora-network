# -*- coding: utf-8 -*-
import random
import time

import config
import logger
import routing
import state
from packet import Packet, make_ask_packet, make_reply_packet
from radio import radio_send
from time_utils import mono_s, in_send_window


def schedule_next_injection() -> None:
    state.next_inject_time = mono_s() + random.uniform(
        config.SOURCE_INTERVAL_MIN_SEC,
        config.SOURCE_INTERVAL_MAX_SEC,
    )


def inject_source_ask() -> None:
    if not config.IS_SOURCE:
        return
    if mono_s() < state.next_inject_time:
        return

    state.next_seq += 1
    pkt = make_ask_packet(state.next_seq)
    key = f"A-{pkt.pkt_id}"
    state.queued_packets[key] = pkt

    print(f"[SRC-ASK] pkt={pkt.pkt_id} data_id={pkt.data_id} target_bst={pkt.target_bst}")
    schedule_next_injection()


def handle_ask(pkt: Packet) -> None:
    if not routing.is_new_ask(pkt):
        return

    print(f"[RX-ASK] pkt={pkt.pkt_id} data_id={pkt.data_id}")

    # data保持ノードだけREPLY生成
    if pkt.data_id in config.MY_DATA_IDS:
        rep = make_reply_packet(pkt)
        state.queued_packets[f"R-{rep.pkt_id}"] = rep
        print(f"[REPLY-GEN] ask={pkt.pkt_id}")

    # ASK自体も中継
    if routing.should_forward(pkt):
        state.queued_packets[f"A-{pkt.pkt_id}"] = pkt


def handle_reply(pkt: Packet) -> None:
    print(f"[RX-REPLY] pkt={pkt.pkt_id} data_id={pkt.data_id}")

    # 自分がsourceなら到着
    if config.MY_BST_ID == pkt.target_bst:
        if pkt.pkt_id not in delivered_replies:
            delivered_replies.add(pkt.pkt_id)
            print(f"[REPLY-ARRIVED] pkt={pkt.pkt_id}")
        return

    # sourceでないノードはREPLYを中継する
    if should_forward(pkt):
        queued_packets[f"R-{pkt.pkt_id}"] = pkt
        print(f"[REPLY-FORWARD-QUEUE] pkt={pkt.pkt_id}")



def handle_rx(pkt: Packet) -> None:
    if pkt.msg_type == "ASK":
        handle_ask(pkt)
    elif pkt.msg_type == "REPLY":
        handle_reply(pkt)


def transmit() -> None:
    if not in_send_window():
        return

    for key, pkt in list(state.queued_packets.items()):
        if pkt.msg_type == "REPLY":
            p = config.P_TX_REPLY
        elif pkt.msg_type == "ASK" and config.IS_SOURCE:
            p = config.P_TX_SOURCE
        else:
            p = config.P_TX_RELAY

        if random.random() > p:
            continue

        jitter_ms = random.randint(0, 300)
        time.sleep(jitter_ms / 1000.0)

        if not in_send_window():
            continue

        radio_send(pkt)
        del state.queued_packets[key]
        break
