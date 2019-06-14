import psycopg2
from anytree import AnyNode,RenderTree
from anytree.exporter import JsonExporter
from ltree import Ltree
really_path=os.path.split(os.path.realpath(__file__))[0]
#connect to postgresql you can also use any other database you perfer
conn=psycopg2.connect(database="test",user="postgres",password="root",host="localhost",port="5432")
cur=conn.cursor()
cur.execute("SELECT * FROM public.user order by id")
rows=cur.fetchall()
exp=JsonExporter(indent=2,sort_keys=False)
root=AnyNode(name="root",value=0)
list1=[root]
AnyNode()
for row in rows:
    #print(row)
    if row[4]==0:
        now_node=AnyNode(name=row[3],parent=list1[0],value=row[1])
    else :
        cur.execute("select * from public.user where uid = %s",(str(row[4]),))
        raws=cur.fetchall()
        now_node=AnyNode(name=row[3],parent=list1[raws[0][0]],value=row[1])
    list1.append(now_node)
f=open(os.path.join(really_path,"full.json"),"w")
f.write(exp.export(root))