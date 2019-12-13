import json
import praw
import random
from flask import Flask, render_template, jsonify


def build_tree(reddit,postId):
	print('getting - ',postId)
	submission = reddit.submission(id=postId)
	c_count=submission.num_comments
	title=submission.title
	permalink=submission.permalink
	time=submission.created
	points=submission.score
	submission.comments.replace_more(limit=None)
	comment_queue = submission.comments[:]

	data=[["",postId]]
	for comment in submission.comments.list():
	    data.append([comment.parent_id.split('_')[-1],comment.id])

	return {'data':data,'link':permalink,'c_count':c_count,'title':title,'time':time,'points':points}
    
def get_pid(reddit,subr):
	print('getting r/',subr)
	submissions = reddit.subreddit(subr).hot()
	
	pref={
		0:[],
		1:[],
		2:[]
	}
	for i in submissions:
		if i.num_comments in range(200,500):
			pref[0].append(i.id)
		if i.num_comments in range(0,200):
			pref[1].append(i.id)
		if i.num_comments in range(350,5000):
			pref[2].append(i.id)

	print(pref)
	pid_list=pref[0]
	if len(pid_list)==0:
		pid_list=pref[1]
	if len(pid_list)==0:
		pid_list=pref[2]

	print('got',len(pid_list))
	return pid_list
	


def get_tree(request):

	request_json = request.get_json()
	if request.args and 'subr' in request.args:
		subr=request.args.get('subr')
	elif request_json and 'subr' in request_json:
		subr=request_json['subr']
	else:
		return "oops!"
    

	reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='zW7Pp8V-5pvw9A', client_secret="WtmRNzCOIm-armXEO_scVunHxDU")
	pid_list=get_pid(reddit,subr)
	random.shuffle(pid_list)
	return build_tree(reddit,pid_list[0])








