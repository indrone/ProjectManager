from tinydb import TinyDB, Query
def insert(tablename,data):
	db = TinyDB(tablename)
	db.insert(data)

def get_all(tablename):
	db = TinyDB(tablename)
	return db.all()

def update(tablename,idx,info):
	db = TinyDB(tablename)
	table = Query()
	db.update(info, table.idx == idx)

def delete(tablename,idx):
	db = TinyDB(tablename)
	table = Query()
	db.remove(table.idx == idx)