from flask import *
from flask import render_template
import pickle
#import gspread

#gc=gspread.service_account(filename='cred.json')
#sh=gc.open_by_key("1oySpvC8I4rF0-j2s8x_HRbZ3hw129CX4Hn_JPMOzDgw")
#ws=sh.sheet1

app = Flask(__name__,static_url_path='/static')


@app.route("/")
def home():
    return render_template('template.html')
    

@app.route("/predict",methods=['POST'])
def predict():
    if request.method == 'POST':
        name = request.form['cname']
        gender = request.form['gender']
        preg = int(request.form['preg'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bp'])
        skinthickness=23
        insulin=32
        weight=float(request.form['weight'])
        height=float(request.form['height'])
        BMI=weight/(height*height) #weight in KG and height in meter
        func=0.37
        age=int(request.form['age'])
        
        array=[[preg,glucose,bp,skinthickness,insulin,BMI,func,age]]
        
        print(array)
        loaded_model = pickle.load(open('finalized_model', 'rb'))
        predict=loaded_model.predict_proba(array)
        predict= predict[0][1]*100
        predict=round(predict)
        array1=[name,gender,preg,glucose,bp,skinthickness,insulin,weight,height,BMI,func,age,predict]
        print(array1)
        print(predict)
        #ws.append_row(array1) 
        
        return render_template('template.html', results = "You are at {}% risk of Diabetes".format(predict))
    
    else:
        return render_template('template.html')   





if __name__ == "__main__":
    app.run()

