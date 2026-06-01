#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import config
import logger
from radio import init_radio, radio_recv
from node import inject_source_ask, schedule_next_injection, handle_rx, transmit
from time_utils import wait_for_ntp_sync, wait_until_next_slot


def print_settings() -> None:
    print("===================================")
    print(f"NODE_ID       = {config.NODE_ID}")
    print(f"MY_BST_ID     = {config.MY_BST_ID}")
    print(f"IS_SOURCE     = {config.IS_SOURCE}")
    print(f"OWN_ID_HEX    = {config.OWN_ID_HEX}")
    if config.IS_SOURCE:
        print(f"ASK_TARGET    = {config.SOURCE_ASK_TARGET_BST_ID}")
        print(f"ASK_DATA_ID   = {config.SOURCE_ASK_DATA_ID}")
    print(f"MY_DATA_IDS   = {sorted(list(config.MY_DATA_IDS))}")
    print("===================================")


def main() -> None:
    print_settings()

    wait_for_ntp_sync()
    wait_until_next_slot()
    init_radio()
    logger.init_logger()

    if config.IS_SOURCE:
        schedule_next_injection()

    while True:
        inject_source_ask()
        radio_recv(handle_rx)
        transmit()
        time.sleep(config.MAIN_LOOP_SLEEP_SEC)


if __name__ == "__main__":
    main()
