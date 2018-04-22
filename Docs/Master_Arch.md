# Master Architecture

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
