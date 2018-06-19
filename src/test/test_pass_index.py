from .. import messages

#list_of_indexes = state.keys()
list_of_indexes1 = [2,7,5,3,4,5,9,88]
list_of_indexes2 = [1,4,7,9,33,5]
ip1 = '10.0.0.14'
ip2 = '10.0.0.6'
messages.send_single_msg(ip1,messages.CLIENT_START_SESSION,0,list_of_indexes1)
print('send list of indexes')