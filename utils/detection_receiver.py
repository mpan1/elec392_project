"""
UDP receiver for Coral detections.
"""

import json
import socket
import time

class DetectionReceiver:
    def __init__(self, port=5005, timeout=0.01, stale_after=0.5):
        """
        timeout: socket timeout for individual recv() call (seconds) - use small value for non-blocking behavior
        stale_after: how old data can be before considered invalid
        """
        self.addr = ("127.0.0.1", port)
        self.timeout = timeout  # Very small timeout for non-blocking behavior
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
        """Attempt to receive new data. Drains all currently available packets without blocking."""
        received_any = False
        packets_drained = 0
        
        # Try to read packets without blocking - use tiny timeout
        while True:
            try:
                data, _ = self.sock.recvfrom(65535)
                self.latest = json.loads(data.decode("utf-8"))
                received_any = True
                packets_drained += 1
                self.packet_count += 1
            except socket.timeout:
                # No more packets available right now - that's ok
                break
            except json.JSONDecodeError:
                # Corrupted packet, skip it
                continue
        
        # Debug: print packet reception rate every 5 seconds
        if time.time() - self.last_debug_time >= 5.0:
            print(f"[DEBUG] Received {self.packet_count} packets total, drained {packets_drained} this update")
            self.last_debug_time = time.time()
            
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