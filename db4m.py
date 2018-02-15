import sqlite3

class DB4M:


	def __init__(self, name=None):
		'''The constructor of the Database class'''
		self.conn = None
		self.cursor = None

		if name:
			self.open(name)
	
	def open(self,name):
		'''This function manually opens a new database connection. 
		The database can also be opened in the constructor or as a context manager.'''
		try:
			self.conn = sqlite3.connect(name);
			self.cursor = self.conn.cursor()

		except sqlite3.Error as e:
			print("Error connecting to database!")
	
	def close(self):
		
		if self.conn:
			self.conn.commit()
			self.cursor.close()
			self.conn.close()

	def __enter__(self):
		
		return self

	def __exit__(self,exc_type,exc_value,traceback):
		
		self.close()


	#######################################################################
	#
	## Function to fetch/query data from a database.
	#
	#  This is the main function used to query a database for data.
	#
	#  @param table The name of the database's table to query from.
	#
	#  @param columns The string of columns, comma-separated, to fetch.
	#
	#  @param limit Optionally, a limit of items to fetch.
	#
	#######################################################################

	def get(self,table,columns,limit=None):

		query = "SELECT {0} from {1};".format(columns,table)
		self.cursor.execute(query)

		# fetch data
		rows = self.cursor.fetchall()

		return rows[len(rows)-limit if limit else 0:]


	#######################################################################
	#
	## Utilty function to get the last row of data from a database.
	#
	#  @param table The database's table from which to query.
	#
	#  @param columns The columns which to query.
	#
	#######################################################################

	def getLast(self,table,columns):
		
		return self.get(table,columns,limit=1)[0]

	
	#######################################################################
	#
	## Utility function that converts a dataset into CSV format.
	#
	#  @param data The data, retrieved from the get() function.
	#
	#  @param fname The file name to store the data in.
	#
	#  @see get()
	#
	#######################################################################

	@staticmethod
	def toCSV(data,fname="output.csv"):
		
		with open(fname,'a') as file:
			file.write(",".join([str(j) for i in data for j in i]))


	#######################################################################
	#
	## Function to write data to the database.
	#
	#  The write() function inserts new data into a table of the database.
	#
	#  @param table The name of the database's table to write to.
	#
	#  @param columns The columns to insert into, as a comma-separated string.
	#
	#  @param data The new data to insert, as a comma-separated string.
	#
	#######################################################################
				
	def write(self,table,columns,data):
		
		query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table,columns,data)

		self.cursor.execute(query)


	#######################################################################
	#
	## Function to query any other SQL statement.
	#
	#  This function is there in case you want to execute any other sql
	#  statement other than a write or get.
	#
	#  @param sql A valid SQL statement in string format.
	#
	#######################################################################

	def query(self,sql):
		self.cursor.execute(sql)

if __name__ == '__main__':
	with open('init.sql') as sc:
		sqlCommands = sc.read().split('----')
	journal = sqlCommands[0]
	database = 'forem.db'
	with DB4M(database) as mydb:
		mydb.query(journal)

