import imaplib
import email
import struct
import time
import getpass
import winsound

class Mail:

	def __init__(self, user, password):
		self.user = user
		self.password = password
		self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
		self.mail.login(self.user, self.password)

	# Check for new mail, return number of new messages
	def check(self):

		self.mail.select()
		(returnCode, messages) = self.mail.search(None, "UNSEEN")

		n = 0
		if(returnCode == "OK"):
			for num in messages[0].split():
				print('Processing...')
				n += 1
				typ, data = self.mail.fetch(num, '(RFC822)')
				for response_part in data:
					if isinstance(response_part, tuple):
						original = email.message_from_bytes(response_part[1])

						print(original['From'])
						print(original['Subject'])
						typ, data = self.mail.store(num,'+FLAGS','\\Seen')
		return n

	# Run the check
	def run(self):
		self.messages = self.check()
		if(self.messages >= 1):
			print("You have " + str(self.messages) + " new message(s).")
			winsound.PlaySound("sounds/tada.wav", winsound.SND_ASYNC)


username = input("Gmail Username: ") + "@gmail.com"
password = getpass.getpass("Gmail Password: ")

instance = Mail(username, password)

while True:
	instance.run()