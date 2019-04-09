import sqlite3

class Database:
	def __init__(self, db_file=':memory:'):
		""" create a database connection to a SQLite database """
		self.con = sqlite3.connect(db_file)
		#print(sqlite3.version)
		cur = self.con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS scores (
				score integer NOT NULL,
				name text
			);
		""")

	def close(self):
		self.con.close()

	def set_score(self, score, name="Anon"):
		cur = self.con.cursor()
		cur.execute("insert into scores(score, name) values (?, ?)", (score, name))
		return cur.lastrowid

	def get_scores(self):
		cur = self.con.cursor()
		cur.execute("select score, name from scores order by score desc limit 10")
		return cur.fetchall()