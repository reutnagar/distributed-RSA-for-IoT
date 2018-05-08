# Master Architecture

## calculatePoolSize(state):
return the size of the keys-pool.(P)

We will find P by this equation:

![P_eq](https://github.com/reutnagar/distributed-RSA-for-IoT/blob/master/Docs/p_eq.png)

when:
- p' = d/(n'-1)
- d = p*(n-1)
- p = ln(n)/n - c/n , when c is real 
- k = M/8

## calculateSubKeysSize(state):
return the size of the subset keys.(k)

k = M/8

## Generation of The Key Pool
arguments: poolSize- the size of the pool to be generated.
returns the pool of random keys
```
generateKeyPool(poolSize):
  keyPool = []  // list of keys
  for i in xrange(1,poolSize):
    key = random(KEY_SIZE)  // generate a random sequence of bits to be the key
    keyPool.append(key)  // add the key to the pool. the key index is its index on this list
  return keyPool    
```

## Distibution of the key
Send a random subset of keys to each client, encryped with their public key
```
sendKeys(state):
  for client in state.toSendKeys: # send the key to nodes that already sent their public key
    index = random(state.poolSize)
    cipher = encrypt(public, state.keyPool[i])
    messages.send(CLIENT_RING_KEYS, index, cipher)
  messages.send(CLIENT_RING_END)
```
