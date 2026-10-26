"""Fixed-record mmap ring buffer for the local ChronosMatch prototype."""
from __future__ import annotations
import mmap
import os
import struct
import tempfile
from pathlib import Path
from typing import Optional

# seq:uint64, side:uint8 (0=BUY, 1=SELL), price_ticks:uint64,
# quantity:uint32, timestamp_ns:uint64
RECORD = struct.Struct("<QBQIQ")
RECORD_SIZE = RECORD.size


class MMapRingBuffer:
    """Single-process producer/consumer ring buffer backed by an mmap file.

    This implementation is intentionally simple and not lock-free or safe for
    unsynchronized multiple processes. It uses a shared cursor in Python.
    """
    def __init__(self, capacity: int = 65536, path: Optional[str] = None):
        if capacity < 2 or capacity & (capacity - 1):
            raise ValueError("capacity must be a power of two and >= 2")
        self.capacity = capacity
        self.mask = capacity - 1
        self._owned_path = path is None
        if path is None:
            fd, path = tempfile.mkstemp(prefix="chronosmatch_", suffix=".mmap")
            os.close(fd)
        self.path = str(Path(path))
        self._file = open(self.path, "w+b")
        self._file.truncate(capacity * RECORD_SIZE)
        self._map = mmap.mmap(self._file.fileno(), capacity * RECORD_SIZE)
        self._write_seq = 0
        self._read_seq = 0
        self.dropped = 0

    def put(self, seq: int, side: int, price_ticks: int,
            quantity: int, timestamp_ns: int) -> bool:
        if self._write_seq - self._read_seq >= self.capacity:
            self.dropped += 1
            return False
        offset = (self._write_seq & self.mask) * RECORD_SIZE
        RECORD.pack_into(self._map, offset, seq, side, price_ticks, quantity, timestamp_ns)
        self._write_seq += 1
        return True

    def get(self):
        if self._read_seq >= self._write_seq:
            return None
        offset = (self._read_seq & self.mask) * RECORD_SIZE
        record = RECORD.unpack_from(self._map, offset)
        self._read_seq += 1
        return record

    def __len__(self):
        return self._write_seq - self._read_seq

    def close(self):
        try:
            self._map.close()
        finally:
            self._file.close()
            if self._owned_path:
                try:
                    os.unlink(self.path)
                except OSError:
                    pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
