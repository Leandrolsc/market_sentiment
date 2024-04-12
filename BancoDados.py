import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

def CreateTableIndustria():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Industria 
                (CodigoInstituicao INTEGER PRIMARY KEY
                ,Industria TEXT
                ,Descricao TEXT)""")

def CreateTableSetor():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Setor     
                (CodigoSetor INTEGER PRIMARY KEY
                ,Setor TEXT
                ,Descricao TEXT)""")


CreateTableIndustria()
CreateTableSetor()
