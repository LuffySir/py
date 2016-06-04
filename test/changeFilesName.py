import os
import string

pos_path = 'E:\\dataset\\polar_movie\\pos'
neg_path = 'E:\\dataset\\polar_movie\\neg'


def file_rename(path,count):
    filelist = os.listdir(path)
    for file in filelist:
        abs_file = os.path.join(path,file)
        old_filename = os.path.splitext(file)[0]
        filetype = os.path.splitext(file)[1]
        new_file = os.path.join(path,str(count)+filetype)
        os.rename(abs_file,new_file)
        count += 1

#file_rename(pos_path,1)
file_rename(neg_path,1001)
