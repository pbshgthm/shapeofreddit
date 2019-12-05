import json
import praw
import random
from flask import Flask, render_template, jsonify


reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='zW7Pp8V-5pvw9A', client_secret="WtmRNzCOIm-armXEO_scVunHxDU")

app = Flask(__name__)
postId='e4ymg6'

def build_tree(postId):
	print('getting - ',postId)
	submission = reddit.submission(id=postId)
	c_count=submission.num_comments
	title=submission.title
	permalink=submission.permalink
	time=submission.created
	points=submission.score
	submission.comments.replace_more(limit=None)
	comment_queue = submission.comments[:]  # Seed with top-level

	data=[["",postId]]
	for comment in submission.comments.list():
	    data.append([comment.parent_id.split('_')[-1],comment.id])

	return {'data':data,'link':permalink,'c_count':c_count,'title':title,'time':time,'points':points}
    
def get_pid(subr):
	print('getting r/',subr)
	submissions = reddit.subreddit(subr).hot()
	
	#'''
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
	'''
	pref=[[i.id,i.num_comments] for i in submissions]
	pref.sort(key=lambda x:x[1])
	pref=[i[0] for i in pref]
	pref=pref[70:80]
	'''
	return pref

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get/<pid>')
def get_tree_p(pid):
	data=build_tree((pid))
	return jsonify({'data':data})

@app.route('/r/<subr>')
def get_tree(subr):

	pid_list=get_pid(subr)
	random.shuffle(pid_list)
	return jsonify(build_tree(pid_list[0]))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)





