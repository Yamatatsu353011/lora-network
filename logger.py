# -*- coding: utf-8 -*-
import csv
from typing import Optional

import config
from packet import Packet
from time_utils import wall_ms

log_file = None
log_writer: Optional[csv.writer] = None


def init_logger() -> None:
    global log_file, log_writer
    log_file = open(f"log_node{config.NODE_ID}.csv", "w", newline="", encoding="utf-8")
    log_writer = csv.writer(log_file)
    log_writer.writerow(["recv_time_ms", "msg_type", "pkt_id", "data_id"])


def log_reply(pkt: Packet) -> None:
    if log_writer is None:
        return
    log_writer.writerow([wall_ms(), pkt.msg_type, pkt.pkt_id, pkt.data_id])
    log_file.flush()
