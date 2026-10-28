"""Simple price-time-priority limit order book."""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
import heapq


@dataclass
class Order:
    order_id: int
    side: int  # 0=BUY, 1=SELL
    price: double  # integer ticks, not floating point
    quantity: int
    timestamp_ns: int


class LimitOrderBook:
    """Matches crossing orders and rests any unfilled quantity on the book."""
    def __init__(self):
        self.bids = defaultdict(deque)  # price -> FIFO orders
        self.asks = defaultdict(deque)
        self._bid_prices = []  # negative prices make heapq act as max heap
        self._ask_prices = []
        self.trades = 0
        self.trade_quantity = 0
        self.last_trade_price = None

    def _best_bid(self):
        while self._bid_prices and not self.bids[-self._bid_prices[0]]:
            heapq.heappop(self._bid_prices)
        return -self._bid_prices[0] if self._bid_prices else None

    def _best_ask(self):
        while self._ask_prices and not self.asks[self._ask_prices[0]]:
            heapq.heappop(self._ask_prices)
        return self._ask_prices[0] if self._ask_prices else None

    def process(self, order: Order) -> int:
        """Process an order; return the number of units filled."""
        remaining = order.quantity
        fills = 0

        if order.side == 0:  # incoming buy crosses lowest asks
            while remaining and self._best_ask() is not None:
                ask_price = self._best_ask()
                if ask_price > order.price:
                    break
                resting = self.asks[ask_price][0]
                qty = min(remaining, resting.quantity)
                remaining -= qty
                resting.quantity -= qty
                fills += qty
                self.trades += 1
                self.trade_quantity += qty
                self.last_trade_price = ask_price
                if resting.quantity == 0:
                    self.asks[ask_price].popleft()
            if remaining:
                if not self.bids[order.price]:
                    heapq.heappush(self._bid_prices, -order.price)
                self.bids[order.price].append(Order(
                    order.order_id, order.side, order.price, remaining, order.timestamp_ns
                ))
        else:  # incoming sell crosses highest bids
            while remaining and self._best_bid() is not None:
                bid_price = self._best_bid()
                if bid_price < order.price:
                    break
                resting = self.bids[bid_price][0]
                qty = min(remaining, resting.quantity)
                remaining -= qty
                resting.quantity -= qty
                fills += qty
                self.trades += 1
                self.trade_quantity += qty
                self.last_trade_price = bid_price
                if resting.quantity == 0:
                    self.bids[bid_price].popleft()
            if remaining:
                if not self.asks[order.price]:
                    heapq.heappush(self._ask_prices, order.price)
                self.asks[order.price].append(Order(
                    order.order_id, order.side, order.price, remaining, order.timestamp_ns
                ))
        return fills

    def snapshot(self):
        best_bid = self._best_bid()
        best_ask = self._best_ask()
        return {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": (best_ask - best_bid) if best_bid is not None and best_ask is not None else None,
            "trades": self.trades,
            "trade_quantity": self.trade_quantity,
            "last_trade_price": self.last_trade_price,
            "bid_levels": sum(bool(q) for q in self.bids.values()),
            "ask_levels": sum(bool(q) for q in self.asks.values()),
        }
