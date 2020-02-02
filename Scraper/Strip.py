import re
import os
import sys
data = os.path.join(os.getcwd(),'data')
w=open(os.path.join(data,'all_links.txt'), 'w')
for root, subfolders, files in os.walk(os.path.join(os.getcwd(),'data','links')):
    for folder in subfolders:
        filesList = os.listdir(os.path.join(data,'links',folder))
        for file in filesList:
            f = open(os.path.join(data,'links',folder,file),'r')
            w.write(f.read())

f = open(os.path.join(os.getcwd(),'data','all_links.txt'), 'r')
linkList = f.read().split()
linkList = list(set(linkList))

numberList = []

for link in linkList:
    number = re.findall(r'\d{9}/', link)[0]
    number = number.replace('/','')
    numberList.append(number)

o = open(os.path.join(os.getcwd(),'data','old_numbers.txt'), 'r')
oldNumbers = o.read().split()
newNumbers = list(set(numberList) - set(oldNumbers))
w = open(os.path.join(os.getcwd(),'data','new_numbers.txt'), 'w')
w.write("\n".join(newNumbers))
