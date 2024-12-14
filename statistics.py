from cryptography.fernet import Fernet, InvalidToken


class Statistics():
    def __init__(self):
        statistics = self.decryptMessageAndReturnIt().split("/")
        try:
            self.total_games = int(statistics[0])
            self.total_wins = int(statistics[1])
            self.total_losses = int(statistics[2])
            self.total_blackjacks = int(statistics[3])
            self.profit = int(statistics[4])
        except (ValueError, IndexError):
            self.reset_statistics()
            self.encryptMessageAndInsertIntoFile()



    def generate_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            self.key_file.write(key)


    def load_key(self):
        return open("secret.key", "rb").read()

    def reset_statistics(self):
        self.total_games = 0
        self.total_wins = 0
        self.total_losses = 0
        self.total_blackjacks = 0
        self.profit = 0

    def encrypt_message(self, message):
        key = self.load_key()
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message


    def decrypt_message(self, encrypted_message):
        try:
            key = self.load_key()
            f = Fernet(key)
            decrypted_message = f.decrypt(encrypted_message)
            return decrypted_message.decode()
        except InvalidToken:
            self.reset_statistics()
            self.encryptMessageAndInsertIntoFile()
            return ""


# use this when you are done with a message and you want to put it in the file

# for Petre : create a Statistics instance for when you want to update statistics, update whatever you have to change from the Statistics instance that you create
# and use this function before quitting the game for the statistics to save. (preferably to make a try except block where if the user leaves the progress is saved)
    def encryptMessageAndInsertIntoFile(self):
        msg = "/".join([str(self.total_games), str(self.total_wins), str(self.total_losses), str(self.total_blackjacks), str(self.profit)])
        with open('database.txt', 'wb') as file:
            file.write(self.encrypt_message(msg))

# use this when you want to retrieve the message from the file
    def decryptMessageAndReturnIt(self):
        try:
            with open('database.txt', 'rb') as file:
                encrypted_data = file.read()
            return self.decrypt_message(encrypted_data)
        except FileNotFoundError:
            self.reset_statistics()
            self.encryptMessageAndInsertIntoFile()
            return ""

    
    