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

def CreateTableTicker():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Ticker    
                (CodigoTicker INTEGER PRIMARY KEY
                    ,CodigoSetor INTEGER
                    ,CodigoInstituicao INTEGER
                    ,FOREIGN KEY(CodigoInstituicao) REFERENCES Instituicao(CodigoInstituicao)
                    ,FOREIGN KEY(CodigoSetor) REFERENCES Setor(CodigoSetor))""")

def CreateTableCotacao():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Cotacao
                (CodigoCotacao INTEGER PRIMARY KEY
                    ,CodigoTicker INTEGER
                    ,CodigoInstituicao INTEGER
                    ,FOREIGN KEY(CodigoTicker) REFERENCES Ticker(CodigoTicker)
                   )""")


def CreateTableNoticia():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Noticia   
                (CodigoNoticia INTEGER PRIMARY KEY
                    ,CodigoTicker INTEGER
                    ,CodigoInstituicao INTEGER
                    ,FOREIGN KEY(CodigoTicker) REFERENCES Ticker(CodigoTicker)
                   )""")


CreateTableIndustria()
CreateTableSetor()
CreateTableTicker()
CreateTableCotacao()
CreateTableNoticia()