import psycopg2

# psycopg2로 DB 연결
class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host='localhost', dbname='testdb',user='testdb',password='testdb',port=5432)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()

# psycopg2로 DB 쿼리
class CRUD(Databases):
    def insertDB(self,schema,table,column,data):
        sql = " INSERT INTO {schema}.{table}({column}) VALUES ('{data}') ;".format(schema=schema,table=table,column=column,data=data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 
    
    def readDB(self,schema,table,column):
        sql = " SELECT {column} from {schema}.{table}".format(column=column,schema=schema,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def updateDB(self,schema,table,column,value,condition):
        sql = " UPDATE {schema}.{table} SET {column}='{value}' WHERE {column}='{condition}' ".format(schema=schema
        , table=table , column=column ,value=value,condition=condition )
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)

    def deleteDB(self,schema,table,condition):
        sql = " delete from {schema}.{table} where {condition} ; ".format(schema=schema,table=table,
        condition=condition)
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print( "delete DB err", e)

if __name__ == "__main__":
    db = CRUD()
    db.insertDB(schema='myschema',table='table',column='ID',data='유동적변경')
    print(db.readDB(schema='myschema',table='table',column='ID'))
    db.updateDB(schema='myschema',table='table',column='ID', value='와우',condition='유동적변경')
    db.deleteDB(schema='myschema',table='table',condition ="id != 'd'")