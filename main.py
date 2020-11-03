
from flask import Flask,render_template,request,redirect,url_for,send_file
from tinydb import TinyDB, Query
from scripts import dbops
import os
import uuid
import datetime
from dateutil.parser import parse
import pandas as pd
today= str(datetime.datetime.today()).split()[0]


BASE_DIR=os.getcwd()
if not os.path.exists(BASE_DIR+"/static/db"):
	os.mkdir(BASE_DIR+"/static/db")

app = Flask(__name__)

member_db=BASE_DIR+"/static/db/member.json"
task_db=BASE_DIR+"/static/db/task.json"

def map_member_task(member,tasks):
	members={i['name']:{"id":i["idx"],"name":i["name"],"task":[]} for i in member}
	for task in tasks:
		members[task["name"]]["task"].append(task)
	return members

@app.route('/',methods=["GET","POST"])
def hello_world():
	member=dbops.get_all(member_db)
	if request.method=="POST":
		name=request.form["name"]
		task=request.form["task"]
		idx=uuid.uuid4()
		dbops.insert(task_db,{"idx":str(idx),"name":name,"task":task,"startdate":today,"status":"Open","enddate":"-"})
	task= dbops.get_all(task_db)
	task=map_member_task(member,task)

	return render_template("index.html",member=member,task=list(task.values()))



@app.route('/member/',methods=["GET","POST"])
def member():
	if request.method=="POST":
		name=request.form["member"]
		idx=uuid.uuid4()
		dbops.insert(member_db,{"idx":str(idx),"name":name})
	data=dbops.get_all(member_db)
	return render_template("member.html",data=data)
@app.route('/status/<idx>',methods=["GET","POST"])
def status(idx):
	url=request.referrer
	task_id,stat=idx.split("@")
	if stat=="On Hold":
		dbops.update(task_db,task_id,{"status":stat})
	else:
		dbops.update(task_db,task_id,{"status":stat,"enddate":today})
	return redirect(url)


@app.route('/delete/<idx>',methods=["GET","POST"])
def delete(idx):
	url=request.referrer
	dbops.delete(task_db,idx)
	return redirect(url)


@app.route("/task/",methods=["GET","POST"])
def task():
	task= dbops.get_all(task_db)
	
	if request.method=="POST":
		
		name= request.form["name"]
		status= request.form["status"]

		startdate= request.form["startdate"]
		enddate=request.form["enddate"]
		if name!="Select Team Mate":
			task=[i for i in task if i["name"]==name]
		if status!="Select Status":
			task=[i for i in task if i["status"]==status]
		if startdate!="" and enddate!="":
			st = parse(startdate)
			et=parse(enddate)
			task=[i for i in task if parse(i["startdate"])>=st and parse(i["startdate"])<=et]
		elif startdate!="":
			st = parse(startdate)
			task=[i for i in task if parse(i["startdate"])==st ]


	task=reversed(task)
	data=dbops.get_all(member_db)
	return render_template("task.html",task=task,data=data)
@app.route("/downloads/",methods=["GET","POST"])
def download():
	task= dbops.get_all(task_db)
	tasklist=pd.DataFrame(task)
	task=tasklist.drop("idx",axis=1)
	task.to_csv("WorkAssingment.csv",index=False)
	return send_file("WorkAssingment.csv",as_attachment=True)


if __name__ =="__main__":
	app.run(host="0.0.0.0",port=8000)
