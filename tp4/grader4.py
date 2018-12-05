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
  n = int(f1.readline())
  m = int(f1.readline())
  E = []
  for i in range(m):
    E.append(tuple(int(x) for x in f1.readline().split()))
  N = dict()
  G = {v : set([v]) for v in range(n)}
  for (u,v) in E:
    G[u].add(v)
    G[v].add(u)

  f2 = open(fn2, 'r')
  n2 = int(f2.readline())
  v2 = []
  for l in f2:
    l = l.strip()
    if not l:
      break
    v2.append(int(l))

  err = 0
  s2 = set(v2)

  if n2 != len(v2):
    print("Expected",n2,"vertices, but the file contains",len(s2))
    err += 1

  s1 = Counter(range(n))
  s2 = Counter(v2)

  if s2 - s1:
    print("Some output vertices were not in the input!")
    print(s2-s1)
    err += 1

  DOM = set(v2)
  undominated = []
  for v in G:
    dominatedby = [u for u in G[v] if u in DOM]
    if not dominatedby:
      undominated.append(v)

  if undominated:
    print("Some vertices are not dominated:",undominated)
    err += 1

  if not err:
    print("Your file passed! Size is",len(s2))
    
    return len(s2)
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

inputfiles = ["16", "256", "1000", "4039"]

grading = {
  "16"   : [6,6,6,6,5,5,5,5,5,5,4],
  "256"  : [50,48,46,44,42,40,38,36,34,33,32],
  "1000" : [194,193,191,188,186,184,182,180,178,177,176],
  "4039" : [344,262,255,230,195,165,135,100,75,70,68]
  }
  
grades = []
rep = open("report.txt", 'w')

for fn in inputfiles:
  rep.write(fn+"\n")
  print("\n***Testing file",fn+".in4")
  l = command + " <" + fn + ".in4 >" + fn + ".out4"
  print("Running " + l)
  system(l)
  k = testinout(fn+".in4",fn+".out4")
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
fn = "tp4_" + students[0]
if len(students)>1:
  fn += "_" + students[1]
fn += ".zip"
print("Creating submission file",fn)
system("zip " + fn + " *.java *.py report.txt")
print("\nPlease check the file and remember to submit it on time!")
