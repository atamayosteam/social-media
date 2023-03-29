from flask import Flask, render_template, request
import pymysql
import pymysql.cursors




app = Flask(__name__)


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

@app.route('/signin')
def sign_in():
     return render_template("signin.html.jinja")

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
          #Handle Signup
          cursur = connection.cursor()

          cursur.execute("""
            INSERT INTO `user`(`username`,`password`,`email`,`display_name`,`bio`,`photo`)
            VALUES(%s,%s,%s,%s,%s,%s)
          """)

          return request.form
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


