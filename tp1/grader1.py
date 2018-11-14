#!/usr/bin/python3

import sys
import math
from collections import Counter
from glob import glob
from subprocess import run
from os import system

def testinout(fn1,fn2):
  f1 = open(fn1, 'r')
  n = int(f1.readline())
  c = int(f1.readline())
  v1 = []
  for i in range(n):
    v1.append(int(f1.readline()))

  f2 = open(fn2, 'r')
  k = int(f2.readline())

  v2 = []
  b = []
  for l in f2:
    l=l.strip()
    if(l):
      b.append(int(l))
    else:
      v2.append(b)
      b = []

  if b:
    v2.append(b)
    b = []

  err = 0
    
  if len(v2) != k:
    print("Expected",k,"bins, but found",len(v2))
    print(v2)
    err += 1

  b = max(v2, key=sum)
  if sum(b)>c:
    print("Found bin","with",sum(b),"when capacity is",c)
    print(b)
    err += 1

  v3 = sum(v2,[])
  s1 = Counter(v1)
  s3 = Counter(v3)

  if s1 - s3:
    print("Some input elements disappeared!")
    print(s1-s3)
    err += 1

  if s3 - s1:
    print("Some output elements were not in the input!")
    print(s3-s1)
    err += 1

  if not err:
    print("Your file passed!")
    print("You used",k,"bins, when the lower bound is",math.ceil(sum(v1)/c))
    print("Check the file:", fn2+".html")
    
    fsvg = open(fn2+".html", "w")
    fsvg.write('<!DOCTYPE html><html><body><svg width="1000" height="'+str(20*k)+'">\n')
    fsvg.write('<rect stroke="red" stroke-width="1" width="1" x="1000" height="' + str(20*k) + '"/>\n')

    for y in range(len(v2)):
      xx = 0.0
      for x in range(len(v2[y])):
        fsvg.write('<rect fill="white" stroke="black" stroke-width="1" y="'+str(20*y)+'" x="'+str(1000*xx/c)+'" height="16" width="'+str(1000*v2[y][x]/c)+'"/>\n')
        xx += v2[y][x]

    fsvg.write("</svg></body></html>\n")
    
    return k
  
  return None
    
def compileJava():
  print("Running javac *.java")
  system("javac *.java")
  
javafiles = glob('*.java')
if javafiles:
  print("Found the following java files: ",javafiles)
  
pythonfiles = glob('tp.py')
if pythonfiles:
  print("Found the tp.py file")
  
if javafiles and pythonfiles:
  print("I cannot tell if your project uses java or python. Aborting.")

if not(javafiles or pythonfiles):
  print("I could not find java or python sources. Aborting.")

if javafiles:
  compileJava()
  command = "java Tp"
else:
  command = "python3 tp.py"

inputfiles = ["20", "100", "1000", "10000"]
grading = {
  "20"    : [[6,10],[5,14],[4,20]],
  "100"   : [[33,10],[32,12],[31,14],[30,20]],
  "1000"  : [[140,10],[130,12],[127,14],[126,16],[125,18],[124,20]],
  "10000" : [[1100,10],[1019,12],[1018,14],[1015,16],[1010,18],[1000,20]]
  }
  
grades = []
rep = open("report.txt", 'w')

for fn in inputfiles:
  rep.write(fn+"\n")
  print("\n***Testing file",fn+".in1")
  l = command + " <" + fn + ".in1 >" + fn + ".out1"
  print("Running " + l)
  system(l)
  k = testinout(fn+".in1",fn+".out1")
  rep.write(str(k)+"\n")
  if k == None:
    print("Your grade cannot be calculated automatically. Try to fix your code.")
  else:
    for a,b in reversed(grading[fn]):
      if k <= a:
        print("Your grade for this file is",b)
        grades.append(b)
        break

print("\nYour average is",sum(grades)/4)
print("Your actual grade will depend on how your code performs when ran on the grading computer")


st = input("\nEnter your email @etu.udamail.fr: ")
students = [st]
st = input("Enter the email of the other student, if any:")
if len(st)>1:
  students.append(st)
students = [st.split('@')[0] for st in students]
print("The group is",students)
for st in students:
  rep.write(st+"\n")
rep.close()

students = [st[0] + st.split('.')[1] for st in students]
fn = "tp1_" + students[0]
if len(students)>1:
  fn += "_" + students[1]
fn += ".zip"
print("Creating submission file",fn)
system("zip " + fn + " *.java *.py report.txt")
print("\nPlease check the file and remember to submit it on time!")
