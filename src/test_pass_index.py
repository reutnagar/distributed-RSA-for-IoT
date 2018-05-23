import main

#list_of_indexes = state.keys()
list_of_indexes = [2,7,5,3,4,5,9,88]
ip = '10.0.0.14'
messages.send_single_msg(message.CLIENT_START_SESSION,0,list_of_indexes,ip)
print('send list of indexes')