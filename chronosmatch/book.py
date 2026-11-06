"""Simple price-time-priority limit order book."""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
import heapq

@dataclass
class Order:
    order_id: int
    side: int  # 0=BUY, 1=SELL
    price: int  # integer ticks
    quantity: int
    timestamp_ns: int

class LimitOrderBook:
    """Match crossing orders and rest any unfilled quantity on the book."""
    def __init__(self):
        self.bids = defaultdict(deque)
        self.asks = defaultdict(deque)
        self._bid_prices = []
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
        if order.side not in (0, 1):
            raise ValueError("side must be 0 (BUY) or 1 (SELL)")
        if order.price <= 0 or order.quantity <= 0:
            raise ValueError("price and quantity must be positive")
        remaining, filled = order.quantity, 0
        if order.side == 0:
            while remaining and self._best_ask() is not None:
                price = self._best_ask()
                if price > order.price: break
                resting = self.asks[price][0]
                qty = min(remaining, resting.quantity)
                remaining -= qty; resting.quantity -= qty; filled += qty
                self.trades += 1; self.trade_quantity += qty; self.last_trade_price = price
                if resting.quantity == 0: self.asks[price].popleft()
            if remaining:
                if not self.bids[order.price]: heapq.heappush(self._bid_prices, -order.price)
                self.bids[order.price].append(Order(order.order_id, order.side, order.price, remaining, order.timestamp_ns))
        else:
            while remaining and self._best_bid() is not None:
                price = self._best_bid()
                if price < order.price: break
                resting = self.bids[price][0]
                qty = min(remaining, resting.quantity)
                remaining -= qty; resting.quantity -= qty; filled += qty
                self.trades += 1; self.trade_quantity += qty; self.last_trade_price = price
                if resting.quantity == 0: self.bids[price].popleft()
            if remaining:
                if not self.asks[order.price]: heapq.heappush(self._ask_prices, order.price)
                self.asks[order.price].append(Order(order.order_id, order.side, order.price, remaining, order.timestamp_ns))
        return filled

    def snapshot(self):
        bid, ask = self._best_bid(), self._best_ask()
        return {"best_bid": bid, "best_ask": ask,
                "spread": ask - bid if bid is not None and ask is not None else None,
                "trades": self.trades, "trade_quantity": self.trade_quantity,
                "last_trade_price": self.last_trade_price,
                "bid_levels": sum(bool(q) for q in self.bids.values()),
                "ask_levels": sum(bool(q) for q in self.asks.values())}
