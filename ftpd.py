import os.path
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_ROOT = '/ftp_root'


def run_ftpd(user, password, host, port, anon):
    user_dir = os.path.join(FTP_ROOT, user)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)
    authorizer = DummyAuthorizer()
    authorizer.add_user(user, password, user_dir, perm="elradfmw")
    if anon:
        authorizer.add_anonymous("/ftp_root/nobody")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.permit_foreign_addresses = True

    server = FTPServer((host, port), handler)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default='user')
    parser.add_argument('--password', default='password')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=21)
    parser.add_argument('--anon', action='store_true')
    args = parser.parse_args()
    run_ftpd(**vars(args))

if __name__ == '__main__':
    main()
