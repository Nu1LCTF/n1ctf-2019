#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, sys, tempfile, signal, hashlib, struct, string, random

UID, GID = 1001, 1001
CHAL_BIN = "cnc"
CHAL_DIR = "/challenge/plugin/"
CHAL_CONF = "/challenge/conf/untrusted.conf"
WORK_DIR = "/workdir/"
DIFFICULTY = 26

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
  # check proof of work
  signal.alarm(600)
  if not PoW():
    wl("Invalid PoW.")
    return 1
  signal.alarm(0)

  # read code
  wl("Give me your code, ended by a line with 'END_OF_SNIPPET' (quote excluded).")
  wl("I will compile it using the 'cnc' binary.")
  lines = []
  while True:
    line = raw_input()
    if line == "END_OF_SNIPPET":
      break
    lines.append(line)
  code = '\n'.join(lines)

  # put and run
  fd, ifp = tempfile.mkstemp(suffix=".hs", dir=WORK_DIR)
  with open(ifp, "wb") as f:
    f.write(code)
  os.close(fd)
  
  fd, ofp = tempfile.mkstemp(suffix=".exe", dir=WORK_DIR)
  os.close(fd)

  os.chdir(CHAL_DIR)
  code = os.system(" ".join(["stack", "exec", CHAL_BIN, "--", ifp, ofp]))
  os.unlink(ifp)

  if code == 0:
    os.chmod(ofp, 0o755)  # set permission
    os.setgroups([])
    os.setgid(GID)
    os.setuid(UID)
    os.execvp("prlimit", ["prlimit", "--as=67108864", "--cpu=30", "--", ofp])   # the binary will be removed by cron job
  else:
    os.unlink(ofp)

  return 0

if __name__ == '__main__':
  sys.exit(main())
