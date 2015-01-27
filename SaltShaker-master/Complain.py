import sqlite3
from datetime import datetime, tzinfo

DATABASE = 'comp_db.db'

def get_db():
   return sqlite3.connect(DATABASE)

def db_read():
   con = get_db()
   cur = con.cursor()
   cur.execute("SELECT * FROM comp_list ORDER BY -score")
   return cur.fetchall()

def db_add(string):
   con = get_db()
   cur = con.cursor()
   entry = (string, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
   cur.execute("INSERT INTO comp_list(content, score, bday) VALUES (?,?,?)", entry)
   con.commit()

def change_score(identity, change):
	con = get_db()
	cur = con.cursor()
	current_score = 0
	for complaint in cur.execute("SELECT identity, score FROM comp_list"):
		if complaint[0] == identity:
			current_score = complaint[1]
	edits = (current_score + change, identity)
	cur.execute("UPDATE comp_list SET score = ? WHERE identity = ?", edits)
	con.commit()

class Complaint:
	class_identity = 0
	def __init__(self, content, score = 0, bday = datetime.now(), identity = 1):
		self.score = score
		self.content = content
		self.identity = identity
		self.bday = bday

	def __repr__(self):
		return "(content:{0},score:{1},age:{2},id:{3})".format(self.content, self.score, self.bday, self.identity)

	def salt_it(self):
		"""
		>>> com = Complaint("This sucks...")
		>>> com.score
		0
		>>> com.content
		'This sucks...'
		>>> com.salt_it()
		>>> com.score
		1
		"""
		self.score += 1
		change_score(self, 1)

	def pepper_it(self):
		"""
		>>> com = Complaint("This sucks...")
		>>> com.score
		0
		>>> com.content
		'This sucks...'
		>>> com.pepper_it()
		>>> com.score
		-1
		"""
		self.score -= 1
		change_score(self, -1)

class Complaint_List:
	def __init__(self):
		"""
		>>> com = Complaint("This sucks...")
		>>> com2 = Complaint("This really sucks...")
		>>> my_lst = Complaint_List([com, com2])
		>>> com2.salt_it()
		>>> com2.score
		1
		>>> my_lst.sort()
		>>> str(my_lst)
		"['[1,This really sucks...]', '[0,This sucks...]']"
		"""
		#self.lst = []

	def __str__():
		if db_read():
			return [complain for complain in db_read()]
		return "empty list!"

	def unique_complaint(self, string):
		for c in db_read():
			if c[0] == string:
				return False
		return True

	def add_complaint(self, string):
		if self.unique_complaint(string):
			db_add(string)
	
	# def sort(self):
	# 	def key(complaint):
	# 		return -complaint.score
	# 	self.lst.sort(key = key)

	def get_complaints(self):
		# self.sort()
		# return self.lst
		lst = []

		for complaint in db_read():
			now = datetime.now()
			bday = datetime.strptime(complaint[2], "%Y-%m-%d %H:%M:%S.%f") 
			difference = now - bday
			if difference.days <= 4:
				lst.append(Complaint(complaint[0], complaint[1], complaint[2], complaint[3]))
		return lst

	def salt(self, complaint_id):
		# for complaint in self.lst:
		# 	if complaint.identity == complaint_id:
		# 		complaint.salt_it()	
		print("trying to salt")
		change_score(complaint_id, 1)


	def pepper(self, complaint_id):
		# for complaint in self.lst:
		# 	if complaint.identity == complaint_id:
		# 		complaint.pepper_it()
		print("tring to pepper")
		change_score(complaint_id, -1)

	# def print_list(self):
	# 	for i in range(len(self.lst)):
	# 		print('element', i, 'is', self.lst[i].score)



