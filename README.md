# Probability Based Keys Sharing for IOT
[![Build Status](https://travis-ci.org/reutnagar/distributed-RSA-for-IoT.svg?branch=master)](https://travis-ci.org/reutnagar/distributed-RSA-for-IoT)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Code Climate](https://codeclimate.com/github/reutnagar/distributed-RSA-for-IoT.svg)](https://codeclimate.com/github/reutnagar/distributed-RSA-for-IoT) 
[![Current Version](https://img.shields.io/github/release/reutnagar/distributed-RSA-for-IoT.svg?style=flat)](https://github.com/reutnagar/distributed-RSA-for-IoT/releases/)
 [Project Management Board](https://trello.com/b/DkjV5sEx/a)

# Abstract

Over the past few years, IoT has been gaining momentum. These devices become the target of attacks. Because their resources are poor, existing security solutions cannot be implemented on them and therefore lack adequate security.
This project deals with finding a security solution for small IoT networks. The solution is also possible in large networks implemented hierarchies.
We present a new security protocol consisting of five steps:

 - Finding a Master
 - Finding its size and creation of the key pool
 - Distribution of keys
 - Finding a common key
 - Secure network

For the second step of the protocol we relied on a mathematical paper that measured the size of the key pool to be created in order to overlap at least one key between two nodes in the network with high probability. This is in order for the network to be dynamic, and changes to the network topology will not undermine its security.
We implemented the solution on three "Raspberry Pi 3" IoT devices, one of which is the master and the other two are two nodes on the network.
