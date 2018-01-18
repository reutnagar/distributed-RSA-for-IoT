# Main Program Flow Architecture

The IoT device will be considered first as a Client.
An instance of this class will be created and run, and should never return.
I case of return- the return value will be True- if this device is the master on the network,
and False- in case of error. in this case there will be another try to create a Client instance and run it again, untill success.
Some data will be visible to main, so it can be used later.

If the device is the master then an instance of the Master classs will be instantiated.
There will be an attempt to run it. What will happen in case of an error has not beed decided yet.

For convenience reasons, we decided to avoid 'Busy Loops' across all program, to enable the KeyboardInterrupt and exit the script in a clean way from console.
Therefore, we will use threading model upon any blocking action in the flow, by now we have identified listening to the network as such action.
