#!/usr/bin/env python2.7
import math
import argparse
import sys
from PIL import Image


def args(msg=None):
    print('[input picture] -c -k [message file] -o [output picture] for encription\n'
          '[input picture] -o [output message] for decryption\n')
    exit(msg)



class picture(object):
    def __init__(self, name):
        try:
            self.image = Image.open(name)
        except IOError:
            exit('File open error ' + name)
        self.data = bytearray(self.image.tobytes())
        self.size = self.image.size[0] * self.image.size[1]

    def crypto(self, crypto):
        
        i_ = 0
        i_ = last_bit(i_, self.data, byte(math.floor(len(crypto) % 256)))
        i_ = last_bit(i_, self.data, byte(math.floor(len(crypto) / 256)))
        
        j_ = 0
        while j_ < len(crypto):
            i_ = last_bit(i_, self.data, byte(crypto[j_]))
            j_ += 1

    def decrypt(self, crypto):
        j_ = 16
        i_ = 0
        while i_ < len(crypto):
            n = to_byte(self.data, j_, j_+8)
            crypto[i_] = n
            j_ += 8
            i_ += 1

    def write(self, outname):
        self.image = Image.frombytes(self.image.mode, self.image.size, bytes(self.data))
        try:
            self.image.save(outname, 'PNG')
        except IOError:
            exit('File saving error ' + outname)


def last_bit(i_, a, b):
    for x in range(0, 8):
        if a[i_] % 2 ^ b[x]:
            if a[i_] % 2 == 1:
                a[i_] -= 1
            else:
                a[i_] += 1
        i_ += 1
    return i_


def byte(a):
    i = 0
    s = 8 * [0]
    while i != 8:
        s[i] = int(a % 2)
        a /= 2
        i += 1
    return s


def read(infile):
    st = ''
    try:
        with open(infile, 'rb') as f:
            st = f.read()
    except IOError:
        print("No such file or directory.")
    return st


def write(a, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(bytes(a))
    except IOError:
        exit("Error")


def to_byte(a, start, end):
    n = 0
    for i in reversed(range(start, end)):
        n <<= 1
        n += a[i] % 2
    return n


def create_parser():
    pars = argparse.ArgumentParser()
    pars.add_argument('input_file')
    pars.add_argument('-c', '--coding', action='store_true', default=False)
    pars.add_argument('-d', '--decoding', action='store_true', default=False)
    pars.add_argument('-k', '--key')
    pars.add_argument('-o', '--output', required=True)
    return pars




if __name__ == '__main__':
    if len(sys.argv) == 1:
        args()
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.coding and namespace.decoding:
        args("\nEnter one -c or -d key")

    elif namespace.coding:
        file_data = picture(namespace.input_file)
        crypto_data = read(namespace.key)
        crypto_data = bytearray(crypto_data)
        if file_data.size > len(crypto_data) * 8:  
            file_data.crypto(crypto_data)
        else:
            exit("Wrong picture size")
        file_data.write(namespace.output)

  
    elif namespace.decoding:
        file_data = picture(namespace.input_file)
        size = to_byte(file_data.data, 0, 16)
        crypto_data = bytearray([0]*size)
        file_data.decrypt(crypto_data)
        write(crypto_data,namespace.output)
