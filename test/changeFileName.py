import os
path = 'E:\\dataset\\polar_movie\\pos';
list_file = os.listdir(path)
count = 1
for files in list_file:
    old = os.path.join(path,files);
    filename = os.path.splitext(files)[0];
    filetype = os.path.splitext(files)[1];
    new = os.path.join(path,filename+str(count)+filetype);
    os.rename(old,new);
