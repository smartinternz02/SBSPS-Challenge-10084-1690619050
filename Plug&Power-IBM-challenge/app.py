from flask import Flask, render_template, request,session

app = Flask(__name__)

app.secret_key ='a'

def showall():
    sql= "SELECT * from DATA"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["ADDRESS"])
        print("The Contact is : ",  dictionary["LATITUDE"])
        print("The Password is : ",  dictionary["LONGTUDE"])
        print("The Password is : ",  dictionary["CONNECTOR"])
        dictionary = ibm_db.fetch_both(stmt)
        
        
def insertdb(conn,name,email,contact,password):
    sql= "INSERT into TABLE1 VALUES('{}','{}','{}','{}')".format(name,email,contact,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print("Number of affected rows: ", ibm_db.num_rows(stmt))

def insertdb1(conn,name,mobile,email,carno,carname,connector,date,time):
    sql= "INSERT into SLOT VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(name,mobile,email,carno,carname,connector,date,time)
    stmt = ibm_db.exec_immediate(conn, sql)
    print("Number of affected rows: ", ibm_db.num_rows(stmt))
    
    
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hjt21704;PWD=Zar2Xb7avAKgdOP7",'','')
print(conn)
print("connection successful...")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def index0():
    return render_template('index.html')

@app.route('/myslot')
def myslot():
    return render_template('myslot.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/book')
def book():
    return render_template('book.html')


@app.route('/register1', methods=['POST','GET'])
def register1():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        contact = request.form['mobile']
        password = request.form['password']
        insertdb(conn,name,email,contact,password)
    return render_template('signup.html')
        


@app.route('/be', methods=['GET', 'POST'])
def be():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        carno = request.form['carno']
        carname = request.form['carname']
        connector = request.form['connector']
        date = request.form['date']
        time = request.form['time']
        insertdb1(conn,name,mobile,email,carno,carname,connector,date,time)
        inp=[name,mobile,email,carno,carname,connector,date,time]
        return render_template('myslot.html',a=inp[0],b=inp[3],c=inp[4],d=inp[5],e=inp[6],f=inp[7])
        
    return render_template('myslot.html')
        

@app.route('/index1')
def index1():
    query = "SELECT * FROM DATA"
    stmt = ibm_db.exec_immediate(conn, query)
    results = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        results.append(row)
        row = ibm_db.fetch_assoc(stmt)

    print(results)
    return render_template('data.html', results=results)



@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sql= "select * from TABLE1 where email='{}' and password='{}'".format(email,password)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        print(userdetails)
        if userdetails:
            session['login'] =userdetails["EMAIL"]
            return render_template('index2.html',name=userdetails["NAME"],email= userdetails["EMAIL"],contact= userdetails["CONTACT"],password=userdetails["PASSWORD"])
        else:
            msg = "Incorrect Email id or Password"
            return render_template("signup.html", msg=msg)
    return render_template('index2.html')




if __name__ =='__main__':
    app.run( debug = True,port = 5000,host ='0.0.0.0')
