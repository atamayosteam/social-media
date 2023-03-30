from flask import Flask, render_template, request, redirect

from flask_login import loginManager

import pymysql
import pymysql.cursors

login_manager = loginManager()




app = Flask(__name__)
login_manager.init_app(app)

class User:
    def __init__(self, id, username, banned):
          self.is_authenticated = True
          self.is_anonymous = False
          self.is_active = not banned


          self.username = username
          self.id = id

    def get_id(self):
     return str(self.id)
    

@login_manager.user_loader
def user_loader(user_id):
     cursur = connection.cursur()

     cursur.execute("SELECT * from `user` WHERE `id` =" + user_id)




     result = cursur.fetchone()

     if result is None:
          return None
     
     return User(result['id'],result['username'],result['banned'])




@app.route("/home")
def index():

    return render_template(
        "home.html.jinja"
        

    )

@app.route('/post')
def post_feed():
      
      cursor = connection.cursor()
      
      cursor.execute("SELECT * FROM `post` JOIN `user` ON `post` . `user_id` = `user`.`ID` ORDER BY `timestamp` DESC;")

      results = cursor.fetchall()

      return render_template(
        "post.html.jinja",

        posts=results
        

    )

@app.route('/sign-in')
def sign_in():
     return render_template("signin.html.jinja")

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
          #Handle Signup
          cursur = connection.cursor()

          photo = request.files['photo']

          file_name = photo.filename # my_photo.jpg

          file_extencion = file_name.split('.')[-1]

          if file_extencion in ['jpg','jpeg','png','gif']:
               photo.save('media/users' + file_name)
          else:
               raise Exception('Invalid file type')
        

          cursur.execute("""
            INSERT INTO `user`(`username`,`password`,`email`,`display_name`,`bio`,`photo`)
            VALUES(%s,%s,%s,%s,%s,%s)
          """,(request.form['username'],request.form['password'],request.form['email'],request.form['display_name'],request.form['bio'],file_name))

          return redirect('/post')
    elif request.method == 'GET':
        return render_template("signup.html.jinja")

connection = pymysql.connect(
    host = "10.100.33.60",
    user = "atamayo",
    password = "220886964",
    database= "atamayo_socialmedia",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit = True
)
if __name__=='__main__':
     app.run(debug=True)


