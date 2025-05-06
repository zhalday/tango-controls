(communication-protocols)=

# Communication paradigms

Tango offers three communication paradigms: 
- synchronous
- asynchronous
- publish-subscribe calls

In the synchronous and asynchronous paradigms
the call is initiated by the client who contacts the server.
The server handles the client's request and sends
the answer to the client or throws an exception, which the client
catches. This paradigm involves two network calls to receive a single answer and
requires the client to be active in initiating the request. 

The calls initiated by the client may be done via 2 mechanisms:

1. The **synchronous** mechanism where the client waits (and is blocked) for the server to send the answer or until the timeout is reached
2. The **asynchronous** mechanism where the client sends the request and immediately returns.
   In this method it is not blocked and is free to do perform other tasks 
   such as updating a graphical user interface. The client has
   the choice to retrieve the server answer by checking if the reply has
   arrived. This is done via a specific API call or by requesting that a
   callback method is executed when the client receives the server's
   answer.

If the client needs to know a value every time it changes
or at regular intervals then it must poll
the server for an update every time. This is not very efficient in
terms of network bandwidth nor in terms of client programming.
For this the publish-subscribe events communication is more efficient:

3. The **publish-subscribe** communication paradigm is a more efficient
   and natural way of programming. In this paradigm the client registers
   its interest in an event once. An event can be a change in value,
   a regular update at a fixed frequency or an archive event.
   After that the server informs the client every time an event has occurred.
   This paradigm avoids the client needing to poll and so leaves it free to do doing other things.
   It is also fast and makes efficient use of the network.