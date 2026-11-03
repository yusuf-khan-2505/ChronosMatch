import unittest

from chronosmatch.ipc import MMapRingBuffer


class MMapRingBufferTests(unittest.TestCase):

    def test_put_and_get_record(self):
        with MMapRingBuffer(capacity=4) as ring:
            self.assertTrue(ring.put(1, 0, 100000, 10, 123456))
            self.assertEqual(ring.get(), (1, 0, 100000, 10, 123456))

    def test_empty_buffer_returns_none(self):
        with MMapRingBuffer(capacity=4) as ring:
            self.assertIsNone(ring.get())
            self.assertEqual(len(ring), 0)

    def test_full_buffer_rejects_new_record(self):
        with MMapRingBuffer(capacity=2) as ring:
            ring.put(1, 0, 100, 5, 1000)
            ring.put(2, 1, 101, 3, 2000)
            self.assertFalse(ring.put(3, 0, 102, 2, 3000))
            self.assertEqual(ring.dropped, 1)

    def test_buffer_reuses_space_after_read(self):
        with MMapRingBuffer(capacity=2) as ring:
            ring.put(1, 0, 100, 5, 1000)
            ring.put(2, 1, 101, 3, 2000)
            ring.get()
            self.assertTrue(ring.put(3, 0, 102, 2, 3000))
            self.assertEqual(ring.get(), (2, 1, 101, 3, 2000))
            self.assertEqual(ring.get(), (3, 0, 102, 2, 3000))

    def test_length_tracks_records(self):
        with MMapRingBuffer(capacity=4) as ring:
            self.assertEqual(len(ring), 0)
            ring.put(1, 0, 100, 5, 1000)
            ring.put(2, 1, 101, 3, 2000)
            self.assertEqual(len(ring), 2)
            ring.get()
            self.assertEqual(len(ring), 1)

    def test_invalid_capacity_is_rejected(self):
        with self.assertRaises(ValueError):
            MMapRingBuffer(capacity=3)


if __name__ == "__main__":
    unittest.main()
