from peewee import *
import secrets
db=SqliteDatabase('proxy.db')

class sources(Model):
    id=AutoField()
    source=CharField()
    destination=CharField()
    identifier=IntegerField(default=secrets.token_hex(12),unique=True)
    delay=IntegerField(default=10)
    @classmethod
    def get_destination(self,source:str)->str:
        return sources.get(sources.source==source).destination

    class  Meta:
        database=db
db.create_tables([sources],safe=True)
clientdata=sources.select().where(sources.source=='127.0.0.1')[0]
print(clientdata.destination)