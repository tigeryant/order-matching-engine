import datetime
import random
from tkinter import *
import tkinter.ttk as ttk


class Order:
    id_counter = 1

    def __init__(self, timestamp, order_id, quantity, market, limit, price, bid, ask):
        self.timestamp = timestamp
        self.order_id = order_id
        self.quantity = quantity
        self.market = market
        self.limit = limit
        self.price = price
        self.bid = bid
        self.ask = ask

    # Defines a method for comparing quotes in the book
    def better_than(self, other):
        if self.bid == True:
            if self.price > other.price:
                return True
            else:
                return False

        elif self.ask == True:
            if self.price > other.price:
                return False
            else:
                return True

    def __repr__(self):
        return f'Bid: {self.bid} Ask: {self.ask}'


def launch_gui():
    global window
    window = Tk()
    window.title("Order Matching Engine")
    window.geometry("870x470")

    fills_frame = ttk.LabelFrame(window, text="Filled orders")
    bid_frame = ttk.LabelFrame(window, text="Bids")
    ask_frame = ttk.LabelFrame(window, text="Offers")

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)

    global bid_tree
    bid_tree = ttk.Treeview(bid_frame, columns=(
        "Price", "Quantity"), show="headings")
    bid_tree.heading("#1", text="Price")
    bid_tree.heading("#2", text="Quantity")
    bid_tree.pack(fill='both')
    bid_frame.grid(row=0, column=0, sticky="nsew")

    global ask_tree
    ask_tree = ttk.Treeview(ask_frame, columns=(
        "Price2", "Quantity2"), show="headings")
    ask_tree.heading("#1", text="Price")
    ask_tree.heading("#2", text="Quantity")
    ask_tree.pack(fill='both')
    ask_frame.grid(row=0, column=1, sticky="nsew")

    global fill_tree
    fill_tree = ttk.Treeview(fills_frame, columns=("Date", "Time", "Price ($)",
                             "Quantity", "Transaction ID", "Bid ID", "Ask ID"), show="headings")
    fill_tree.column("#1", width=120)
    fill_tree.column("#2", width=120)
    fill_tree.column("#3", width=120)
    fill_tree.column("#4", width=120)
    fill_tree.column("#5", width=120)
    fill_tree.column("#6", width=120)
    fill_tree.column("#7", width=120)
    fill_tree.heading("#1", text="Date")
    fill_tree.heading("#2", text="Time")
    fill_tree.heading("#3", text="Price ($)")
    fill_tree.heading("#4", text="Quantity")
    fill_tree.heading("#5", text="Transaction ID")
    fill_tree.heading("#6", text="Bid ID")
    fill_tree.heading("#7", text="Ask ID")
    fill_tree.pack(fill='both')
    fills_frame.grid(row=1, column=0, columnspan=2,
                     sticky="nsew", padx=5, pady=5)


def sample():
    # further development: shift the mean randomly, periodically (sample)
    ask = None
    bid = None
    global eq_price
    eq_price = 200  # further development: periodically change this
    std_dev = 25
    # further development: include a method of catching 0 or negative values
    price = round(random.normalvariate(eq_price, std_dev), 2)

    if price > eq_price:
        if price > (eq_price + (0.1 * std_dev)):
            ask = True
            bid = False

        elif price <= (eq_price + (0.1 * std_dev)):
            x = random.randint(1, 10)
            if x < 9:
                ask = True
                bid = False
            else:
                ask = False
                bid = True

    elif price <= eq_price:
        if price < (eq_price - (0.1 * std_dev)):
            bid = True
            ask = False

        elif price >= (eq_price - (0.1 * std_dev)):
            x = random.randint(1, 10)
            if x < 9:
                bid = True
                ask = False
            else:
                bid = False
                ask = True

    return price, bid, ask


def generate_order():
    timestamp = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    order_id = Order.id_counter
    Order.id_counter += 1
    quantity = random.randint(1, 100)

    random_type = random.randint(1, 10)
    if random_type < 8:
        market = True
        limit = False
        price = None
    else:
        market = False
        limit = True

    price, bid, ask = sample()

    order = Order(timestamp, order_id, quantity,
                  market, limit, price, bid, ask)
    add_to_book(order)


def draw_book(cache):  # refactoring opportunity
    if cache == buy_cache:
        tree = bid_tree
    elif cache == sell_cache:
        tree = ask_tree
    elif cache == fill_cache:
        tree = fill_tree

    if tree == bid_tree or tree == ask_tree:
        tree.delete(*tree.get_children())
        i = 0
        iid = 0

        if len(cache) == 0:
            return

        for record in cache:  # refactoring opportunity
            if record == None:
                continue

            tree.insert(parent="", index=i, iid=iid, text="",
                        values=(record.get("price"), record.get("quantity")))
            i = i + 1
            iid = iid + 1

    else:
        tree.delete(*tree.get_children())
        i = 0
        iid = 0

        for record in cache:
            tree.insert(parent="", index=i, iid=iid, text="", values=(record.get("Date"), record.get("Time"),
                        record.get("Price ($)"), record.get("Quantity"), record.get("Transaction ID"), record.get("Bid ID"), record.get("Ask ID")))
            i = i + 1
            iid = iid + 1


def update_cache(book):
    if book == fill_book:
        cache = fill_cache
    elif book == buy_book:
        cache = buy_cache
    elif book == sell_book:
        cache = sell_cache

    cache.clear()

    if cache == fill_cache:
        if len(fill_book) < cache_length:
            for x in range(len(fill_book)):
                fill_cache.append(fill_book[x])

        else:
            for x in range(cache_length):
                fill_cache.append(fill_book[x])

    elif cache == buy_cache or cache == sell_cache:
        empty_list = [None] * 10
        cache.extend(empty_list)

        if len(book) == 0:
            draw_book(cache)
            return

        index = 0
        current_price = book[0].price
        quantity = 0

        while index < 10:
            for order in book:
                if order.price == current_price:
                    quantity = quantity + order.quantity

            cache_order = {
                "quantity": quantity,
                "price": current_price
            }

            cache[index] = cache_order

            for order in book:
                if book == sell_book:
                    if order.price > current_price:
                        current_price = order.price
                        break

                elif book == buy_book:
                    if order.price < current_price:
                        current_price = order.price
                        break

            quantity = 0
            index = index + 1

    draw_book(cache)


def add_to_book(order):
    same = []
    opp = []

    if order.bid == True:
        same = buy_book
        opp = sell_book

    elif order.ask == True:
        same = sell_book
        opp = buy_book

    if order.limit == True:
        if len(same) == 0:
            same.append(order)
        else:
            insert_order(order, same)

    if order.market == True:
        if len(opp) != 0:
            order.price = opp[0].price

            if len(same) == 0:
                same.append(order)
            else:
                insert_order(order, same)

        else:
            if len(same) != 0:
                order.price = same[0].price
                insert_order(order, same)

            else:
                order.price = eq_price
                same.append(order)


def insert_order(order, book):
    if order.bid == True:
        book = buy_book
    elif order.ask == True:
        book = sell_book

    if Order.better_than(order, book[0]) == True:
        book.insert(0, order)

    elif Order.better_than(order, book[len(book) - 1]) == False:
        book.append(order)

    else:
        for entry in book:
            if Order.better_than(order, entry) == True:
                insert_point = book.index(entry) - 1
                book.insert(insert_point, order)
                break


def add_to_fills(tx):
    fill_book.insert(0, tx)
    update_cache(fill_book)


def create_tx(bid, ask, price, quantity):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    time = datetime.datetime.now().strftime("%H:%M:%S")
    global tx_count
    tx_id = tx_count
    tx_count = tx_count + 1
    bid_id = bid.order_id
    ask_id = ask.order_id

    tx = {
        "Date": date,
        "Time": time,
        "Transaction ID": tx_id,
        "Bid ID": bid_id,
        "Ask ID": ask_id,
        "Price ($)": price,
        "Quantity": quantity
    }

    add_to_fills(tx)


def remove_from_book(order):
    book = []
    if order.bid == True:
        book = buy_book
    elif order.ask == True:
        book = sell_book

    for entry in book:
        if entry.order_id == order.order_id:
            discard = entry
            break

    book.remove(discard)
    update_cache(book)


def reduce_quantity(order, quantity):
    book = []
    if order.bid == True:
        book = buy_book
    elif order.ask == True:
        book = sell_book

    for entry in book:
        if entry.order_id == order.order_id:
            entry.quantity = entry.quantity - quantity
            break

    update_cache(book)


def match():
    bid = buy_book[0]
    ask = sell_book[0]
    tx_price = ask.price
    tx_quantity = None

    if bid.quantity < ask.quantity:
        tx_quantity = bid.quantity
    else:
        tx_quantity = ask.quantity

    if bid.price < ask.price:
        pass

    elif bid.price == ask.price:
        create_tx(bid, ask, tx_price, tx_quantity)  # TODO

        if bid.quantity < ask.quantity:
            remove_from_book(bid)
            reduce_quantity(ask, bid.quantity)

        elif bid.quantity == ask.quantity:
            remove_from_book(bid)
            remove_from_book(ask)

        elif bid.quantity > ask.quantity:
            remove_from_book(ask)
            reduce_quantity(bid, ask.quantity)


def main():
    global tx_count
    global cache_length
    global buy_book
    global sell_book
    global buy_cache
    global sell_cache
    global fill_book
    global fill_cache

    tx_count = 0
    cache_length = 15
    buy_book = []
    sell_book = []
    buy_cache = []
    sell_cache = []
    fill_cache = []
    fill_book = []

    launch_gui()

    run = True

    while (run):
        generate_order()

        if len(buy_book) > 0 and len(sell_book) > 0:
            match()

        window.update_idletasks()
        window.update()


if __name__ == "__main__":
    main()
