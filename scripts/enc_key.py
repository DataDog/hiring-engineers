#!/usr/bin/python

from cryptography.fernet import Fernet
import base64
import sys
import os


def encrypt_key_from_cli():
    fernet_key=b'kLBTXhXvcUqVYbdZ7yE59C8GMoKbU9qsrWE3LO-xR7I='
    f=Fernet(fernet_key)
    cli_argument = sys.argv[1]
    token = f.encrypt(cli_argument.encode('UTF-8'))
    pw_str=token.decode(encoding='UTF-8')
    print(pw_str)

def main():
    encrypt_key_from_cli()

if __name__ == "__main__":
    main()
