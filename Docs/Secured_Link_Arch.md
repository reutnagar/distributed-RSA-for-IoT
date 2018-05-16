# Secured Session

## Algorithm
We will use keys of length 126 bits (16 Bytes) and algorithm AES-128.

## Starting a Secured Link
The Initial node will send a a message of type CLIENT_START_SESSION, that will include the indexes of the keys in its key ring.
The receiver node will pick an index number that is common to its own key ring and to the initial node, 
and will return a message of type CLIENT_COMMON_INDEX and wil include the common index. If such index is not found, return -1.
Both nodes must save the common index, associated with the appropriate neighbor IP,  for lated use.

## Communication on A Secured Link
When a node needs to send data to another node on the network, it will send the data encrypted by the key 
associated with their common index in a message of type CLIENT_DATA_ENC. On receive of message CLIENT_DATA_ENC, a node may decrypt the data 
by the key associated with itself and the sender's common index.
