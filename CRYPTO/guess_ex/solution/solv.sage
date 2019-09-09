#!/usr/bin/env sage

from sage.all import *
import socket
import ast
import telnetlib

#HOST, PORT = 'localhost', 9999
HOST, PORT = '47.245.28.107', 9998

s = socket.socket()
s.connect((HOST, PORT))
f = s.makefile('rw', 0)

def recv_until(f, delim='\n'):
  buf = ''
  while not buf.endswith(delim):
    buf += f.read(1)
  return buf

rho = 1.0
epsilon = 0.05
m = 1180377880254925849184613297220733950775082607541
delta = floor(m ** ((2 * rho - 1) / 5 - epsilon))
d = ceil(4 * (1 / epsilon) / 5)

def find_lambda(Q, A, m):
  idx = 0
  frac = continued_fraction(A / m)
  while True:
    pi = frac.numerator(idx)
    qi = frac.denominator(idx)
    qi1 = frac.denominator(idx + 1)
    if qi < Q and qi1 >= Q:
      break
    idx += 1
  return qi

def babai(A, w):
  A = A.LLL(delta=0.75)
  G = A.gram_schmidt()[0]
  t = w
  for i in reversed(range(A.nrows())):
    c = ((t * G[i]) / (G[i] * G[i])).round()
    t -= A[i] * c
  return w - t

def solve_prob(A, T, S):
  q = sqrt(m / delta)
  l = find_lambda(q, A, m)
  V = [(l * Ti) % m for Ti in T]
  U = [(l * Si) % m for Si in S]

  M = Matrix(QQ, d + 1, d + 1)
  for i in xrange(d):
    M[i, i] = m
    M[d, i] = V[i]
  M[d, d] = 1 / m

  closest = babai(M, vector(U + [0]))
  return (closest[-1] * m) % m

NTRIES = 10

for _ in xrange(NTRIES):
  A = ast.literal_eval(recv_until(f, '\n'))
  T = ast.literal_eval(recv_until(f, '\n'))
  S = ast.literal_eval(recv_until(f, '\n'))
  recv_until(f, 'Input number: ')
  alpha = solve_prob(A, T, S)
  f.write(str(alpha) + '\n')

t = telnetlib.Telnet()
t.sock = s
t.interact()

