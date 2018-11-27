#!/usr/bin/python3

import sys
import math
from collections import Counter
from glob import glob
from subprocess import run
from os import system

def dist(p,q):
  return math.sqrt((p[0]-q[0])*(p[0]-q[0]) + (p[1]-q[1])*(p[1]-q[1]))

def length(t):
  return dist(t[0],t[-1]) + sum((dist(t[i],t[i+1]) for i in range(len(t)-1)))


def testinout(fn1,fn2):
  f1 = open(fn1, 'r')
  n1 = int(f1.readline())
  v1 = []
  for i in range(n1):
    v1.append(tuple(float(x) for x in f1.readline().split()))

  f2 = open(fn2, 'r')
  n2 = int(f2.readline())
  l2 = float(f2.readline())
  v2 = []
  for l in f2:
    l = l.strip()
    if not l:
      break
    v2.append(tuple(float(x) for x in l.split()))

  err = 0

  if n1 != n2:
    print("Expected",n1,"points, but the file claims there are",n2)
    err += 1

  if n1 != len(v2):
    print("Expected",n1,"points, but the file contains",len(v2))
    err += 1

  s1 = Counter(v1)
  s2 = Counter(v2)

  if s2 - s1:
    print("Some output elements were not in the input!")
    print(s2-s1)
    err += 1

  if s1 - s2:
    print("Some input elements were not in the output!")
    print(s2-s1)
    err += 1

  l = length(v2)
  if abs(l - l2) > .001:
    print("Calculated length",l,"but the file claims",l2)
    err += 1
    
  if not err:
    print("Your file passed! The length of your tour is", l)
    
    imgsz = 1000.0
    x0 = min([p[0] for p in v1])
    y0 = min([p[1] for p in v1])
    x1 = max([p[0] for p in v1])
    y1 = max([p[1] for p in v1])
    sz = max(x1-x0, y1-y0)
    r2 = 10.0

    fsvg = open(fn2+".svg", "w")
    fsvg.write('<?xml version="1.0" encoding="utf-8"?>\n')
    fsvg.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="'+str(imgsz+2*r2)+'" height="'+str(imgsz+2*r2)+'">\n')

    for p in v2:
      q = (r2 + (p[1]-y0) * imgsz / sz, r2 + (x1-p[0]) * imgsz / sz)
      fsvg.write('<circle stroke="darkblue" stroke-width="2" cx="'+str(q[0])+'" cy="'+str(q[1])+'" r="1"/>\n')
    
    fsvg.write('<polygon stroke="black" stroke-width="1" fill="none" points="')
    for p in v2:
      q = (r2 + (p[1]-y0) * imgsz / sz, r2 + (x1-p[0]) * imgsz / sz)
      fsvg.write(str(q[0])+','+str(q[1])+' ')
    fsvg.write('"/>\n')

    fsvg.write("</svg>\n")

    print("Svg visualisation written to",fn2+".svg")
    return l
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
  "20"    : [115, 108, 105, 103, 100, 99, 97, 95, 94, 93, 92],
  "100"   : [100000, 90000, 85000, 84000, 83000, 82000, 81000, 80000, 79000, 78500, 78000],
  "1000"  : [135000, 128000, 124000, 121000, 119000, 117000, 115000, 113000, 111000, 109000, 108000],
  "10000" : [560000, 540000, 530000, 525000, 520000, 510000, 500000, 490000, 480000, 470000, 465000]
  }
  
grades = []
rep = open("report.txt", 'w')

for fn in inputfiles:
  rep.write(fn+"\n")
  print("\n***Testing file",fn+".in3")
  l = command + " <" + fn + ".in3 >" + fn + ".out3"
  print("Running " + l)
  system(l)
  k = testinout(fn+".in3",fn+".out3")
  rep.write(str(k)+"\n")
  if k == None:
    print("Your grade cannot be calculated automatically. Try to fix your code.")
  else:
    b = 20
    for a in reversed(grading[fn]):
      if k <= a:
        print("Your grade for this file is",b)
        grades.append(b)
        break
      b -= 1

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
fn = "tp2_" + students[0]
if len(students)>1:
  fn += "_" + students[1]
fn += ".zip"
print("Creating submission file",fn)
system("zip " + fn + " *.java *.py report.txt")
print("\nPlease check the file and remember to submit it on time!")
