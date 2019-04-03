import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import pandas as pd
from flask import Flask, render_template, redirect, url_for, jsonify
from sqlalchemy.sql import text
from flask import request


app = Flask(__name__)


@app.route("/")
# @app.route("/layout.html")
# def layout_file():

#    return render_template("layout.html")

# @app.route("/about.html")
# def about_file():

#    return render_template("about.html")

# @app.route("/prod_data")
# def prod_data():
#     import pymysql
#     pymysql.install_as_MySQLdb()
#     password = "ENTER YOUR PASSWORD"
#     string = f"mysql://root:{password}@localhost/eurotravel"
#     engine = create_engine(string)
#     conn = engine.connect()
#     dataframe = pd.read_sql('SELECT status,author,title,consumer,program,prod_type,threat,pcgs,impact,summary,datetime,serial FROM production ORDER BY datetime DESC', conn)
#     dataframe['datetime'] = dataframe['datetime'].dt.strftime('%Y-%m-%d')
#     data = dataframe.to_json(orient='values', date_format='iso')

#     return(data)

# machine learning algo. => model
# pred = mla(test_data)
    
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
        password = "ENTER YOUR PASSWORD"
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


if __name__ == "__main__":
   app.run(debug=True)