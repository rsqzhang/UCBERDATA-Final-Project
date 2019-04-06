import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pandas as pd
from flask import Flask, render_template, redirect, url_for, jsonify
from sqlalchemy.sql import text
from flask import request
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import json as json
import pickle

app = Flask(__name__)


@app.route("/")
def home_file():

   return render_template("index.html")

@app.route("/map.html")
def layout_file():

   return render_template("map.html")

@app.route("/sunburst-vue.html")
def sunburst():
    return render_template("sunburst-vue.html")




@app.route("/index.html", methods=['GET','POST'])
def survey_file():
    if request.method == 'POST':
        print('entering flask post mthd route')
        age = request.form['age']
        state = request.form['state']
        gender = request.form['gender']
        # country = pred(age, state, gender)
        import pymysql
        pymysql.install_as_MySQLdb()
        password = "YourPasswordHere"
        string = f"mysql://root:{password}@localhost/eurotravel"
        engine = create_engine(string)
        conn = engine.connect()
        with engine.connect() as con:
            #data = ({"first_name": fname, "last_name": lname},)
            data = ({"age": age,
                    "state": state,
                    "gender": gender
                    },)
            statement = text("""INSERT INTO answers(age,state,gender)VALUES(:age,:state,:gender)""")
            for line in data:
                con.execute(statement, **line)
        return render_template("index.html")
    return render_template("index.html")

@app.route("/map.html")
def prod_data():
    import pymysql
    pymysql.install_as_MySQLdb()
    password = "YourPasswordHere"
    string = f"mysql://root:{password}@localhost/eurotravel"
    engine = create_engine(string)
    conn = engine.connect()
    dataframe = pd.read_sql('SELECT age,state,gender FROM eurotravel', conn)
    data = dataframe.to_dict()
    user_input_json=data
    filename = 'rf.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    x_header = ['Age','M','F','Illinois','California','New York','Wisconsin','Alabama','Ohio','North Carolina','Florida','Kansas','Missouri','Oregon','Texas','Nevada','Louisiana','District of Columbia','Maryland','Oklahoma','Indiana','Colorado','Washington','Utah','Minnesota','Michigan','Georgia','Connecticut','Arizona','Mississippi','Virginia','Kentucky','Pennsylvania','Massachusetts','New Jersey','West Virginia','South Carolina','Idaho','New Mexico','Maine','Hawaii','Vermont','Arkansas','New Hampshire','Tennessee','Alaska','Nebraska','Delaware','Iowa','Rhode Island','South Dakota','Montana']
    stateList = ['Illinois','California','New York','Wisconsin','Alabama','Ohio','North Carolina','Florida','Kansas','Missouri','Oregon','Texas','Nevada','Louisiana','District of Columbia','Maryland','Oklahoma','Indiana','Colorado','Washington','Utah','Minnesota','Michigan','Georgia','Connecticut','Arizona','Mississippi','Virginia','Kentucky','Pennsylvania','Massachusetts','New Jersey','West Virginia','South Carolina','Idaho','New Mexico','Maine','Hawaii','Vermont','Arkansas','New Hampshire','Tennessee','Alaska','Nebraska','Delaware','Iowa','Rhode Island','South Dakota','Montana']
    genderList = ['M','F']
    newDict = dict()
    newDict['Age'] = [0]
    for gender in genderList:
        newDict[gender] = [0]
    for state in stateList:
        newDict[state] = [0]
    # with open('user_input.json') as user_input:
    # user_input_json = json.load(user_input)
    newDict["Age"] = [user_input_json["Age"]]
    newDict[user_input_json['gender']] = [1]
    newDict[user_input_json['state']] = [1]
    x_to_predict = pd.DataFrame(newDict)
    y_predict = loaded_model.predict(x_to_predict)
    print("my prediction is "+ y_predict[0], file=sys.stderr)
    return render_template("map.html", modelprediction = y_predict[0])
    
@app.route("/answer")
def what():
    import pymysql
    pymysql.install_as_MySQLdb()
    password = "YourPasswordHere"
    string = f"mysql://root:{password}@localhost/eurotravel"
    engine = create_engine(string)
    conn = engine.connect()
    dataframe = pd.read_sql('SELECT age,gender,state FROM answers', conn)
    data_frame_result = dataframe.iloc[-1,:]
    # data_frame_result = data_frame_result.to_json()
    data_frame_result = data_frame_result.to_json("user_input.json")
    # json.dump(data_frame_result,)
    # data_frame_result= json.dumps(data_frame_result)
    filename = 'rf.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    x_header = ['Age','M','F','Illinois','California','New York','Wisconsin','Alabama','Ohio','North Carolina','Florida','Kansas','Missouri','Oregon','Texas','Nevada','Louisiana','District of Columbia','Maryland','Oklahoma','Indiana','Colorado','Washington','Utah','Minnesota','Michigan','Georgia','Connecticut','Arizona','Mississippi','Virginia','Kentucky','Pennsylvania','Massachusetts','New Jersey','West Virginia','South Carolina','Idaho','New Mexico','Maine','Hawaii','Vermont','Arkansas','New Hampshire','Tennessee','Alaska','Nebraska','Delaware','Iowa','Rhode Island','South Dakota','Montana']
    stateList = ['Illinois','California','New York','Wisconsin','Alabama','Ohio','North Carolina','Florida','Kansas','Missouri','Oregon','Texas','Nevada','Louisiana','District of Columbia','Maryland','Oklahoma','Indiana','Colorado','Washington','Utah','Minnesota','Michigan','Georgia','Connecticut','Arizona','Mississippi','Virginia','Kentucky','Pennsylvania','Massachusetts','New Jersey','West Virginia','South Carolina','Idaho','New Mexico','Maine','Hawaii','Vermont','Arkansas','New Hampshire','Tennessee','Alaska','Nebraska','Delaware','Iowa','Rhode Island','South Dakota','Montana']
    genderList = ['male','female']
    newDict = dict()
    newDict['Age'] = [0]
    for gender in genderList:
        newDict[gender] = [0]
    for state in stateList:
        newDict[state] = [0]
    with open('user_input.json') as user_input:
        user_input_json=json.load(user_input)


    newDict["Age"] = [user_input_json["age"]]
    newDict[user_input_json['gender']] = [1]
    newDict[user_input_json['state']] = [1]
    x_to_predict = pd.DataFrame(newDict)
    show_x_to_predict = x_to_predict.to_html()
    y_predict = loaded_model.predict(x_to_predict)
    return y_predict[0]
    # return show_x_to_predict    

# machine learning algo. => model
# pred = mla(test_data)
    
if __name__ == "__main__":
   app.run(debug=True)