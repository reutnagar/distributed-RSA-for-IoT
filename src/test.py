import master

k = master.calculate_sub_keys_size()
print 'from test: k = ' + str(k)

P = master.calculate_pool_size()
print 'from test: P = ' + str(P)

key_pool = []
key_pool = master.generate_key_pool()
print 'from test: the key pool is:' + str(key_pool)

#print master.calculateC(0.7)
print master.a()
print master.calcPp()

num = master.nodesInNetwork() # num of neigbors
Matrix = [[0 for x in range(k)] for y in range(num)]
for i in xrange(num):
    Matrix[i] = master.generate_sub_keys(key_pool, k).keys()
    #print Matrix[i]

count=0	
a=0
for i in xrange(num):
	for j in range(i+1,num):
		#print 'i:'+str(i)+',j:'+str(j)+str(set(Matrix[i]).intersection(Matrix[j]))
		a+=1
		if set(Matrix[i]).intersection(Matrix[j]):
			count+=1
print str(count) +'in'+ str(a)
print count*1.0/a
