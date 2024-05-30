from flask import Flask,render_template,request
import sqlite3
import json
import pickle

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
        conn = sqlite3.connect('contactus.db')
        cur = conn.cursor()
        cur.execute(f'''
        Insert into contact values(
                    "{name}","{email}","{country}","{state}","{message}"
        )
        ''')

        conn.commit()
        return render_template("message.html")

    else:
        return render_template('contactus.html')


@app.route('/check-price', methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        Make = request.form.get('make')
        Model = request.form.get('model')
        Year = request.form.get('year')
        KMs_Driven = request.form.get('kms_driven')
        Fuel = request.form.get('fuel')
        Registration_City = request.form.get('registration_city')
        Car_Documents = request.form.get('car_documents')
        Assembly = request.form.get('assembly')
        Transmission = request.form.get('transmission')
        print(Make,Model,Year,KMs_Driven,Fuel,Registration_City,Car_Documents,Assembly,Transmission)

        with open("encdata.json","r") as file:
            data = json.load(file)
        mkenc = int(data["Make"][Make])
        mdlenc = int(data["Model"][Model])
        flenc = int(data["Fuel"][Fuel])
        rgctenc = int(data["Registration city"][Registration_City])
        cardcdnc = int(data["Car documents"][Car_Documents])
        assenc = int(data["Assembly"][Assembly])
        trenc = int(data["Transmission"][Transmission])
        print(mkenc,mdlenc,flenc,rgctenc,cardcdnc,assenc,trenc)
        file.close()
        with open("model.pickle","rb") as model:
            mymodel = pickle.load(model)
        res = mymodel.predict([[int(Year),int(KMs_Driven),mkenc,mdlenc,flenc,rgctenc,cardcdnc,assenc,trenc]])
        print(res[0])

    else:
        return render_template('predict.html')
    
    return render_template("result.html",car_price = str(int(res[0]*0.3))+" INR")




if __name__=='__main__':
    app.run(host="0.0.0.0",port=5500)
    


