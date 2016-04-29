import os.path
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_ROOT = '/ftp_root'


def run_ftpd(user, password, host='127.0.0.1', port=21, anon=True):
    user_dir = os.path.join(FTP_ROOT, user)
    os.mkdir(user_dir)
    authorizer = DummyAuthorizer()
    authorizer.add_user(user, password, user_dir, perm="elradfmw")
    if anon:
        authorizer.add_anonymous("/ftp_root/nobody")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer((host, port), handler)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='user')
    parser.add_argument('--password', default='password')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=21)
    parser.add_argument('--anon', action='store_true')
    args = parser.parse_args()
    run_ftpd(**vars(args))

if __name__ == '__main__':
    main()
