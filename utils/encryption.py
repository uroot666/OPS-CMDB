#encoding: utf-8

import hashlib

def md5_str(string):
    md5 = hashlib.md5()
    md5.update(bytes(string, encoding='utf-8'))
    return md5.hexdigest()

def md5_file(path):
    fhandler = open(path, 'rb')
    md5 = hashlib.md5()
    for line in fhandler:
        md5.update(line)
    fhandler.close()
    return md5.hexdigest()

if __name__ == '__main__':
    print(md5_str('123'))