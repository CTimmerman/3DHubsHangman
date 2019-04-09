import sqlite3, time

class Database:
	def __init__(self, db_file=':memory:'):
		""" create a database connection to a SQLite database """
		self.con = sqlite3.connect(db_file)
		print(sqlite3.version)
		cur = self.con.cursor()
		cur.execute("""
			CREATE TABLE IF NOT EXISTS scores (
				score integer NOT NULL,
				name text,
				timestamp integer
			);
		""")

	def close(self):
		self.con.close()

	def set_score(self, score, name="Anon"):
		cur = self.con.cursor()
		cur.execute("insert into scores(score, name, timestamp) values (?, ?, ?)", (score, name, time.time()))
		self.con.commit()
		return cur.lastrowid

	def get_scores(self, limit=1000):
		cur = self.con.cursor()
		cur.execute("select score, name, timestamp from scores order by score desc, timestamp desc limit ?", (limit,))
		return cur.fetchall()