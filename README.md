# Probability Based Keys Sharing for IOT
[![Build Status](https://travis-ci.org/reutnagar/distributed-RSA-for-IoT.svg?branch=master)](https://travis-ci.org/reutnagar/distributed-RSA-for-IoT)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Code Climate](https://codeclimate.com/github/reutnagar/distributed-RSA-for-IoT.svg)](https://codeclimate.com/github/reutnagar/distributed-RSA-for-IoT) 
[![Current Version](https://img.shields.io/github/release/reutnagar/distributed-RSA-for-IoT.svg?style=flat)](https://github.com/reutnagar/distributed-RSA-for-IoT/releases/)
 [Project Management Board](https://trello.com/b/DkjV5sEx/a)

## The Goal
To provide confidentiality of the data that is exchanged within an IoT network.
## Assumptions
The following assumptions guide us throughout the development of our solution:
#### Communication is within the Network
We are dealing with large networks on IoT devices, that the nodes inside theese networks need to communicate one with each other. This communication can be tapped, so there is need for some measure of security to protect the communication within the network. A communication with node that are outside of the network and protecting it- is out of the scope of this project.
#### Cheap Devices, Cheap Solution
The IoT devices are cheap. They dont have much resources, (and probably dont keep important secrets- which are saved in strong servers) but an attacker can find useful data when only listening to the devices communication. We want to get rid of an external device dedicated to protect the IoT network, and implement a satisfing solution managed by the IoT devices themselves. This will decrease the cost for establishing an IoT network and maintaining it.
#### Physical Presence is unusual
We assume that a physical presence will not occure, because it is impossible to steal such amount of devices that are spread all ove a city, for example- a network of camera's or small microphone all over a city. Even if one device is stolen and the data inside it can be read- we assure that the impact will be limited and not much of the network comminication is revoked.
## The solution
#### Encrypted Communication with Shared Key
The communication will be encrypted with a symetric key. The real problem is how to exchange a common secret for two nodes in the network to be their shared key. The solution introduced here suggests a way to solve this problem.
#### Sharing Keys on an IoT network
(Add the probability factor)
#### Using The keys for secured communication
#### Edge cases: New member, Node left
