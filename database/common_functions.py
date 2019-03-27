from hashlib import sha1
import random
import string
import os

def sha1_hash(s):
    return sha1(s.encode('utf-8')).hexdigest()

def gen_file_name(path, size):
    name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    while name in list(map(lambda x: ''.join(x.split('.')[::-1]), os.listdir(path))):
        name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    return name

def break_list(lst, cnt):
    n = len(lst)
    res = []
    for i in range(0, n, cnt):
        res.append(lst[i: min(n, i + cnt)])

    if len(res) == 0:
        res.append([])

    return res
