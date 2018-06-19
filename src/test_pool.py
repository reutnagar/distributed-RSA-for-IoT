import master, math , random

k = master.get_k()
print 'from test: k = ' + str(k)

P = master.get_P()
print 'from test: P = ' + str(P)

key_pool = []
key_pool = master.generate_key_pool()
#print 'from test: the key pool is:' + str(key_pool)

#print master.calculateC(0.7)
print ('pc: ',master.a())
print ('pp: ',master.get_pp())

num = master.nodesInNetwork() # num of neigbors
Matrix = [[0 for x in range(k)] for y in range(num)]
for i in xrange(num):
    Matrix[i] = master.generate_sub_keys(key_pool, k).keys()
    #print 'i:' + str(i)+':'+ str(Matrix[i])

count=0	
a=0
nn = master.get_nn()

randNodes=[]
for m in xrange(nn):
	id = int(math.floor(random.random() * len(key_pool)))
	randNodes.append(id)
print randNodes
for i in xrange(nn):
	for j in range(i+1,nn):
		#print 'i:'+str(randNodes[i])+',j:'+str(randNodes[j])+str(set(Matrix[randNodes[i]]).intersection(Matrix[randNodes[j]]))
		a+=1
		if set(Matrix[i]).intersection(Matrix[j]):
			count+=1
print str(count) +'in'+ str(a)
print str(count*100.0/a)+'%'

# for i in xrange(num):
	# for j in range(i+1,num):
		# #print 'i:'+str(i)+',j:'+str(j)+str(set(Matrix[i]).intersection(Matrix[j]))
		# a+=1
		# if set(Matrix[i]).intersection(Matrix[j]):
			# count+=1
# print str(count) +'in'+ str(a)
# print str(count*100.0/a)+'%'
