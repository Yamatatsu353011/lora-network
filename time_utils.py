# -*- coding: utf-8 -*-
import subprocess
import time
import config


def wall_ms() -> int:
    return int(time.time() * 1000)


def mono_s() -> float:
    return time.monotonic()


def wait_for_ntp_sync() -> None:
    print("[TIME] waiting for time synchronization...")

    try:
        subprocess.run(
            ["chronyc", "waitsync", "60", "0.01"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[TIME] chrony waitsync OK")
        return
    except Exception:
        pass

    try:
        for _ in range(20):
            p = subprocess.run(["timedatectl"], capture_output=True, text=True)
            if "System clock synchronized: yes" in p.stdout:
                print("[TIME] timedatectl synchronized")
                return
            time.sleep(1.0)
    except Exception:
        pass

    print(f"[TIME] fallback sleep {config.NTP_STABILIZE_SEC}s")
    time.sleep(config.NTP_STABILIZE_SEC)


def wait_until_next_slot() -> None:
    # 最初の動作確認ではスキップでOK
    print("[TIME] skip slot alignment for now")
    return


def in_send_window() -> bool:
    phase = wall_ms() % config.SLOT_MS
    return config.GUARD_MS < phase < (config.SLOT_MS - config.GUARD_MS)
