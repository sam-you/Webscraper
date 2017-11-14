from flask import Flask, render_template,url_for,redirect,flash,request
import requests
import lxml.html
import urllib.request
import urllib.parse
import re
import mysql.connector as mariadb
# response = requests.get('http://www.mathhelp.com/intermediate-algebra-help/')
# tree = lxml.html.fromstring(response.text)
# links = tree.xpath('//a')
# out = []
# for link in links:
#     if 'href' in link.attrib:
#         out.append(link.attrib['href'])
# result=[]
# for x in out:
# 	if x[:4]=='/how':
# 		x='www.mathhelp.com'+x
# 		result.append(x)
# 		print(x)

    
	

# open the home website
url='http://www.purplemath.com/modules/'
req=urllib.request.Request(url);
resp=urllib.request.urlopen(req).read();
#get the intermediate Aljebra topics using regular expression 
units=re.findall(r'Intermediate Algebra Topics(.*?)Advanced Algebra Topics',str(resp))
# get all the topics hyper links
li=re.findall(r'<a href="(.*?)">',str(units))
results=[]
# get the content from each topic 
for x in li :
	obj={}
	y=re.findall(r'.*?htm',str(x))[0];
	y='http://www.purplemath.com/modules/'+y;
	obj['link']=y
	r=urllib.request.Request(y);
	res=urllib.request.urlopen(r).read();
	# get the topic title 
	tiitle=re.findall(r'<title>(.*?)</title>',str(res));
	obj['title']=tiitle[0]
	results.append(obj)
#store the grapped data to the database 
connection = mariadb.connect(user='root', database='scraper')
for result in results:
	l=result['link'];
	t=result['title'];
	cursor = connection.cursor()
	cursor.execute("INSERT INTO topics (topic,link) VALUES(%s,%s)",(t,l))
	connection.commit()




	
    

app = Flask(__name__)
# login block
@app.route("/login",methods=['POST','GET'])
def login_page():
	print('inside login')
	error=None
	if request.method=='POST':
		username=request.form['username']
		password=request.form['password']
		cursor = connection.cursor()
		cursor.execute("Select * from users where username='"+username+"'")
		user=cursor.fetchone()
		print(len(user))
		if len(user) is 1:
			print('inside login')
			return redirect(url_for('main'))
		else:
			return 'faild'
	return redirect(url_for('main'))

# sign up block 
@app.route("/signup",methods=['POST','GET'])
def signup_page():
	error=None
	if request.method=='POST':
		print('inside signup')
		name=request.form['name']
		username=request.form['username']
		password=request.form['password']
		email=request.form['email']
		cursor = connection.cursor()
		cursor.execute('INSERT INTO users(name,username,password,email)VALUES(%s,%s,%s,%s)',(name,username,password,email))
		connection.commit()
	return render_template('signup.html')

	
	


# main route 

@app.route("/")
def main():
	return render_template('index.html',results=results)

if __name__ == "__main__":
   app.run(debug=True)
   