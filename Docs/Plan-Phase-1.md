# Plan Phase One

## Assumptions& Arch Decisions
- Each device has pre knowledge of the master required strengh.
- The first device (e.g. arduino) to declare itself master- wins.
- The IP's of network members list is with the master.
- Node is reset when entering a new network.


## Initialization
On init, the device will verify its capability of being a 'Master'. if not- will be continuoasly listening for a message from a master on the network.
Otherwise: on startup,  the device will be listening on the network for a second, then broadcasting a massege, and listening again in a loop. The message sent will have an 'I am the master' decleration.
Once accepted a message like this, the device will recognize the sender as master and stop listening to broadcasts.

## First Communication with Master
Protocol as follows:
- Master to Node: "I am Master"
- Node to master: "OK"
- Master store Nodes IP in list

## Pseudo Code:

_Welcome to the distributed-RSA-for-IoT wiki!_

_Init():_
  
  _self_strengh = calc_strengh();_
  
  _IAmMaster = FALSE_
  
  _master_found = FALSE_

_run_prog():_
  
  _if(self_strengh < REQUIRED_STRENGH):_
      
      _message = listen()_
      
      _proc_message(message)_
  _else:_
    
    _while(!master_found || IAmMaster){_
      
      _message = listen(1_SECOND)_
      
      _proc_message(message)_
      
      _if(master_found):_
        
        _master_ip = message.senderIP_
        
        _node_comm_to_master()_
        
        _break;_
      
      _else if(message.content == "OK") _
        
        _IAmMaster = TRUE_
        
        _network_nodes_list.add(message.senderIP)_
        
        _master_comm_to_node()_
      
      _broadcast("I am master")_
      
      _}// end while()_
