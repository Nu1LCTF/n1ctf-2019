#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os, math, random, signal

def w(c):
  sys.stdout.write(c)
  sys.stdout.flush()

def wl(l):
  w(l)
  return w('\n')

def ri(prompt):
  try:
    w(prompt)
    ret = int(raw_input())
  except:
    sys.exit(1)
  return ret

floor = lambda x: long(math.floor(x))
ceil = lambda x: long(math.ceil(x))
NTRIES = 10

P = 1180377880254925849184613297220733950775082607541
e = 0.05
r = 1.0
delta = P ** ((2 * r - 1) / 5 - e)
d = ceil(4 * (1 / e) / 5)

messup = lambda x: random.randint(x - floor(delta), x + floor(delta))

def main():
  signal.alarm(90)
  for _ in xrange(NTRIES):
    a = random.randint(0, P - 1)
    t = [random.randint(0, P - 1) for _ in xrange(d)]
    u = [(a * x) % P for x in t]

    A = messup(a)
    T = map(messup, t)
    S = map(messup, u)
    wl(str(A))
    wl(repr(T))
    wl(repr(S))
    
    answer = ri("Input number: ")
    if answer != a:
      wl("Wrong anwser!")
      return 1

  with open("/flag", 'rb') as f:
    w(f.readline())
  return 0

if __name__ == '__main__':
  sys.exit(main())

