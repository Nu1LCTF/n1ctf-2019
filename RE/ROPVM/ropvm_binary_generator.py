from pwn import *

flag_buf = 0x6cd000
input_prompt = 0x6cd100
correct_prompt = 0x6cd180
wrong_prompt = 0x6cd1c0
correct_buf = 0x6cd200
sum = 0x6cd300
delta = 0x6cd304
v0 = 0x6cd308
v1 = 0x6cd30c
k0 = 0x6cd310
k1 = 0x6cd314
k2 = 0x6cd318
k3 = 0x6cd31c
temp_buf = 0x6cd400
nop_buf = 0x6cd500
table_buf = 0x6cd600
i = table_buf
j = table_buf + 8
entry = 0x6cbbb8


def save_data(data, addr):
    buf  = ''
    buf += p64(0x442976) # pop rdx; ret
    buf += p64(data)
    buf += p64(0x4015e6) # pop rdi; ret
    buf += p64(addr + 8)
    buf += p64(0x4315c6) # mov qword ptr [rdi - 8], rdx; ret; 
    return buf

def __read(fd, buff, leng):
    buf  = ''
    buf += p64(0x4015e6) # pop rdi; ret
    buf += p64(fd)
    buf += p64(0x401707) # pop rsi; ret
    buf += p64(buff)
    buf += p64(0x442976)
    buf += p64(leng)
    buf += p64(0x43f4a0) # read
    return buf

def __puts(buff):
    buf  = ''
    buf += p64(0x4015e6) # pop rdi; ret
    buf += p64(buff)
    buf += p64(0x40fbe0) # puts
    return buf

def __exit(val):
    buf  = ''
    buf += p64(0x4015e6) # pop rdi; ret
    buf += p64(val)
    buf += p64(0x43eaf0) # exit
    return buf

data = p32(0xacd01111)

code = ''
code += save_data(u64('Input Fl'), input_prompt)
code += save_data(u64('ag: '.ljust(8,'\x00')), input_prompt + 8)
code += save_data(u64('Congratu'), correct_prompt)
code += save_data(u64('lations!'), correct_prompt + 8)
code += save_data(0, correct_prompt + 16)
code += save_data(u64('Wrong Fl'), wrong_prompt)
code += save_data(u64('ag! '.ljust(8, '\x00')), wrong_prompt + 8)
code += save_data(0x146d16a886dab2be, correct_buf)
code += save_data(0x54f1658f3c9edb52, correct_buf + 8)
code += save_data(0x2a33699d19c12643, correct_buf + 16)
code += save_data(0xc1ce322600cd9e6b, correct_buf + 24)
code += save_data(0, v0)
code += save_data(u64("F14gF114"), k0)
code += save_data(u64("gF11114g"), k2)
code += save_data(4, table_buf + 8)
code += save_data(flag_buf, table_buf + 16)
code += __puts(input_prompt)
code += __read(0, flag_buf, 32)


code += p64(0x4015e6) # pop rdi; ret
code += p64(entry - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(3176)
code += p64(0x426133) # add rax, rdi; ret
code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 24 - 0x308)
code += p64(0x470e06) # mov qword ptr [rdi + 0x308], rax; ret; 

code += p64(0x4015e6) # pop rdi; ret
code += p64(entry - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(3736)
code += p64(0x426133) # add rax, rdi; ret
code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 32 - 0x308)
code += p64(0x470e06) # mov qword ptr [rdi + 0x308], rax; ret; 

# 0x0000000000426133: add rax, rdi; ret; 
# 0x0000000000478540: mov rax, qword ptr [rax + 8]; ret; 
# 0x0000000000470e06: mov qword ptr [rdi + 0x308], rax; ret; 

print len(code)

# code += save_data(0x4242424241414141, v0)
code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 16 - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(0x10000000000000000 - 8)
code += p64(0x426133) # add rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(v0 - 0x308)
code += p64(0x470e06) # mov qword ptr [rdi + 0x308], rax; ret; 

code += save_data(0x5f3759df00000000, sum)

code += save_data(32, i)

print len(code) 
# 920




code += p64(0x4015e6) # pop rdi; ret
code += p64(v1)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474849) # pop rcx; dec dword ptr [rax + 0x63]; ret;  # rax + 0x63 == 0x6cd30c + 0x63
code += p64(4)
# cl = 4
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = v1
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x20 + 4)
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0) # rbx
# temp_buf[1] = v1
code += p64(0x4443d1) # shl eax, cl; pop rbx; pop rbp; ret; 
# eax <<= 4
code += p64(temp_buf - 0x20) # rbx 
code += p64(0) # rbp
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0) # rbx
# temp_buf[0] = v1 << 4
code += p64(0x4015e6) # pop rdi; ret
code += p64(v1)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474849) # pop rcx; dec dword ptr [rax + 0x63]; ret;  # rax + 0x63 == 0x6cd30c + 0x63
code += p64(5)
# cl = 5
code += p64(0x442976) # pop rdx; ret
code += p64(temp_buf + 4)
# rdx = &temp_buf[1]
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x426d69) # shr dword ptr [rdx], cl; add dword ptr [rax], eax; ret; 
# temp_buf[1] = v1 >> 5
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 4)
# rbx = &temp_buf[1]
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
# rsi = &temp_buf[0]
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = temp_buf[0]
code += p64(0x4015e6) # pop rdi; ret
code += p64(0x4002e1) # ret
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x45612a) # xor ecx, dword ptr [rbx]; jmp rax
# ecx ^= rbx
# ecx = temp_buf[1] ^ temp_buf[0]
code += p64(0x4015e6) # pop rdi; ret
code += p64(v1)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = v1
code += p64(0x425efa) # add eax, ecx; ret;
# eax = v1 + ((v1 << 4) ^ (v1 >> 5))
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x20)
# rbx + 0x20 = &temp_buf[0]
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# temp_buf[0] = eax
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(sum)
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = sum
code += save_data(0x4002e1, temp_buf + 16)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 16 + 0x70) # ret
code += p64(0x4015e6) # pop rdi; ret
code += p64(3)
# rdi = 3
code += p64(0x46f6bb) # and ecx, edi; jmp qword ptr [rsi - 0x70];
# ecx = sum & 3
code += p64(0x442976) # pop rdx; ret
code += p64(k0)
# rdx = &k0
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
# rax = 0
code += p64(0x4290f3) # mov ecx, dword ptr [rdx + rcx*4]; mov eax, dword ptr [rdx + rax*4]; sub eax, ecx; ret; 
# ecx = key[sum & 3]
code += p64(0x4015e6) # pop rdi; ret
code += p64(sum)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = sum
code += p64(0x425efa) # add eax, ecx; ret;
# eax = sum + key[sum & 3]
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 4 - 0x20)
# rbx + 0x20 = &temp_buf[1]
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# temp_buf[1] = eax
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 4)
# rbx = &temp_buf[1]
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
# rsi = &temp_buf[0]
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = temp_buf[0]
code += p64(0x4015e6) # pop rdi; ret
code += p64(0x4002e1) # ret
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x45612a) # xor ecx, dword ptr [rbx]; jmp rax
# ecx ^= rbx
# ecx = temp_buf[1] ^ temp_buf[0]
# ecx = ((v1 << 4) ^ (v1 >> 5) + v1) ^ (sum + key[sum & 3])
code += p64(0x4015e6) # pop rdi; ret
code += p64(v0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = v0
code += p64(0x425efa) # add eax, ecx; ret;
# eax = v0 + ecx
code += p64(0x400e25) # pop rbx; ret
code += p64(v0 - 0x20)
# rbx + 0x20 = &v0
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# v0 = eax


code += p64(0x4015e6) # pop rdi; ret
code += p64(sum)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = sum
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(delta)
# rsi = &delta
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = delta
code += p64(0x425efa) # add eax, ecx; ret;
# eax = sum + delta
code += p64(0x400e25) # pop rbx; ret
code += p64(sum - 0x20)
# rbx + 0x20 = &sum
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# sum = eax


code += p64(0x4015e6) # pop rdi; ret
code += p64(v0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474849) # pop rcx; dec dword ptr [rax + 0x63]; ret;  # rax + 0x63 == 0x6cd30c + 0x63
code += p64(4)
# cl = 4
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = v0
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x20 + 4)
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0) # rbx
# temp_buf[1] = v0
code += p64(0x4443d1) # shl eax, cl; pop rbx; pop rbp; ret; 
# eax <<= 4
code += p64(temp_buf - 0x20) # rbx 
code += p64(0) # rbp
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0) # rbx
# temp_buf[0] = v0 << 4
code += p64(0x4015e6) # pop rdi; ret
code += p64(v0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474849) # pop rcx; dec dword ptr [rax + 0x63]; ret;  # rax + 0x63 == 0x6cd30c + 0x63
code += p64(5)
# cl = 5
code += p64(0x442976) # pop rdx; ret
code += p64(temp_buf + 4)
# rdx = &temp_buf[1]
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x426d69) # shr dword ptr [rdx], cl; add dword ptr [rax], eax; ret; 
# temp_buf[1] = v0 >> 5
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 4)
# rbx = &temp_buf[1]
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
# rsi = &temp_buf[0]
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = temp_buf[0]
code += p64(0x4015e6) # pop rdi; ret
code += p64(0x4002e1) # ret
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x45612a) # xor ecx, dword ptr [rbx]; jmp rax
# ecx ^= *rbx
# ecx = temp_buf[1] ^ temp_buf[0]
code += p64(0x4015e6) # pop rdi; ret
code += p64(v0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = v0
code += p64(0x425efa) # add eax, ecx; ret;
# eax = v0 + ((v0 << 4) ^ (v0 >> 5))
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x20)
# rbx + 0x20 = &temp_buf[0]
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# temp_buf[0] = eax
code += p64(0x4015e6) # pop rdi; ret
code += p64(sum)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = sum
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x20 + 8)
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0) # rbx
# temp_buf[2] = eax
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474849) # pop rcx; dec dword ptr [rax + 0x63]; ret;  
code += p64(11)
# cl = 11
code += p64(0x442976) # pop rdx; ret
code += p64(temp_buf + 8)
# rdx = &temp_buf[2]
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x426d69) # shr dword ptr [rdx], cl; add dword ptr [rax], eax; ret; 
# temp_buf[2] = sum >> 11
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 8)
# rsi = &temp_buf[2]
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = temp_buf[2]
code += save_data(0x4002e1, temp_buf + 16)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 16 + 0x70) # ret
code += p64(0x4015e6) # pop rdi; ret
code += p64(3)
# rdi = 3
code += p64(0x46f6bb) # and ecx, edi; jmp qword ptr [rsi - 0x70];
# ecx = (sum >> 11) & 3
code += p64(0x442976) # pop rdx; ret
code += p64(k0)
# rdx = &k0
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
# rax = 0
code += p64(0x4290f3) # mov ecx, dword ptr [rdx + rcx*4]; mov eax, dword ptr [rdx + rax*4]; sub eax, ecx; ret; 
# ecx = key[(sum >> 11) & 3]
code += p64(0x4015e6) # pop rdi; ret
code += p64(sum)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = sum
code += p64(0x425efa) # add eax, ecx; ret;
# eax = sum + key[(sum >> 11) & 3]
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 4 - 0x20)
# rbx + 0x20 = &temp_buf[1]
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# temp_buf[1] = eax
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 4)
# rbx = &temp_buf[1]
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
# rsi = &temp_buf[0]
code += p64(0x43b3d1) # mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# ecx = temp_buf[0]
code += p64(0x4015e6) # pop rdi; ret
code += p64(0x4002e1) # ret
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x45612a) # xor ecx, dword ptr [rbx]; jmp rax
# ecx ^= rbx
# ecx = temp_buf[1] ^ temp_buf[0]
# ecx = ((v0 << 4) ^ (v0 >> 5) + v0) ^ (sum + key[(sum >> 11) & 3])
code += p64(0x4015e6) # pop rdi; ret
code += p64(v1)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
# eax = v1
code += p64(0x425efa) # add eax, ecx; ret;
# eax = v1 + ecx
code += p64(0x400e25) # pop rbx; ret
code += p64(v1 - 0x20)
# rbx + 0x20 = &v1
code += p64(0x47caa3) # mov dword ptr [rbx + 0x20], eax; pop rbx; ret; 
code += p64(0)
# v1 = eax

code += p64(0x4015e6) # pop rdi; ret
code += p64(i - 1)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x41072c) # dec dword ptr [rax + 1]; ret; 
# ecx = i
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
# if i == 0 eax = 0 else eax = 1
code += save_data(3176 - 1048, temp_buf)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x47ce2f) # imul ecx; ret; 
code += save_data(0x4002e1, temp_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(table_buf + 24)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
code += p64(0x423b08) # sub rax, rdi; ret; 
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x18) 
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x49c7ad) # mov rsp, rcx; ret; 

print len(code)

code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(v0)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 16 - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret;
code += p64(0x4015e6) # pop rdi; ret
code += p64(0x10000000000000000 - 0x40)
code += p64(0x426133) # add rax, rdi; ret
code += p64(0x463bcc) # mov qword ptr [rax + 0x40], rcx; ret; 

# 0x0000000000463bcc: mov qword ptr [rax + 0x40], rcx; ret; 

code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 16 - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(8)
code += p64(0x426133) # add rax, rdi; ret
code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 16 - 0x308)
code += p64(0x470e06) # mov qword ptr [rdi + 0x308], rax; ret; 




code += p64(0x4015e6) # pop rdi; ret
code += p64(j - 1)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x41072c) # dec dword ptr [rax + 1]; ret; 
# ecx = j
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
# if j == 0 eax = 0 else eax = 1
code += save_data(3736 - 880, temp_buf)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x47ce2f) # imul ecx; ret; 
code += save_data(0x4002e1, temp_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(table_buf + 32)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
code += p64(0x423b08) # sub rax, rdi; ret; 
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x18) 
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x49c7ad) # mov rsp, rcx; ret; 


print len(code)

code += save_data(0x4002e1, temp_buf)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(flag_buf - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(correct_buf - 8)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x423b08) # sub rax, rdi; ret;
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 0x80 - 0x18)
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)

code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(flag_buf)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(correct_buf)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x423b08) # sub rax, rdi; ret;
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 0x88 - 0x18)
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)

code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(flag_buf + 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(correct_buf + 8)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x423b08) # sub rax, rdi; ret;
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 0x90 - 0x18)
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)

code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(flag_buf + 16)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(correct_buf + 16)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x423b08) # sub rax, rdi; ret;
code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf + 0x98 - 0x18)
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)

code += p64(0x4015e6) # pop rdi; ret
code += p64(entry - 8)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x478540) # mov rax, qword ptr [rax + 8]; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(5264)
code += p64(0x426133) # add rax, rdi; ret
code += p64(0x4015e6) # pop rdi; ret
code += p64(table_buf + 40 - 0x308)
code += p64(0x470e06) # mov qword ptr [rdi + 0x308], rax; ret; 

code += p64(0x4260df) # xor rax, rax; ret; 
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 0x80)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x425ef9) # add rax, rcx; ret;
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 0x88)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x425ef9) # add rax, rcx; ret;
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 0x90)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x425ef9) # add rax, rcx; ret;
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf + 0x98)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x425ef9) # add rax, rcx; ret;

code += p64(0x4015e6) # pop rdi; ret
code += p64(0)
code += p64(0x416920) # mov rax, rdi; ret
code += p64(0x416a6c) # setne al; neg eax; ret; 
code += p64(0x416a6f) # neg eax; ret;
code += save_data(5264 - 5216, temp_buf)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x47ce2f) # imul ecx; ret; 
code += save_data(0x4002e1, temp_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x420627) # mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
code += p64(0) * 3
code += p64(0x442976) # pop rdx; ret
code += p64(table_buf + 40)
code += p64(0x426e48) # mov rax, rdx; ret; 
code += p64(0x474a89) # mov eax, qword ptr [rax]; ret 
code += p64(0x423b08) # sub rax, rdi; ret; 
code += p64(0x400e25) # pop rbx; ret
code += p64(temp_buf - 0x18) 
code += p64(0x488064) # mov qword ptr [rbx + 0x18], rax; pop rbx; ret;  
code += p64(0)
code += p64(0x4015e6) # pop rdi; ret
code += p64(nop_buf)
code += p64(0x401707) # pop rsi; ret
code += p64(temp_buf)
code += p64(0x43b430) # mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 
code += p64(0x49c7ad) # mov rsp, rcx; ret; 

print len(code)

code += __puts(wrong_prompt)
code += __exit(0)

print len(code)

code += __puts(correct_prompt)

# 0x0000000000425ef9: add rax, rcx; ret; 

# 0x0000000000488064: mov qword ptr [rbx + 0x18], rax; pop rbx; ret; 
# 0x0000000000426e48: mov rax, rdx; ret; 
# 0x0000000000420627: mov rdi, rax; pop rbx; pop rbp; pop r12; jmp rcx;
# 0x0000000000423b08: sub rax, rdi; ret; 
# 0x000000000041072c: dec dword ptr [rax + 1]; ret; 
# 0x00000000004358b8: pop rcx; jmp qword ptr [rdx - 0xf]; 
# 0x000000000047a44d: dec ecx; ret; 
# 0x000000000047ce2f: imul ecx; ret; 

# 0x000000000043b430: mov rcx, qword ptr [rsi]; mov byte ptr [rdi + 8], dh; mov qword ptr [rdi], rcx; ret; 

# 0x00000000004290f3: mov ecx, dword ptr [rdx + rcx*4]; mov eax, dword ptr [rdx + rax*4]; sub eax, ecx; ret; 
# 0x000000000046f6bb: and ecx, edi; jmp qword ptr [rsi - 0x70];
# 0x00000000004354d1: mov edx, dword ptr [rsi]; mov qword ptr [rdi], rdx; ret; 
# 0x000000000049c7ad: mov rsp, rcx; ret; 
# 0x0000000000426133: add rax, rdi; ret; 
# 0x000000000040dd0f: and bl, dh; ret;
# 0x0000000000416a6f: neg eax; ret; 
# 0x0000000000416a6c: setne al; neg eax; ret; 
# 0x00000000004260df: xor rax, rax; ret; 
# 0x000000000045612a: xor ecx, dword ptr [rbx]; jmp rax; 
# 0x00000000004002e1: ret; 
# 0x000000000049d053: mov dword ptr [rax - 0x7d], ecx; ret;
# 0x000000000043b3d1: mov ecx, dword ptr [rsi]; mov word ptr [rdi], cx; mov byte ptr [rdi + 2], dh; ret;
# 0x0000000000425efa: add eax, ecx; ret;
# 0x0000000000426134: add eax, edi; ret; 
# 0x0000000000401707: pop rsi; ret; 

code += __exit(0)




f = open('binary', 'wb')
f.write(data + p32(len(code)) + code)
f.close()
