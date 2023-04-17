from flask import Flask, render_template, request, redirect, send_from_directory

from flask_login import LoginManager, login_required, login_user, current_user, logout_user

import pymysql
import pymysql.cursors

login_manager = LoginManager()




app = Flask(__name__)
login_manager.init_app(app)



app.config['SECRET_KEY'] = 'something_random'

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
     cursur = connection.cursor()

     cursur.execute("SELECT * from `user` WHERE `id` =" + user_id)




     result = cursur.fetchone()

     if result is None:
          return None
     
     return User(result['ID'],result['username'],result['banned'])


@app.get('/media/<path:path>')
def send_media(path):
     return send_from_directory('media', path)

@app.route("/home")
def index():

    return render_template(
        "home.html.jinja"
        

    )

@app.route('/feed')
@login_required
def post_feed():
      
      cursor = connection.cursor()
      
      cursor.execute("SELECT * FROM `post` JOIN `user` ON `post` . `user_id` = `user`.`ID` ORDER BY `timestamp` DESC;")

      results = cursor.fetchall()

      return render_template(
        "post.html.jinja",

        posts=results
        

    )

@app.route('/post', methods= ['POST'])
@login_required
def create_post():
     cursor = connection.cursor()

     photo = request.files['uploads']

     file_name = photo.filename # my_photo.jpg

     file_extencion = file_name.split('.')[-1]

     if file_extencion in ['jpg','jpeg','png','gif']:
               photo.save('media/post' + file_name)
     else:
               raise Exception('Invalid file type')

     user_id = current_user.id

     cursor.execute("INSERT INTO `post`(`post_text`,`post_image`,`user_id`) VALUES(%s,%s,%s)", (request.form['text'], file_name, user_id))

     return redirect('/feed')







@app.route('/sign-out')
def sign_out():
     logout_user()

     return redirect('/sign-in')



@app.route('/sign-in', methods = ['POST','GET'])
def sign_in():
     if current_user.is_authenticated:
          return redirect('/feed')
     if request.method == 'POST':
          cursor = connection.cursor()

          cursor.execute(f"SELECT * FROM `user` where `username` =  '{request.form ['username']}'")

          result = cursor.fetchone()

          if result is None:
               return render_template("signin.html.jinja")
          
          if request.form['password'] == result['password']:
               user = User(result['ID'], result['username'], result['banned'])

               login_user(user)

               return redirect('/feed')

          else:
               return request.form
     elif request.method == 'GET':
          return render_template("signin.html.jinja")

@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
          #Handle Signup
          cursor = connection.cursor()

          photo = request.files['photo']

          file_name = photo.filename # my_photo.jpg

          file_extencion = file_name.split('.')[-1]

          if file_extencion in ['jpg','jpeg','png','gif']:
               photo.save('media/users' + file_name)
          else:
               raise Exception('Invalid file type')
        

          cursor.execute("""
            INSERT INTO `user`(`username`,`password`,`email`,`display_name`,`bio`,`photo`)
            VALUES(%s,%s,%s,%s,%s,%s)
          """,(request.form['username'],request.form['password'],request.form['email'],request.form['display_name'],request.form['bio'],file_name))

          return redirect('/feed')
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

@app.route('/profile/<username>')
def user_profile(username):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM `user` WHERE `username` = %s", (username))

    result = cursor.fetchone()




    return render_template("user_profile.html.jinja", user = result)


if __name__=='__main__':
     app.run(debug=True)


