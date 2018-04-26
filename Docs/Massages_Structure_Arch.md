# Variable-size message architecture

The header is the size of the msg in bytes

There are two ways:

## The header size is known (binary size or ascii string wuth padding):

### In sending massages:
1. Send the header.
2. Send the blocks of the split massage.

### In recieving massage:
1. Extract the size of the message from the first block.
2. Recieve the blocks of the massage, depending on the size of the message.

more about implementation [here](https://stackoverflow.com/questions/27428936/python-size-of-message-to-send-via-socket) and some explanation [here](http://stupidpythonideas.blogspot.co.il/2013/05/sockets-are-byte-streams-not-message.html).
## The header size is not known:

### In sending massages:
1. Send the header + '|'
2. Send the blocks of the split massage.

### In recieving massage:
1. Read character by character until you find the '|' character.
2. Then you got the header, and can recieve all the blocks of the header.



