import os
import string

path = 'E:\\dataset\\polar_movie_new\\20\\all_lda_20t'
topicSepPath = 'E:\\dataset\\polar_movie_new\\20\\all_lda_20'
topicSepPathAdd0 = 'E:\\dataset\\polar_movie_new\\20\\all_lda_20_addzero'

path2 = 'E:\\dataset\\polar_movie\\test_lda_by_topic'
path3 = 'E:\\dataset\\polar_movie\\test_lda'

def matSep(path,topicSepPath):
    filelist = os.listdir(path)
    for i in filelist:
        absfile = os.path.join(path,i) 
        count = 1
        with open(absfile,'r') as file:
            for line in file:
                matrix = str(line).strip(string.punctuation)
                # matrix = matrix.lstrip('[')
                matrix2list = matrix.split(']')
                
                for mm in matrix2list:
                    file_name = str(count)
                    fin = open(os.path.join(topicSepPath,file_name),'a+') 
                    fin.write(str(mm).lstrip(' ').replace(',',' ').replace('[','').replace('\'','').strip()) 
                    fin.write('\n')
                    count += 1
                    fin.close()

def addZero(path,pathAddZero):
    filelist = os.listdir(path)
    files_num = 0
    for file in filelist:
        count = 1
        abs_file = os.path.join(path,file)

        files_num += 1
        files_name = str(files_num)+'.txt'

        abs_file_new = os.path.join(pathAddZero,files_name)

        fin = open(abs_file_new,'a+')
        with open(abs_file,'r') as file:
            for line in file:
                if count == 1:
                    line = line.strip('\n') + '  0.0'*20 + '\n'             
                    fin.write(line)
                else:
                    fin.write(line)
                count += 1
        fin.close()
    

matSep(path,topicSepPath)
addZero(topicSepPath,topicSepPathAdd0)
