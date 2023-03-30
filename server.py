from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import pymysql
import hashlib
import socket
import time
app = Flask(__name__)
app.secret_key = "line"

current_time = time.localtime() 
year = time.strftime("%Y", current_time)
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname) 

# Key API : AIzaSyDdJjxsRSzyYb0sUEdce9GLPZqqTOKohmw 

#------------------------------------------------------------------------ Conn DB ------------------------------------------------------------------------------------------------------------------

def connect_to_db():
    try: 
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db="final_project",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor #ดึงข้อมูล
        )
        return conn
    except Exception as e:
        print("Cannot Connect to DB!", e)
    return None


def user_Email(email):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        stmt = "SELECT * FROM tbl_user  WHERE email=%s"
        cursor.execute(stmt,(email,))
        result = cursor.fetchone()
        return result
#------------------------------------------------------------------------ Results ------------------------------------------------------------------------------------------------------------------

def lastID(user_id):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        stmt = "SELECT FORMAT(loss_budget,2) AS loss_budget FROM tbl_project WHERE user_id=%s ORDER BY project_dt DESC LIMIT 1"
        cursor.execute(stmt,(user_id))
        results = cursor.fetchone()
        return results  

#--------------------------------------------------------------------- index ✓ ------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index(): 
    if 'user' in session:
        if session['role'] == "admin": 
            return redirect(url_for('admin'))
        return redirect(url_for('history'))
    return redirect(url_for('login'))

#--------------------------------------------------------------------- logout ✓ -----------------------------------------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    session.pop('user', None)  
    return redirect(url_for('index'))


#--------------------------------------------------------------------- login ✓ -----------------------------------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
 error = None
 if 'user' in session:
    return redirect(url_for('index'))
 if request.method == "POST":
    email = request.form['inputEmail']
    pwd = request.form['inputPassword']    
    hash_password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    conn = connect_to_db()
    with conn.cursor() as cursor:
        stmt = "SELECT * FROM tbl_user WHERE email=%s AND pwd=%s"
        cursor.execute(stmt,(email,hash_password))
        rc = cursor.rowcount
        if rc > 0:
            result = cursor.fetchone()
            if email == result['email'] and hash_password == result['pwd']:
                session['user'] = result['email']  
                session['year'] = year
                stmt_role = "SELECT * FROM tbl_role WHERE role_id=%s"
                cursor.execute(stmt_role,(result['role_id']))
                result_role = cursor.fetchone()
                session['role'] = result_role['role_name']  
                
                if session['role'] == "admin":
                    #  stmt = "SELECT * FROM tbl_project t1 LEFT JOIN user t2 ON t1.user_id = t2.user_id"
                    #  cursor.execute(stmt)
                    #  return redirect(url_for('database'))
                    return redirect(url_for('admin')) 

                if session['role'] == "manager":
                    #  stmt = "SELECT * FROM tbl_project t1 LEFT JOIN user t2 ON t1.user_id = t2.user_id"
                    #  cursor.execute(stmt)
                    #  return redirect(url_for('database'))
                    return redirect(url_for('manager')) 
                # return redirect(url_for('index')) 
                
                if session['role'] == "staff":
                    #  stmt = "SELECT * FROM tbl_project t1 LEFT JOIN user t2 ON t1.user_id = t2.user_id"
                    #  cursor.execute(stmt)
                    #  return redirect(url_for('database'))
                    return redirect(url_for('staff')) 
                # return redirect(url_for('index')) 
        else:
            
            error = "⚠️ Wrong Email or Password !!"
            flash(error)
            return redirect(request.url)
 return render_template('sign_in.html', error=error)  

#--------------------------------------------------------------------- Register ✓ -------------------------------------------------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register(user = None):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if request.method == "POST" :
            fname = request.form['inputFullname']
            email = request.form['inputEmail']            
            password = request.form['inputPassword']
            Repassword = request.form['inputRePassword']
           
            if fname !='' and email !='' and password !='':                    
                stmt1 = "SELECT * FROM tbl_user WHERE email=%s"  
                cursor.execute(stmt1, (email))
                rc = cursor.rowcount
                if rc == 0:
                     if Repassword == password :
                        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                        stmt_role = "SELECT * FROM tbl_role WHERE role_name=%s"  
                        cursor.execute(stmt_role, ("staff"))
                        results_role = cursor.fetchone()
                        role_id = results_role['role_id']

                        stmt = """INSERT INTO tbl_user
                        (fname,email,pwd,line_userID,role_id)
                        VALUES
                        (%s,%s,%s,%s,%s)"""
                        cursor.execute(stmt, (fname,email,hash_password,'',role_id))
                        conn.commit()
                        flash('✔️ SingUp '+fname+' is Successful')
                        return redirect(url_for('index'))
                     else:
                        flash('⚠️ Passwords do not match !!')
                        return redirect(request.url)
                        # return redirect(url_for('register'))
                else:                  
                    flash('⚠️ Email : '+email+' already exists !!')
                    return redirect(request.url)
                    # return redirect(url_for('register'))
            else:
                flash('❌ Register is Failed !!')
                return redirect(url_for('register'))
        if 'user' in session:
            if session['role'] == "admin":
                user =  user_Email(session['user'])
                return render_template('sign_up.html',user=user)
        return render_template('sign_up.html',user=user)



# edit Profile

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            user =  user_Email(session['user'])
            if request.method == "POST" :
                userID = request.form['userID']
                fname = request.form['inputFullname']
                email = request.form['inputEmail']            
                password = request.form['inputPassword'] 
                Repassword = request.form['inputRePassword']
                if fname != "" and email != "" and password != "" and Repassword != "":
                    if Repassword != password :
                        flash("⚠️ Passwords don't match !!")
                        return render_template('edit_profile.html',user=user)
                    elif Repassword == password :
                        
                        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                        stmt1 = "UPDATE tbl_user SET fname=%s,email=%s,pwd=%s WHERE user_id=%s"
                        cursor.execute(stmt1, (fname,email,hash_password,userID))
                        conn.commit()
                        flash('✔️ Update is Complete')
                        return render_template('edit_profile.html',user=user)
                    else :
                        flash('❌ Update: '+fname+' is Faill !!')
                        return render_template('edit_profile.html',user=user)
                else :
                    flash('⚠️ Please check it completely. !!')
                    return render_template('edit_profile.html',user=user)
            return render_template('edit_profile.html',user=user)
        flash('⚠️ Please login !!')
        return redirect(url_for('index'))   
# ----------------------------------

@app.route('/admin')
def admin():
    if 'user' in session:
        user =  user_Email(session['user'])
        if session['role'] == "admin": 
            return render_template('admin.html',user=user)
    return redirect(url_for('index'))    

@app.route('/manager')
def manager():
    if 'user' in session:
        if session['role'] == "manager": 
            return render_template('manager.html')
    return redirect(url_for('index'))    


@app.route('/staff')
def staff():
    if 'user' in session:
        user =  user_Email(session['user'])
        if session['role'] == "staff": 
            return render_template('staff.html',user=user)
    return redirect(url_for('index'))    

@app.route('/add_role', methods=['GET', 'POST'])
def add_role():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        user = user_Email(session['user'])
        if request.method == "POST":
            user_id = request.form['user']
            role = request.form['role']
            stmt_role1 = "UPDATE tbl_user SET role_id = %s WHERE user_id = %s"
            cursor.execute(stmt_role1 ,(role,user_id))
            conn.commit()
            return redirect(url_for('add_role'))

        stmt_user = "SELECT * FROM tbl_user WHERE role_id>1"
        cursor.execute(stmt_user)
        results_user = cursor.fetchall()

        stmt_role = "SELECT * FROM tbl_role"
        cursor.execute(stmt_role)
        results_role = cursor.fetchall()

    return render_template('add_role.html',user=user,users=results_user,roles=results_role)

#--------------------------------------------------------------------- Show History ✓ --------------------------------------------------------------------------------------------------------
 
@app.route('/history', methods=['GET', 'POST'])
def history():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            user_id = resultUser['user_id']
            # if session['role'] == "admin": 
            #     return redirect(url_for('index'))

            stmt = "SELECT * FROM tbl_project t1 LEFT JOIN tbl_user t2 ON t1.user_id = t2.user_id WHERE t1.user_id=%s "
            cursor.execute(stmt,(user_id,))
            results = cursor.fetchall()  

            stmt_color = "SELECT * FROM loss_threshold where threshold_status=1 order by threshold_dt DESC LIMIT 1"
            cursor.execute(stmt_color)        
            results_color = cursor.fetchone()          
            return render_template('history.html',threshold=results_color, projects=results,user=resultUser)
        flash('⚠️ Please login !!') 
        return redirect(url_for('index'))    

 #--------------------------------------------------------------------- Add Project -------------------------------------------------------------------------------------------------------------

@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:        
            user =  user_Email(session['user'])
            stmt = "SELECT * FROM tbl_splitter"
            cursor.execute(stmt)        
            results = cursor.fetchall()

            stmt_olt = "SELECT * FROM olt where olt_status=1 order by olt_dt DESC LIMIT 1"
            cursor.execute(stmt_olt)        
            olt = cursor.fetchone()
            return render_template('add.html',user=user,olt=olt,splitters = results)
        flash('⚠️ Please login !!')
        return redirect(url_for('index'))
    
#--------------------------------------------------------------------- Show result ? -------------------------------------------------------------------------------------------------------------

@app.route('/results', methods=['GET', 'POST'])
def results():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            user =  user_Email(session['user'])
            last =lastID(user['user_id'])

            stmt_color = "SELECT * FROM loss_threshold where threshold_status=1 order by threshold_dt DESC LIMIT 1"
            cursor.execute(stmt_color)        
            results_color = cursor.fetchone()
            return render_template('results.html',threshold=results_color, user=user,projects=last) 
    flash('⚠️ Please login !!')
    return redirect(url_for('index'))
#--------------------------------------------------------------------------------- splitter ---------------------------------------------------------------------------------------------------------------

@app.route('/select_splitter')
def select_splitter():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            if session['role'] == "admin": 
                resultUser = user_Email(session['user'])
                stmt = "SELECT * FROM tbl_splitter"
                cursor.execute(stmt)        
                results = cursor.fetchall()
                return render_template('select_splitter.html',splitters=results,user=resultUser)
        flash('❌ Only Authorized Persons')
        return redirect(url_for('index'))
 
 
@app.route('/edit_splitter/<splt_id>', methods=['GET', 'POST'])
@app.route('/edit_splitter', methods=['GET', 'POST'])
def edit_splitter(splt_id=None):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            if session['role'] == "admin":  
                if request.method == 'POST':
                    type_splt = request.form['type']
                    value_splt = request.form['value']
                    splitter_id = request.form['splt_id']

                    stmt1 = "UPDATE tbl_splitter SET splitter_type=%s,splitter_value=%s WHERE splitter_id=%s"
                    cursor.execute(stmt1, (type_splt,value_splt,splitter_id))
                    conn.commit()
                    flash('✔️ UPDATE IS COMPLETE')
                    return redirect(url_for('select_splitter'))
        
                stmt = "SELECT * FROM tbl_splitter WHERE splitter_id=%s"
                cursor.execute(stmt,(splt_id))        
                result = cursor.fetchone()
                return render_template('edit_splitter.html',splitter=result,user=resultUser)
            else:
                flash('❌ Only Authorized Persons')
                return redirect(url_for('index'))
        flash('❌ Only Authorized Persons')
        return redirect(url_for('index'))

@app.route('/delete_splitter/<splt_id>')
def delete_splitter(splt_id):
    # resultUser = user_Email(session['user'])
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            if session['role'] == "admin": 
                stmt = "DELETE FROM tbl_splitter WHERE splitter_id=%s"
                cursor.execute(stmt, (splt_id,))
                conn.commit()
                flash('⚠️ Delete is Complete')
                return redirect(url_for('select_splitter'))
        flash('❌ Only Authorized Persons')          
        return redirect(url_for('index'))

@app.route('/add_splitter', methods=['GET', 'POST'])
def add_splitter():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            if session['role'] == "admin":  
                if request.method == 'POST':
                    type_splt = request.form['type']
                    value_splt = request.form['value']
                    stmt_s = "SELECT * FROM tbl_splitter WHERE splitter_type=%s"
                    cursor.execute(stmt_s,(type_splt))
                    rc = cursor.rowcount
                    if rc > 0:
                        flash('This type ['+ type_splt +'] of splitter already exists.!!')
                        return render_template('add_splitter.html',user=resultUser)
                        
                    else:
                        stmt = """INSERT INTO tbl_splitter (splitter_type,splitter_value) 
                        VALUES
                        (%s,%s)"""
                        cursor.execute(stmt, (type_splt,value_splt))
                        conn.commit()
                        flash("✔️ INSERT IS COMPLETE")
                        return redirect(url_for('select_splitter'))
                        
            else:
                flash('❌ Only Authorized Persons')
                return redirect(url_for('index'))
            return render_template("add_splitter.html",user=resultUser)
        flash('❌ Only Authorized Persons')          
        return redirect(url_for('index'))


# ---------------------------------------------------------  budget_threshold -----------------------------------------------------------------------------------------------------------

@app.route('/loss_threshold', methods=['GET','POST'])
def budget_threshold():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            stmt = "SELECT * FROM loss_threshold order by threshold_status=1 DESC"
            cursor.execute(stmt)        
            results = cursor.fetchall()
            return render_template('select_budget_threshold.html',threshold=results,user=resultUser)
            # return jsonify(results)
        return redirect(url_for('index'))

@app.route('/edit_threshold', methods=['GET','POST'])
def edit_threshold():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            if session['role'] =="admin":
                if request.method =="POST":
                    Threshold_id_old = request.form['threshold_id_old']
                    Success_new = request.form['Success']
                    Warning_new = request.form['Warning']
                    Danger_new  = request.form['Danger']
                    stmt_old = "UPDATE loss_threshold SET threshold_status=%s WHERE threshold_id=%s"
                    cursor.execute(stmt_old, (0,Threshold_id_old))
                    conn.commit()
                    
                    stmt_new = """INSERT INTO loss_threshold (threshold_success,threshold_warning,threshold_danger,threshold_status) 
                    VALUES
                    (%s,%s,%s,'1')"""
                    cursor.execute(stmt_new, (Success_new,Warning_new,Danger_new))
                    conn.commit()
                    flash("✔️ UPDATE IS COMPLETE")
                    return redirect(url_for('edit_threshold'))

            stmt_old = "SELECT * FROM loss_threshold where threshold_status=1 order by threshold_dt DESC LIMIT 1"
            cursor.execute(stmt_old)        
            threshold_old = cursor.fetchone()
            return render_template("edit_threshold.html",threshold_old=threshold_old,user=resultUser)
        flash('❌ Only Authorized Persons')          
        return redirect(url_for('index'))

@app.route('/threshold', methods=['GET','POST'])
def threshold():
	conn = connect_to_db()
	with conn.cursor() as cursor:
		if 'user' in session:
			resultUser = user_Email(session['user'])
			stmt_old = "SELECT * FROM loss_threshold where threshold_status=1 order by threshold_dt DESC LIMIT 1"
			cursor.execute(stmt_old)        
			threshold_old = cursor.fetchone()
			return render_template("threshold.html",threshold_old=threshold_old,user=resultUser)
	flash('⚠️ Please login !!')	
	return redirect(url_for('index'))

# --------------------------------------------------------- OLT Power -----------------------------------------------------------------------------------------------------------
@app.route('/olt_power', methods=['GET','POST'])
def olt_power():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            stmt = "SELECT * FROM olt order by olt_status=1 DESC"
            cursor.execute(stmt)        
            results = cursor.fetchall()
            return render_template('select_olt.html',olt = results,user=resultUser)
            # return jsonify(results)
        return redirect(url_for('index'))

@app.route('/edit_olt', methods=['GET','POST'])
def edit_olt():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            if session['role'] =="admin":
                if request.method =="POST":
                    olt_id_old = request.form['olt_id_old']
                    olt_power_new = request.form['power_olt']
                    stmt_old = "UPDATE olt SET olt_status='0' WHERE olt_id=%s"
                    cursor.execute(stmt_old, (olt_id_old))
                    conn.commit()
                    
                    stmt_new = """INSERT INTO olt (olt_power,olt_status) 
                    VALUES
                    (%s,'1')"""
                    cursor.execute(stmt_new, (olt_power_new))
                    conn.commit()
                    flash("✔️ UPDATE IS COMPLETE")
                    return redirect(url_for('edit_olt'))

            stmt_old = "SELECT * FROM olt where olt_status=1 order by olt_dt DESC LIMIT 1"
            cursor.execute(stmt_old)        
            olt_old = cursor.fetchone()
            return render_template("edit_olt.html",olt_old=olt_old,user=resultUser)
        flash('❌ Only Authorized Persons')          
        return redirect(url_for('index'))
#------------------------------------------------------------------- add Marker --------------------------------------------------

@app.route('/select_marker', methods=['GET','POST'])
def select_marker():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
        
            stmt = "SELECT * FROM tbl_marker t1 LEFT JOIN tbl_splitter t2 ON t1.splitter_id = t2.splitter_id "
            cursor.execute(stmt)        
            results_marker = cursor.fetchall()
            return render_template("select_marker.html",user=resultUser,markers=results_marker)
        return redirect(url_for('index'))

@app.route('/add_marker', methods=['GET','POST'])
def add_marker():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            if request.method =="POST":
                marker_name = request.form['marker_name']
                splitter_id = request.form['splt']
                lat = request.form['lat']
                lng = request.form['lng']
                stmt = """INSERT INTO tbl_marker (marker_name,lat,lng,splitter_id) 
                    VALUES
                    (%s,%s,%s,%s)"""
                cursor.execute(stmt, (marker_name,lat,lng,splitter_id))
                conn.commit()
                flash("✔️ INSERT IS COMPLETE")
                return redirect(url_for('select_marker'))

            stmt = "SELECT * FROM tbl_splitter"
            cursor.execute(stmt)        
            results_splt = cursor.fetchall()
            return render_template("add_marker.html",user=resultUser,splts=results_splt)
        return redirect(url_for('index'))

@app.route('/delete_marker/<marker_id>')
def delete_marker(marker_id):
    # resultUser = user_Email(session['user'])
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            if session['role'] == "admin": 
                stmt = "DELETE FROM tbl_marker WHERE marker_id=%s"
                cursor.execute(stmt, (marker_id,))
                # conn.commit()
                flash('⚠️ Delete is Complete')
                return redirect(url_for('select_marker'))
        flash('❌ Only Authorized Persons')          
        return redirect(url_for('index'))

@app.route('/edit_marker/<marker_id>', methods=['GET', 'POST'])
@app.route('/edit_marker', methods=['GET', 'POST'])
def edit_marker(marker_id=None):
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:
            resultUser = user_Email(session['user'])
            if session['role'] == "admin":  
                if request.method == 'POST':
                    marker_name = request.form['marker_name']
                    splitter_id = request.form['splt']
                    lat = request.form['lat']
                    lng = request.form['lng']
                    marker_id = request.form['marker_id']
                    stmt1 = "UPDATE tbl_marker SET marker_name=%s,lat=%s,lng=%s,splitter_id=%s WHERE marker_id=%s"
                    cursor.execute(stmt1, (marker_name,lat,lng,splitter_id,marker_id))
                    conn.commit()
                    flash('✔️ UPDATE IS COMPLETE')
                    return redirect(url_for('select_marker'))
        
                stmt = "SELECT * FROM tbl_marker WHERE marker_id=%s"
                cursor.execute(stmt,(marker_id))        
                result = cursor.fetchone()

                stmt_splt = "SELECT * FROM tbl_splitter"
                cursor.execute(stmt_splt)        
                results_splt = cursor.fetchall()
                return render_template('edit_marker.html',marker=result,user=resultUser,splts=results_splt)
            else:
                flash('❌ Only Authorized Persons')
                return redirect(url_for('index'))
        flash('❌ Only Authorized Persons')
        return redirect(url_for('index'))

@app.route('/add_mk')
def add_mk():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session: 
            stmt = "SELECT * FROM tbl_marker"
            cursor.execute(stmt)        
            results = cursor.fetchall()
            return jsonify(results)
        return redirect(url_for('index'))   

#------------------------------------------------------------------- Map --------------------------------------------------
        
@app.route('/map', methods=['GET', 'POST'])
def map():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session:        
            user =  user_Email(session['user'])
            stmt_olt = "SELECT * FROM olt where olt_status=1 order by olt_dt DESC LIMIT 1"
            cursor.execute(stmt_olt)        
            olt = cursor.fetchone()
            return render_template('map.html',user=user,olt=olt)
        flash('⚠️ Please login !!')
        return redirect(url_for('index'))

#-------------------------------------------------------------------   App Spliter --------------------------------------------------------------------------------------------------------------------------

@app.route('/add_splt')
def add_splt():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if 'user' in session: 
            stmt = "SELECT * FROM tbl_splitter"
            cursor.execute(stmt)        
            results = cursor.fetchall()
            return jsonify(results)
        return redirect(url_for('index'))   

#---------------------------------------------------------------------- (Test) Save and display----------------------------------------------------------------------------------------------------------

@app.route('/save', methods=['GET', 'POST'])
def save():
    conn = connect_to_db()
    with conn.cursor() as cursor:
        if request.method == "POST" :
            olt_power =  request.form['olt_power']
            project_name  = request.form['ProjectName']
            userID  = request.form['userID']
            distance  = request.form['Distance']            
            # position = request.form['poi']
            connector  = request.form['Connector']
            splice  = request.form['Splice']
            splitter = request.form['splitter_arrl']
            loss_budget  = request.form['loss_budget']
            
            stmt = """INSERT INTO tbl_project
            (project_name,user_id,olt_power,distance,connector,splice,splitter,loss_budget)
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(stmt, (project_name,userID,olt_power,distance,connector,splice,splitter,loss_budget))
            conn.commit()
            return redirect(url_for('results'))
        flash('⚠️ Please login !!')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0" ,debug=True, port=5000)