import psycopg2
from anytree import AnyNode,RenderTree
from anytree.exporter import JsonExporter
from ltree import Ltree

really_path=os.path.split(os.path.realpath(__file__))[0]
#database
conn=psycopg2.connect(database="npupt",user="postgres",password="root",host="localhost",port="5432")
cur=conn.cursor()
cur.execute("SELECT * FROM public.user order by id")
rows=cur.fetchall()
exp=JsonExporter(indent=2,sort_keys=False)
root=AnyNode(name="root",value=0)
list1=[root]
AnyNode()
f=open(os.path.join(really_path,"name.txt"),"w",encoding='utf-8')
f.write("root\n")
for row in rows:
    f.write(str.lower(row[2])+'\n')