import unittest
from chronosmatch.book import LimitOrderBook, Order

class LimitOrderBookTests(unittest.TestCase):
    def setUp(self): self.book = LimitOrderBook()

    def test_non_crossing_orders_rest_on_book(self):
        self.assertEqual(self.book.process(Order(1, 0, 100, 5, 1)), 0)
        self.assertEqual(self.book.process(Order(2, 1, 110, 4, 2)), 0)
        snap = self.book.snapshot()
        self.assertEqual(snap["best_bid"], 100)
        self.assertEqual(snap["best_ask"], 110)

    def test_buy_matches_ask_at_ask_price(self):
        self.book.process(Order(1, 1, 100, 5, 1))
        self.assertEqual(self.book.process(Order(2, 0, 105, 3, 2)), 3)
        self.assertEqual(self.book.snapshot()["last_trade_price"], 100)
        self.assertEqual(self.book.snapshot()["trade_quantity"], 3)

    def test_sell_matches_bid_at_bid_price(self):
        self.book.process(Order(1, 0, 100, 5, 1))
        self.assertEqual(self.book.process(Order(2, 1, 95, 2, 2)), 2)
        self.assertEqual(self.book.snapshot()["last_trade_price"], 100)

    def test_partial_fill_leaves_remainder(self):
        self.book.process(Order(1, 1, 100, 2, 1))
        self.assertEqual(self.book.process(Order(2, 0, 100, 5, 2)), 2)
        self.assertEqual(self.book.snapshot()["best_bid"], 100)

    def test_invalid_side_rejected(self):
        with self.assertRaises(ValueError): self.book.process(Order(1, 3, 100, 1, 1))

    def test_invalid_price_rejected(self):
        with self.assertRaises(ValueError): self.book.process(Order(1, 0, 0, 1, 1))

if __name__ == "__main__": unittest.main()
