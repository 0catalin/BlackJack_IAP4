from cryptography.fernet import Fernet

class Statistics():
    def __init__(self):
        statistics = self.decryptMessageAndReturnIt().split("/")
        try:
            self.total_games = int(statistics[0])
            self.total_wins = int(statistics[1])
            self.total_losses = int(statistics[2])
            self.total_blackjacks = int(statistics[3])
            self.profit = int(statistics[4])
        except IndexError:
            self.total_games = 0
            self.total_wins = 0
            self.total_losses = 0
            self.total_blackjacks = 0
            self.profit = 0
            self.encryptMessageAndInsertIntoFile()
        except ValueError:
            self.total_games = 0
            self.total_wins = 0
            self.total_losses = 0
            self.total_blackjacks = 0
            self.profit = 0
            self.encryptMessageAndInsertIntoFile()






    def generate_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            self.key_file.write(key)


    def load_key(self):
        return open("secret.key", "rb").read()


    def encrypt_message(self, message):
        key = self.load_key()
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message


    def decrypt_message(self, encrypted_message):
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        return decrypted_message.decode()

# use this when you are done with a message and you want to put it in the file
    def encryptMessageAndInsertIntoFile(self):
        msg = "/".join([self.total_games, self.total_wins, self.total_losses, self.total_blackjacks, self.profit])
        with open('database.txt', 'wb') as file:
            file.write(self.encrypt_message(msg))

# use this when you want to retrieve the message from the file
    def decryptMessageAndReturnIt(self):
        with open('database.txt', 'rb') as file:
            return self.decrypt_message(file.read())

    
    