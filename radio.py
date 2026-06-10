# -*- coding: utf-8 -*-
import time
from typing import Callable, Optional
import serial

import config
from packet import Packet, encode, decode

ser: Optional[serial.Serial] = None


def _read_available_lines(prefix="[INIT-RX]", duration_sec=0.8) -> None:
    global ser
    if ser is None:
        return

    t_end = time.time() + duration_sec
    while time.time() < t_end:
        try:
            raw = ser.readline()
            if raw:
                print(prefix, raw.decode("utf-8", errors="ignore").strip())
        except Exception:
            break


def _send_cmd(cmd: str, wait_sec: float = 0.3) -> None:
    global ser
    if ser is None:
        raise RuntimeError("Serial port is not initialized")

    msg = cmd + "\r\n"
    print("[INIT-TX]", repr(msg))
    ser.write(msg.encode("utf-8", errors="ignore"))
    ser.flush()
    time.sleep(wait_sec)
    _read_available_lines(duration_sec=0.4)


def init_radio() -> None:
    global ser

    ser = serial.Serial(config.SERIAL_PORT, config.BAUDRATE, timeout=config.SER_TIMEOUT)
    time.sleep(2.0)

    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
    except Exception:
        pass

    _read_available_lines(prefix="[BOOT]", duration_sec=1.0)

    _send_cmd("2")
    _send_cmd(f"channel {config.CHANNEL}")
    _send_cmd(f"sf {config.SPREADING_FACTOR}")
    _send_cmd(f"panid {config.PAN_ID_HEX}")
    _send_cmd(f"ownid {config.OWN_ID_HEX}")
    _send_cmd("dstid FFFF")
    _send_cmd("ack 2")
    _send_cmd("retry 0")
    _send_cmd("transmode 1")
    _send_cmd("format 1")
    _send_cmd("start", wait_sec=0.5)
    _read_available_lines(prefix="[AFTER-START]", duration_sec=1.0)

    print("[RADIO] ready")


def radio_send(pkt: Packet) -> None:
    global ser
    if ser is None:
        raise RuntimeError("Serial port is not initialized")

    msg = encode(pkt)
    ser.write((msg + "\r\n").encode("utf-8", errors="ignore"))
    ser.flush()
    print("[TX]", msg)


def radio_recv(handle_packet: Callable[[Packet], None]) -> None:
    global ser
    if ser is None:
        raise RuntimeError("Serial port is not initialized")

    while ser.in_waiting > 0:
        raw = ser.readline()
        if not raw:
            break

        line = raw.decode("utf-8", errors="ignore").strip()
        if not line:
            continue

        upper_line = line.upper()
        if upper_line == "OK" or upper_line.startswith("NG"):
            print("[MODEM]", line)
            continue

        print("[RX-LINE]", line)

        pkt = decode(line)
        if pkt is None:
            print("[DECODE_FAIL]", line)
            continue

        handle_packet(pkt)
