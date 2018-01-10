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

```
Init():
  
  self_strengh = calc_strengh();
  
  IAmMaster = FALSE
  
  master_found = FALSE

run_prog():
  
  if(self_strengh < REQUIRED_STRENGH):
      
      message = listen()
      
      proc_message(message)
  else:
    
    while(!master_found || IAmMaster){
      
      message = listen(1_SECOND)
      
      proc_message(message)
      
      if(master_found):
        
        master_ip = message.senderIP
        
        node_comm_to_master()
        
        break;
      
      else if(message.content == "OK") 
        
        IAmMaster = TRUE
        
        network_nodes_list.add(message.senderIP)
        
        master_comm_to_node()
      
      broadcast("I am master")
      
      }// end while()```
