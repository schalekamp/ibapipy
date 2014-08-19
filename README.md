ibapipy
=======

Interactive Brokers API (IB API) native Python port

# Introduction

Python provides some excellent libraries for working with financial data.
[NumPy](http://www.numpy.org), [SciPy](http://www.scipy.org),
[matplotlib](http://matplotlib.org), and
[scikit-learn](http://scikit-learn.org) are a few that I've found to be
invaluable.

[Interactive Brokers](https://www.interactivebrokers.com) provides fantastic
access to a wide variety of markets through their own API (IB API) or a FIX
computer-to-computer interface (CTCI).

This package is heavily based on the Java source code provided by Interactive
Brokers for their API and closely replicates its behavior with a few minor
exceptions. The end result is a pure Python package that (hopefully) provides
seamless access to the full range of IB services.

# Brief module/class overview

* *core/reader.py*. The lowest-level module in the API. In Java, an EReader
  class is used to handle the low-level socket communications. That is
  partially replaced by this module which operates off of process-safe queues.
  The message\_listener() method works as a dispatcher that receives
  information via a socket queue and translates the raw socket data into
  a method name and parameters which are placed in an output queue.
* *core/network\_handler.py*. Handles communicating with the broker over a
  socket, but leaves the interpretation of the socket messages to the reader
  module. This class makes use of processes to get around the concurrency
  limitations of threads with Python's GIL. For communication, queues are used
  to pass messages between the different processes. There are three processes:
 * Outgoing request listener. Handles client --> broker communication.
 * Incoming data listener. Handles broker --> client communication.
 * Incoming message handler. Deserializes the socket data stream for incoming
   communications.
* *core/client\_socket.py*. Python implementation of the API presented by the
  EClientSocket class in Java. This is the user-facing class that is used as
  "the API".
* *data/...*. Data objects such as ticks, orders, etc.

# Changes from the native IB API

* Contract and ContractDetails are merged into a single Contract class.
* Order and OrderState are merged into a single Order class.
* Tick class adds midpoint() and spread() methods.
* Execution class adds a milliseconds attribute.

# To do

Due to the size of the API and the fact that I'm not trading everything that it
offers, I've only implemented enough to support common operations that would be
necessary in the equity and foreign exchange markets. There's still a fair
amount left to do.

* Improve inline documentation.
* Add unit tests.
* Implement the following methods in the ClientSocket class:
 * cancel\_calculate\_implied\_volatility()
 * calculate\_option\_price()
 * calculate\_implied\_volatility()
 * cancel\_calculate\_option\_price()
 * cancel\_fundamental\_data()
 * cancel\_mkt\_depth()
 * cancel\_news\_bulletins()
 * cancel\_real\_time\_bars()
 * cancel\_scanner\_subscription()
 * exercise\_options()
 * replace\_fa()
 * req\_fundamental\_data()
 * req\_market\_data\_type()
 * req\_mkt\_depth()
 * req\_news\_bulletins()
 * req\_real\_time\_bars()
 * req\_scanner\_parameters()
 * req\_scanner\_subscription()
 * request\_fa()
* Add support to ClientSocket.place\_order() for bag\_type, under\_comp, and
  algo\_strategy.
* Add support to ClientSocket.req\_historical\_data() for bag\_type.
* Add support to ClientSocket.req\_market\_data() for bag\_type and under\_type.

# See also

* [Java API Guide](http://www.interactivebrokers.com/en/software/api/apiguide/java/java.htm)
