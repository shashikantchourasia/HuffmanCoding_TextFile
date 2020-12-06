import heapq
import os

class Huff_Code:
	def __init__(self, path):
		self.path = path
		self.stack = []
		self.key = {}
		self.back_chart = {}

	class Mainbranch:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.lt = None
			self.rt = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other,Mainbranch)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def cre_freq_dict(self, text):
		fre = {}
		for per in text:
			if not per in fre:
				fre[per] = 0
			fre[per] += 1
		return fre

	def cre_leep(self, fre):
		for x in fre:
			branch = self.Mainbranch(x, fre[x])
			heapq.heappush(self.stack, branch)

	def narr_branch(self):
		while(len(self.stack)>1):
			a = heapq.heappop(self.stack)
			b = heapq.heappop(self.stack)

			comb = self.Mainbranch(None, a.freq + b.freq)
			comb.lt = a
			comb.rt = b

			heapq.heappush(self.stack, comb)


	def cre_prog_aid(self, root, exact_branch):
		if(root == None):
			return

		if(root.char != None):
			self.key[root.char] = exact_branch
			self.back_chart[exact_branch] = root.char
			return

		self.cre_prog_aid(root.lt, exact_branch + "0")
		self.cre_prog_aid(root.rt, exact_branch + "1")


	def cre_prog(self):
		root = heapq.heappop(self.stack)
		exact_branch = ""
		self.cre_prog_aid(root, exact_branch)


	def com_cipher(self, text):
		cipher_word = ""
		for per in text:
			cipher_word += self.key[per]
		return cipher_word


	def pack_cipher(self, cipher_word):
		exc_pack = 8 - len(cipher_word) % 8
		for i in range(exc_pack):
			cipher_word += "0"

		pack_data = "{0:08b}".format(exc_pack)
		cipher_word = pack_data + cipher_word
		return cipher_word


	def ac_list(self, word_cipher):
		if(len(word_cipher) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		z = bytearray()
		for i in range(0, len(word_cipher), 8):
			p = word_cipher[i:i+8]
			z.append(int(p, 2))
		return z


	def press(self):
		fname, fext = os.path.splitext(self.path)
		out_pt = fname + ".bin"

		with open(self.path, 'r+') as file, open(out_pt, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			fre = self.cre_freq_dict(text)
			self.cre_leep(fre)
			self.narr_branch()
			self.cre_prog()

			cipher_word = self.com_cipher(text)
			word_cipher = self.pack_cipher(cipher_word)

			z = self.ac_list(word_cipher)
			output.write(bytes(z))

		print("Test file is compressed")
		return out_pt