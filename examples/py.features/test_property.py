def test_prop():
	#def get_paperino(self):
	# 	return self.paperino
	#return property(get_paperino)
	return property(lambda self : self.paperino)

class pippo():
	pluto = test_prop()
	def __init__(self, paperino_val):
		self.paperino = paperino_val
		self.topolino = test_prop()

a = pippo("Eugenio")
b = pippo("Parodi")
c = pippo("Rocks!!!")

print(a.pluto)
print(b.pluto)
print(c.pluto)

print(a.topolino)
print(b.topolino)
print(c.topolino)