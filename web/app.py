from random import randrange
from flask import Flask, render_template,request
from pyecharts import options as opts
from pyecharts.charts import Tree
import os
import json
import psycopg2
from anytree import AnyNode,RenderTree
from anytree.exporter import JsonExporter
from anytree.search import find_by_attr
from anytree.importer import DictImporter
import pymysql
import time
import queue
app = Flask(__name__, static_folder="templates")
really_path=os.path.split(os.path.realpath(__file__))[0]

#old vesion to get sub-tree of target node
'''
def old_get_json(raw_input):
    s1=time.clock()
    f=open(os.path.join(really_path,"fixtures","exp3.json"),"r",encoding="utf-8")
    e1=time.clock()
    print("get data in use:%s"%(e1-s1))
    data_json=json.load(f)
    importer=DictImporter()
    s3=time.clock()
    root=importer.import_(data_json)
    e3=time.clock()
    print("build tree use :%s"%(e3-s3))
    s2=time.clock()
    target_node=find_by_attr(root,str(raw_input))
    e2=time.clock()
    print("find node use: %s"%(e2-s2))
    exporter=JsonExporter(indent=2,sort_keys=True)
    o=open(os.path.join("fixtures","subtree"+str(raw_input)+".json"),"w",encoding="utf-8")
    print(target_node)
    o.write(exporter.export(target_node))
'''
def get_json(raw_input):
    # open full-tree json & get json in
    need=str(raw_input)
    f=open(os.path.join(really_path,"data","json","full.json"),"r",encoding='utf-8')
    data_json=json.load(f)
    # simple bfs to find target-node
    node_queue=queue.Queue()
    node_queue.put(data_json)
    while node_queue.qsize() != 0 :
        top_node=node_queue.get()
        if top_node['name']==need:
            target_node=top_node
            break
        else:
            if 'children' in top_node.keys():
                for child_node in top_node['children']:
                    node_queue.put(child_node)
    o=open(os.path.join(really_path,"data","json","subtree"+need+".json"),"w",encoding="utf-8")
    o.write(json.dumps(target_node))
#check username
def checkuser(username):
    txt=open(os.path.join(really_path,"data","name.txt"),"r",encoding='utf-8')
    fullname=txt.read()
    if fullname.find(str(username)) == -1:
        return False
    return True

@app.route("/data",methods=['GET'])
def index():
    #get_json(request.form['name'])
    raw_input=str.lower(request.args.get("name"))
    if checkuser(raw_input)==False:
        return "User illegal"
    conn=psycopg2.connect(database="npupt",user="postgres",password="root",host="localhost",port="5432")
    cur=conn.cursor()
    cur.execute("select * from public.user where lower(username) = %s",(raw_input,))
    rows=cur.fetchall()
    usernick=rows[0][3]
    return render_template("EChart.html",Nick=usernick)

@app.route("/")
def reallyindex():
    return render_template("reallyindex.html")

@app.route("/getjson",methods=['GET'])
def endjson():
    #get UserNick
    name=request.args.get("name")
    if os.path.exists(os.path.join(really_path,"data","json","subtree"+str(name)+".json"))==False:
        get_json(name)
    with open(os.path.join(really_path,"data","json","subtree"+str(name)+".json"),"r",encoding="utf-8") as f:
        j=json.load(f)
    return json.dumps(j)
if __name__ == "__main__":
    app.run(host="::",port=2086)