# Plan Phase One

## Overview
- The first device (e.g. arduino) to declare itself master- wins.
- Each device has pre knowledge of the master required strengh.
- The IP's of network members list is with the master.

## Initialization
On init, the device will verify its capability of being a 'Master'. if not- will be continuoasly listening for a message from a master on the network.
Otherwise: on startup,  the device will be listening on the network for a second, then broadcasting a massege, and listening again in a loop. The message sent will have an 'I am the master' decleration.
Once accepted a message like this, the device will recognize the sender as master and stop listening to broadcasts.

## First Communication with Master
