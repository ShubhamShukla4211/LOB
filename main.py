import heapq
import random
import numpy as np
import matplotlib.pyplot as plt

class Order:
    def __init__(self, order_id, price, size):
        self.order_id = order_id
        self.price = price
        self.size = size
    
    def __lt__(self, other):
        return self.price < other.price  # Needed for heapq

class OrderBook:
    def __init__(self):
        self.bids = []  # max-heap for bids
        self.asks = []  # min-heap for asks
        self.order_id_counter = 0
        self.bid_orders = {}
        self.ask_orders = {}
    
    def place_limit_order(self, price, size, side):
        order = Order(self.order_id_counter, price, size)
        self.order_id_counter += 1
        if side == 'bid':
            heapq.heappush(self.bids, (-price, order))
            self.bid_orders[order.order_id] = order
        elif side == 'ask':
            heapq.heappush(self.asks, (price, order))
            self.ask_orders[order.order_id] = order
    
    def place_market_order(self, size, side):
        trades = []
        if side == 'buy':
            while size > 0 and self.asks:
                best_ask_price, best_ask_order = self.asks[0]
                trade_size = min(size, best_ask_order.size)
                trades.append((best_ask_price, trade_size))
                size -= trade_size
                best_ask_order.size -= trade_size
                if best_ask_order.size == 0:
                    heapq.heappop(self.asks)
                    del self.ask_orders[best_ask_order.order_id]
        elif side == 'sell':
            while size > 0 and self.bids:
                best_bid_price_neg, best_bid_order = self.bids[0]
                best_bid_price = -best_bid_price_neg
                trade_size = min(size, best_bid_order.size)
                trades.append((best_bid_price, trade_size))
                size -= trade_size
                best_bid_order.size -= trade_size
                if best_bid_order.size == 0:
                    heapq.heappop(self.bids)
                    del self.bid_orders[best_bid_order.order_id]
        return trades

    def best_bid(self):
        return -self.bids[0][0] if self.bids else None

    def best_ask(self):
        return self.asks[0][0] if self.asks else None

def simulate_market(steps=1000):
    ob = OrderBook()
    mid_price = 100
    price_history = []

    for step in range(steps):
        # Random agent actions
        action = random.choices(['limit', 'market', 'cancel'], weights=[0.7, 0.25, 0.05])[0]

        if action == 'limit':
            side = random.choice(['bid', 'ask'])
            price = mid_price + random.randint(-5, 5)
            size = random.randint(1, 10)
            ob.place_limit_order(price, size, side)

        elif action == 'market':
            side = random.choice(['buy', 'sell'])
            size = random.randint(1, 10)
            trades = ob.place_market_order(size, side)
            if trades:
                last_price = trades[-1][0]
                mid_price = last_price

        elif action == 'cancel':
            # Remove random order
            if ob.bid_orders and random.random() < 0.5:
                order_id = random.choice(list(ob.bid_orders.keys()))
                del ob.bid_orders[order_id]
                ob.bids = [item for item in ob.bids if item[1].order_id != order_id]
                heapq.heapify(ob.bids)
            elif ob.ask_orders:
                order_id = random.choice(list(ob.ask_orders.keys()))
                del ob.ask_orders[order_id]
                ob.asks = [item for item in ob.asks if item[1].order_id != order_id]
                heapq.heapify(ob.asks)

        # Record mid price
        bid = ob.best_bid()
        ask = ob.best_ask()
        if bid is not None and ask is not None:
            mid_price = (bid + ask) / 2
        price_history.append(mid_price)

    return price_history

# Run simulation
price_history = simulate_market(steps=1000)

# Plot
plt.plot(price_history)
plt.xlabel('Time')
plt.ylabel('Mid Price')
plt.title('Simulated Mid Price over Time')
plt.show()
