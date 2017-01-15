import argparse
import socket

class IRCClient:
    """Class used to represent IRC connection."""

    def __init__(self, username, nickname=None, realname=None):
        self.username = username
        self.nickname = nickname or username
        self.realname = realname or username
        self.socket = socket.socket()

    def connect(self, address, port):
        self.socket.connect((address, port))
        self.send('NICK {}'.format(self.nickname))
        self.send('USER {} 0 * :{}'.format(self.username, self.realname))

    def send(self, message):
        self.socket.send((message + '\n').encode())

    def pong(self):
        buffer = ""
        while True:
            buffer += self.socket.recv(4096).decode()
            while '\r\n' in buffer:
                message, buffer = buffer.split('\r\n', maxsplit=1)
                print(message)
                command, *params = message.split()
                if command == 'PING':
                    print('PONG!\r\n')
                    self.send('PONG {}'.format(params[0]))


def main():
    # Parsing arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', type=str, default='chat.freenode.net',
                        help='Server name.')
    parser.add_argument('-p', '--port', type=int, default=6667,
                        help='Server port.')
    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Username used for log in.')
    parser.add_argument('-n', '--nickname', type=str,
                        help='Defines what name people will see when you send a chat message.')
    parser.add_argument('-rn', '--realname', type=str,
                        help='Your real name.')
    args = parser.parse_args()

    irc_client = IRCClient(args.username, args.nickname, args.realname)
    irc_client.connect(args.server, args.port)
    irc_client.pong()

if __name__ == '__main__':
    main()
