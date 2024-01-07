from flask import Flask, render_template, request,session
from pymongo import MongoClient

query_list=[]
app=Flask(__name__)
app.secret_key = '99009'

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blood_db']
    blood_collection = db['blood']
    print('Connected to Database')
except:
    print('Could not connect to Database')

def read_data_from_table():
    for i in blood_collection.find():
        print (i)

def read_data_for_homePage(k):
    global query_list
    query_list = blood_collection.find({"bloodgroup": k})
    return query_list

@app.route('/')
@app.route('/index')
def index():
    return (render_template('index.html'))

@app.route('/about')
def about():
    return (render_template('about.html'))

@app.route('/contact')
def contact():
    return (render_template('contact.html'))

@app.route('/register')
def register():
    return (render_template('register.html'))

@app.route('/change_details')
def change_details():
    return (render_template('change_details.html'))

@app.route('/find_blood')
def find_blood():
    return (render_template('find_donor.html'))

@app.route('/login')
def login1():
    return (render_template('login.html'))

@app.route('/logout')
def logoutfrom():
    return(render_template('index.html'))

@app.route('/hello')
def returnto():
    return(render_template('register.html'))

@app.route('/login_verify',methods=['post'])
def verify():
    name=request.form['username']
    pas=request.form['password']
    data=blood_collection.find()
    for i in data:
        if i['username']==name and i['password']==pas:
            session['u']=name
            session['w']='owner'
            student_details = blood_collection.find_one({'username': name})
            print(student_details)
            return render_template('display.html', donordetails=student_details)

    return render_template('login.html',res='invalid user or password')


    
    
@app.route('/homeblood',methods=['GET'])
def home_blood():
    blood_request_type=request.args.get('bloodgroup')
    print(blood_request_type)
    rows=read_data_for_homePage(blood_request_type)
    print(rows)
    query_list=[]
    return (render_template('find_blood.html',rows=rows))

@app.route('/passdb',methods=['POST'])
def pass_db():
    username=request.form['username']
    password=request.form['password']
    fullname=request.form['fullname']
    dob=request.form['dob']
    gender=request.form['gender']
    bloodgroup=request.form['bloodgroup']
    mobile=request.form['mobile']
    email=request.form['email']
    town=request.form['town']
    state=request.form['state']
    print(username,password,fullname,dob,gender,bloodgroup,mobile,email,town,state)
    blood_collection.insert_one({
        "username": username,
        "password": password,
        "name": fullname,
        "dob": dob,
        "gender": gender,
        "bloodgroup": bloodgroup,
        "pno": mobile,
        "email": email,
        "town": town,
        "city": state
    })
    print ('Registered into the Collection')
    return (render_template('register.html',resultCode='Stored Successfully'))

if __name__=="__main__":
    app.run(debug=True)