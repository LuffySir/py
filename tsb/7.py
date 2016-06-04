import string
path = 'E:\\dataset\\polar_movie\\test\\new 1.txt'
path1 = 'E:\\Code\R\\test\\t1.R'
path2 = 'E:\\课程\\课表11111111.docx'
path3 = 'E:\\Code\\ab.docx'

print(string.punctuation)
#print(str(string.punctuation.split())
      
with open(path,'r') as f:
     
    for line in f:
        # print(line)
        
        line.strip('\n')
        word = line.replace(str(string.punctuation.split()),' ')
        #word = line.split(' ')
        print(word)

        
    #print(text)

        

       
