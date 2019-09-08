#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, random, string, struct, hashlib, signal 

DIFFICULTY = 24

randstr = lambda x: ''.join([random.choice(string.ascii_letters) for _ in xrange(x)])

def w(c):
  sys.stdout.write(c)
  sys.stdout.flush()
  return

def wl(l):
  w(l)
  w('\n')
  return

def ri(prompt):
  try:
    w(prompt)
    res = int(raw_input())
  except:
    sys.exit(1)
  return res

def check_pow(chal, suffix):
  work = chal + struct.pack("<Q", suffix)
  bits = '{0:0256b}'.format(int(hashlib.sha256(work).hexdigest(), 16))
  if not bits.endswith(DIFFICULTY * '0'):
    return False
  return True

def PoW():
  chal = randstr(8)
  wl("Please run the pow script with: {} {}".format(chal, DIFFICULTY))
  result = ri("... and give me the result: ")
  return check_pow(chal, result)

def main():
  signal.alarm(300)
  if not PoW():
    return 1
  return 0

if __name__ == '__main__':
  sys.exit(main())
