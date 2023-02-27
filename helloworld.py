#print("Hello world hahaha")

#import glob
#print(glob.glob("*.py"))

import os
print (os.getcwd())

folder = "sample_dir"

if os.path.exists(folder):
    print("existed folder")
else:
    os.makedirs(folder)
    print(folder, "생성하였습니다") 