# Order-matching-engine
## Introduction 
The function of this program is to simulate trading activity and order matching processed by electronic exchanges of financial instruments. The software used for this purpose is referred to as an *order matching engine*. Buyers and sellers of some instrument come to market and place *bids* and *asks*, which are orders that represent the intent to buy or sell a certain quantity of an asset at a definite price. These orders are added to either side of the *order book*, which is essentially a list of all unmatched orders placed. The contents of the list - whether it contains bids or asks - determines its *side*. The engine matches orders according to an algorithm. After two (or more) orders are matched, they are said to have been *filled*. The engine works to continue order matching until no orders are left in the book satisfying certain parameters.

## Algorithm
The two most common algorithms used for order matching are known as price/time priority (also called *First In First Out* or *FIFO*) and pro-rata, both of which have various strengths and weaknesses. This program implements the price/time priority algorithm. One benefit of price/time priority is that it motivates market participants to narrow the *spread*, which is the difference between the best quote on either side of the book. A weakness of price/time priority is that it can be more computationally demanding than pro-rata.

## Control flow
### Overview
The control flow of the program is detailed by the flowchart shown below. At runtime, `main()` initialises many of the data structures used by the rest of the application. An order is generated and passed to one side of the order book. If the order book is not empty, `match()` is called. It selects the best quote on either side of the book and consummates a trade if each order satisfies a certain price.

<div>
  <img src="https://i.imgur.com/rELEZrD.png" width="500">
  </div>

### Order generation and sampling
Mention limit and market orders here
In order to create dummy data for the `match()` function to process, and to simulate the activity of buyers and sellers on the market, orders are generated according to certain parameters. These parameters determine all the characteristics of the order, including their quantity and type (market or limit). The price of the order is determined by taking samples from a normal distribution. This is a relatively trivial process thanks to the `random.normalvariate()` method.

### Update book
Once an order has been generated, it is added to one side of the book. It’s side is dependent on whether it is a buy or sell order, and its position in the book is determined by its price and type.

### Match
The `match()` function evaluates two best quotes, one from either side of the book, and evaluates them to determine if they satisfy each other’s price parameters. If a trade can be consummated, a *tx* (transaction) is created, and the appropriate quantity or order is removed from the book. The transaction is passed to the fill book, which is a record of all filled orders.

### Update cache
Each list used by the program (`buy_book`, `sell_book`, and `fill_book`) is associated with a *cache*. The buy and sell caches are populated by aggregating all orders at a given price and representing them with a single record. The fill cache represents a short list of the most recently filled orders. These caches are passed to the `draw_book` method.

### Update GUI
The contents of the caches listed above are inserted into a `Treeview`, which is a structure used by the `Tkinter` GUI module for displaying tabular data. The image below shows the output. It contains three tables which display the bids, offers and filled orders.

<div>
  <img src="https://i.imgur.com/N3SEd82.png" width="650">
  </div>

## Challenges
### Concurrency and multiprocessing
The original architecture of this program used a model based on concurrency through multiprocessing pools. Due to various bugs in this version, the decision was made to opt for a single-threaded model without multiprocessing. Below is a flowchart that illustrates the control flow of the original program.

<div>
  <img src="https://i.imgur.com/8LWFVen.png" width="650">
  </div>

## Future developments
This section details parts of the program that could be improved in a subsequent release and features that could be added.

### Depth chart
According to [this](https://intercom.help/sfox-trading/en/articles/3864391-how-does-a-depth-chart-work):
> Depth refers to the ability of a market for a specific asset to sustain large orders of that asset without the asset’s price moving significantly.

A depth chart is a graphical representation of the quantity of buy and sell orders at certain prices. A depth chart could be derived from the order book and represented in the GUI on another pane.

### Order generation chart
Another chart could display the process of order price determination. This would be represented by a graph with an outline of a normal distribution and an arrow or line representing the sampling of the distribution each time an order was generated.

### Price action simulation
One improvement of the current program would be a more advanced order generation process, which more accurately simulated real life price action. One way of doing this is to periodically shift the mean around which the distribution is centered. Another way is to forcibly create a disequilibrium between the volume of orders above the market price and those below. This would lead to ‘pressure’ from one side of the market or the order, replicating bullish or bearish price action. These improvements are somewhat subordinate, as the function of the program is not to accurately represent market price action, but to match orders and remove them from the book.
