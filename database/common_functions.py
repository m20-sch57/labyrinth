def sha1_hash(s):
    return sha1(s.encode('utf-8')).hexdigest()

def gen_file_name(path, size):
    name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    while name in list(map(lambda x: ''.join(x.split('.')[::-1]), os.listdir(path))):
        name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
    return name
