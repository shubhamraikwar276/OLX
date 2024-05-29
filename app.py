from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("home.html")


@app.route('/contact', methods = ["GET",'POST'])
def contactus():
    if request.method== 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")
        state = request.form.get("state")
        message = request.form.get("message")
        print(name,email,country,state,message)
    else:
        return render_template('contactus.html')




if __name__=='__main__':
    app.run()
    


