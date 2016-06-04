import os
import string

path = 'E:\\dataset\\polar_movie_new\\all_lda_3'
path1 = 'E:\\dataset\\polar_movie_new\\all_lda_3_addzero'

filelist = os.listdir(path)

files_num = 0

for file in filelist:
    count = 1
    abs_file = os.path.join(path,file)

    files_num += 1
    files_name = str(files_num)+'.txt'

    abs_file_new = os.path.join(path1,files_name)

    fin = open(abs_file_new,'a+')
    with open(abs_file,'r') as file:
        for line in file:
            if count == 1:
                line = line.strip('\n') + '  0.0'*30 + '\n'             
                fin.write(line)
            else:
                fin.write(line)
            count += 1
    fin.close()

            
