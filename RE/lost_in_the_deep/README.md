# Lost in deep writeup

## Overall
This is a challenge of Golang exe reversing.
It's easy to recover symbol from a ELF file with well known `golang_loader_assist.py` but it doesn't work on PE files.
But it's still possible to recover functions names from PE files with some tools like https://github.com/sibears/IDAGolangHelper or write one yourself.
You can also solve this challenge without recovering function names, but maybe a bit painful.

## Part 1

### main function
After recovering the function names, we are able to find `main_main` function. 
First, `argc` is checked to decide whether to run server or client, the result value of client function will be printed out.

Running the binary without params will start a server running at 30754 port, while passing an ip will connect to 30754 port of that ip.

Nothing interesting in the client function, let's head into the server function.
The `main_run_server` function reads `flag1.txt` and `flag2.txt`, passing them to `main_my_server` function when client connected. 
### dec function
In `main_my_server`, our input is passed through `main_dec` function, inside is a simple base64 decode with custom alphabet, where the alphabet is encrypted with rc4. You can dump the alphabet or decrypt with key `This is not the key`  where itself is RC4ed for 1024 times before finally get used:
`AiHheGuklOxE5wz+WS9JLZRY7FXnyV0jCQP/Kf3d4BqTr8MmUta6NbpIov2cDgs1`

After that, `check` function is called, you will get different response depending on return value:
```
0: n
1: flag1
2: flag1+flag2
```
### check function
Let's see how `check` function works:
Fisrt, we can see a while loop that handles the input string byte by byte, checking some conditions and modify two variables, which are checked after the loop.
`if v53 >= 580 and v14 <= 233` -> flag1
`if v53 >= 1050 and v14 <= 233` -> flag1 + flag2
#### check logic
More on the while loop, we can recover a struct like this:
```go
type node struct {
	a         int
	b         int
	flag      bool
	p         *node
}
```
And off_5FDAA0[] is a node array with length 100.
First, flags are cleared at the beginning of `check`:
```cpp
  for ( i = 0i64; i < v8; ++i )
    v9[i]->flag = 0;
```
Then, every byte of input string is indexed through a string `unk_529AEA`. The return value is in range(0, len(that string) = 100), which corresponds to a node in the array.
There's some checks on index number:
```cpp
    if ( idx == -1 || idx >= 100 || (!idx ? false : (idx <= lst_idx) ) )
    {
        fail;
    }
```
Which means that index should be in ascend order.
Next, if node.flag == false, the check will fail as well. Otherwise, node.a and node.b will be added up like this:
```cpp
tot_a += node.a
tot_b += node.b
tot_c.flag = true
```
Recall the constraints after the while loop:
`tot_a >= 1050 and tot_b <= 233`
Meaning this is actually a knapsack problem on a tree where a is value and b is weight.

To get the first flag, your total value just needs to reach 580, which could be done manually. You can dump those nodes and draw the tree to ease the process:
```
0 w: 6 v: 82
├── 1 w: 31 v: 46
│   ├── 5 w: 22 v: 51
│   │   ├── 15 w: 41 v: 54
│   │   │   └── 30 w: 44 v: 98
│   │   └── 16 w: 2 v: 6
│   │       ├── 31 w: 2 v: 71
│   │       │   ├── 50 w: 32 v: 79
│   │       │   └── 51 w: 50 v: 45
│   │       │       └── 70 w: 41 v: 73
│   │       │           └── 84 w: 5 v: 99
│   │       ├── 32 w: 8 v: 49
│   │       │   ├── 52 w: 21 v: 81
│   │       │   ├── 53 w: 17 v: 7
│   │       │   │   └── 71 w: 34 v: 9
│   │       │   │       └── 85 w: 44 v: 45
│   │       │   ├── 54 w: 28 v: 54
│   │       │   └── 55 w: 28 v: 59
│   │       │       ├── 72 w: 36 v: 100
│   │       │       └── 73 w: 39 v: 86
│   │       │           └── 86 w: 3 v: 86
│   │       ├── 33 w: 29 v: 19
│   │       ├── 34 w: 29 v: 15
│   │       └── 35 w: 50 v: 61
│   │           ├── 56 w: 6 v: 99
│   │           │   ├── 74 w: 41 v: 24
│   │           │   │   └── 87 w: 24 v: 64
│   │           │   ├── 75 w: 27 v: 24
│   │           │   │   ├── 88 w: 11 v: 91
│   │           │   │   ├── 89 w: 12 v: 86
│   │           │   │   │   └── 94 w: 33 v: 70
│   │           │   │   └── 90 w: 25 v: 66
│   │           │   │       └── 95 w: 34 v: 58
│   │           │   └── 76 w: 16 v: 19
│   │           │       └── 91 w: 15 v: 59
│   │           │           ├── 96 w: 14 v: 37
│   │           │           └── 97 w: 1 v: 82
│   │           ├── 57 w: 26 v: 4
│   │           ├── 58 w: 25 v: 16
│   │           │   ├── 77 w: 28 v: 84
│   │           │   │   └── 92 w: 42 v: 19
│   │           │   └── 78 w: 20 v: 10
│   │           └── 59 w: 3 v: 35
│   ├── 6 w: 22 v: 54
│   └── 7 w: 16 v: 14
│       ├── 17 w: 34 v: 30
│       │   └── 36 w: 5 v: 100
│       ├── 18 w: 33 v: 56
│       │   └── 37 w: 22 v: 65
│       ├── 19 w: 11 v: 79
│       └── 20 w: 23 v: 44
│           └── 38 w: 20 v: 13
│               ├── 60 w: 36 v: 40
│               │   └── 79 w: 37 v: 99
│               └── 61 w: 19 v: 35
├── 2 w: 40 v: 53
├── 3 w: 10 v: 15
│   ├── 10 w: 6 v: 86
│   │   ├── 24 w: 2 v: 4
│   │   ├── 25 w: 3 v: 16
│   │   └── 26 w: 15 v: 92
│   │       └── 45 w: 4 v: 26
│   │           └── 67 w: 22 v: 29
│   ├── 11 w: 8 v: 46
│   │   ├── 27 w: 32 v: 82
│   │   │   ├── 46 w: 34 v: 11
│   │   │   ├── 47 w: 17 v: 19
│   │   │   │   └── 68 w: 21 v: 20
│   │   │   └── 48 w: 40 v: 74
│   │   │       └── 69 w: 7 v: 12
│   │   │           ├── 82 w: 10 v: 22
│   │   │           └── 83 w: 46 v: 93
│   │   ├── 28 w: 8 v: 54
│   │   │   └── 49 w: 11 v: 36
│   │   └── 29 w: 48 v: 71
│   ├── 12 w: 34 v: 47
│   ├── 8 w: 36 v: 1
│   │   ├── 21 w: 43 v: 26
│   │   │   ├── 39 w: 27 v: 14
│   │   │   │   └── 62 w: 13 v: 19
│   │   │   ├── 40 w: 28 v: 72
│   │   │   │   └── 63 w: 34 v: 85
│   │   │   │       └── 80 w: 8 v: 97
│   │   │   └── 41 w: 45 v: 46
│   │   │       └── 64 w: 4 v: 18
│   │   ├── 22 w: 1 v: 25
│   │   │   ├── 42 w: 13 v: 71
│   │   │   └── 43 w: 39 v: 59
│   │   │       └── 65 w: 43 v: 31
│   │   └── 23 w: 48 v: 82
│   │       └── 44 w: 17 v: 84
│   │           └── 66 w: 43 v: 8
│   │               └── 81 w: 37 v: 49
│   │                   └── 93 w: 135 v: 11
│   │                       ├── 98 w: 68 v: 398
│   │                       └── 99 w: 55 v: 480
│   └── 9 w: 17 v: 43
└── 4 w: 18 v: 2
    ├── 13 w: 17 v: 99
    └── 14 w: 50 v: 75
```
You can get something like `[0,1,2,3,4,5,6,7,10,13,16,31,32]` that satify the first conditions easily.
Encode it and send it to server to get the first flag:
```python
from string import maketrans

base='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
diy_base='AiHheGuklOxE5wz+WS9JLZRY7FXnyV0jCQP/Kf3d4BqTr8MmUta6NbpIov2cDgs1'
t=maketrans(base,diy_base)
t2=maketrans(diy_base, base)

def cus_base64_enc(x):
	return x.encode('base64').translate(t)

def cus_base64_dec(x):
	return x.translate(t2).decode('base64')
chars="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"
l=[0,1,2,3,4,5,6,7,10,13,16,31,32]
l.sort()
x=''.join(map(lambda x:chars[x],l))
print cus_base64_enc(x).replace('\n','')
```

## Part2

### Solution 1
To get flag2, you can just solve the knapsack problem with dynamic programming or just brute force. Here is a example with dp:
```python
arr=[[6,82,-1],[31,46,1],[40,53,1],[10,15,1],[18,2,1],[22,51,2],[22,54,2],[16,14,2],[36,1,4],[17,43,4],[6,86,4],[8,46,4],[34,47,4],[17,99,5],[50,75,5],[41,54,6],[2,6,6],[34,30,8],[33,56,8],[11,79,8],[23,44,8],[43,26,9],[1,25,9],[48,82,9],[2,4,11],[3,16,11],[15,92,11],[32,82,12],[8,54,12],[48,71,12],[44,98,16],[2,71,17],[8,49,17],[29,19,17],[29,15,17],[50,61,17],[5,100,18],[22,65,19],[20,13,21],[27,14,22],[28,72,22],[45,46,22],[13,71,23],[39,59,23],[17,84,24],[4,26,27],[34,11,28],[17,19,28],[40,74,28],[11,36,29],[32,79,32],[50,45,32],[21,81,33],[17,7,33],[28,54,33],[28,59,33],[6,99,36],[26,4,36],[25,16,36],[3,35,36],[36,40,39],[19,35,39],[13,19,40],[34,85,41],[4,18,42],[43,31,44],[43,8,45],[22,29,46],[21,20,48],[7,12,49],[41,73,52],[34,9,54],[36,100,56],[39,86,56],[41,24,57],[27,24,57],[16,19,57],[28,84,59],[20,10,59],[37,99,61],[8,97,64],[37,49,67],[10,22,70],[46,93,70],[5,99,71],[44,45,72],[3,86,74],[24,64,75],[11,91,76],[12,86,76],[25,66,76],[15,59,77],[42,19,78],[11,20,82],[33,70,90],[34,58,91],[14,37,92],[1,82,92],[9,39,94],[25,95,94]]

cnt = len(arr)
m=233
children=[[] for i in range(cnt)]
w=[]
v=[]
root = 0
for i in range(cnt):
	l = arr[i]
	w.append(l[0])
	v.append(l[1])
	if l[2] != -1:
		children[l[2]-1].append(i)
	else:
		root = i

f = [[0 for j in range(m+1)] for i in range(cnt)]
sol = [[[] for j in range(m+1)] for i in range(cnt)]

def dfs(cur):
	for child in children[cur]:
		dfs(child)
		for j in range(m-w[cur], -1, -1):
			max_idx = -1
			val_list = []
			for k in range(j+1):
				if f[cur][j - k] + f[child][k] > f[cur][j]:
					f[cur][j] = f[cur][j - k] + f[child][k]
					sol[cur][j] = sol[cur][j - k] + sol[child][k][:]
	
	for i in range(m, w[cur]-1, -1):
		f[cur][i] = f[cur][i - w[cur]] + v[cur]
		sol[cur][i] = sol[cur][i - w[cur]][:]
		sol[cur][i].append(cur)

	for i in range(w[cur]):
		f[cur][i] = 0

dfs(root)
print f[root][m]
sol[root][m].sort()
print sol[root][m]
tot_v_ = 0
tot_w_ = 0
for i in sol[root][m]:
	tot_v_ += v[i]
	tot_w_ += w[i]
print 'v: %d w: %d'%(tot_v_, tot_w_)
```
Encrypt the result `[0, 1, 3, 5, 10, 11, 16, 25, 26, 28, 31, 32, 35, 52, 56, 59, 76, 91, 97]` to get the flag.
### Solution 2
There is also a `race condition` in server's logic.
There's no concurrency lock in `check` function, and nodes' flag are modified inside it.
There is also a long time interval between flags are cleaned and flags are checked when decrypting the base64 table with 1024 rounds RC4, which makes race condition easy to exploit.
So we want to find a timing that **in one connection**, we choose an node to make its flag true and then **in another connection** we choose its child so that we don't need to choose itself to bypass the father check.
Examine the tree, we can find node93 has a big weight and its children has huge values.
So the idea is to create a connection to choose node93, and then another connection choose its children:
```python
from pwn import *
import thread
import time

context.log_level = 'debug'
addr = '127.0.0.1'
port = 30754

while 1:
    conn0 = remote(addr, port)
    conn = remote(addr, port)
    
    conn0.sendline('5h5onKKf+doEhA==') # [0,3,8,23,44,66,81,93,98,99]
    conn.sendline('5hSKHUU=') # [0,4,13,98,99]

    x = conn.recvall()
    if 'N1CTF' in x:
        print x
        exit(0)
    conn.close()
    conn0.close()

```
After a few attempts, you get the two flags with ease

Nobody solved in this way, maybe I should made the tree more complicated..