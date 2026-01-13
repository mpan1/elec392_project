"""
UDP receiver for Coral detections.
"""

import json
import socket
import time

class DetectionReceiver:
    def __init__(self, port=5005, timeout=0.2, stale_after=0.5):
        """
        timeout: socket timeout (seconds)
        stale_after: how old data can be before considered invalid
        """
        self.addr = ("127.0.0.1", port)
        self.timeout = timeout
        self.stale_after = stale_after

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allow address reuse
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.settimeout(self.timeout)
        # Increase receive buffer to handle burst traffic
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 262144)

        self.latest = None
        self.packet_count = 0
        self.last_debug_time = time.time()

    def update(self):
        received_any = False
        packets_drained = 0

        while True:
            try:
                data, _ = self.sock.recvfrom(65535)
            except socket.timeout:
                # Nothing waiting → we’re done for this update() call
                break
            except OSError as e:
                print(f"[DEBUG] socket error: {e}", flush=True)
                break

            try:
                self.latest = json.loads(data.decode("utf-8"))
                received_any = True
                packets_drained += 1
                self.packet_count += 1
            except json.JSONDecodeError as e:
                print(f"[DEBUG] bad JSON: {e}", flush=True)

            # Optional: safety cap so a flood can’t trap you
            if packets_drained >= 50:
                print("[DEBUG] hit drain cap (sender flooding)", flush=True)
                break

        return received_any

    def get_latest(self):
        """Return latest detections or None if stale/missing."""
        if self.latest is None:
            return None

        age = time.time() - self.latest["timestamp"]
        if age > self.stale_after:
            # Debug: print why it's stale
            print(f"[DEBUG] Data is stale: age={age:.2f}s, stale_after={self.stale_after}s, frame={self.latest.get('frame_id', '?')}")
            return None

        return self.latest