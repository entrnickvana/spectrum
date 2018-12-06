

if __name__ == '__main__':

	file = open('a1.txt', 'w')
	for i in range(1,600):
		file.write(str(.5*(i%7 == 0 or i%12 == 0 or i%16== 0) ) + '\n')
	
	file.close()



