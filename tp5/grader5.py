#!/usr/bin/python3

import sys
import math
from collections import Counter
from glob import glob
from subprocess import run
from os import system

def dist(p,q):
  return math.sqrt((p[0]-q[0])*(p[0]-q[0]) + (p[1]-q[1])*(p[1]-q[1]))

def testinout(fn1,fn2):
  f1 = open(fn1, 'r')
  n = int(f1.readline())
  m = int(f1.readline())
  E = []
  for i in range(m):
    E.append(tuple(int(x) for x in f1.readline().split()))
  N = dict()
  #G = {v : set([v]) for v in range(n)}
  #for (u,v) in E:
    #G[u].add(v)
    #G[v].add(u)

  f2 = open(fn2, 'r')
  n2 = int(f2.readline())
  k = int(f2.readline())
  C = []
  for l in f2:
    l = l.strip()
    if not l:
      break
    C.append(int(l))

  err = 0

  if n2 != len(C):
    print("Expected",n2,"values, but the file contains",len(C))
    err += 1

  if max(C) >= k:
    print("You say colors go from 0 to ",k-1,", but I found color",max(C))
    err += 1

  if min(C) < 0:
    print("Negative colors are not allowed! I found color",min(C))
    err += 1

  for (u,v) in E:
    if(C[u] == C[v]):
      print("Adjacent vertices",u,v,"have the same color",C[u])
      err += 1
      break

  if not err:
    print("Your file passed! Number of colors is", k)
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

inputfiles = ["10", "100", "1000", "4039"]
grading = {
  "10"    : [[5,10],[4,14],[3,20]],
  "100"   : [[11,10],[10,14],[9,16],[8,18],[7,20]],
  "1000"  : [[7,10],[6,14],[5,18],[4,20]],
  "4039"  : [[76,10],[75,12],[73,14],[72,16],[71,18],[70,20]]
  }
  
grades = []
rep = open("report.txt", 'w')

for fn in inputfiles:
  rep.write(fn+"\n")
  print("\n***Testing file",fn+".in5")
  l = command + " <" + fn + ".in5 >" + fn + ".out5"
  print("Running " + l)
  system(l)
  k = testinout(fn+".in5",fn+".out5")
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
fn = "tp5_" + students[0]
if len(students)>1:
  fn += "_" + students[1]
fn += ".zip"
print("Creating submission file",fn)
system("zip " + fn + " *.java *.py report.txt")
print("\nPlease check the file and remember to submit it on time!")
