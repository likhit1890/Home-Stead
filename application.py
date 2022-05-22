from flask import Flask, jsonify, render_template, url_for, request, session, redirect
import pymongo
import pickle
import json
import pickle
import numpy as np

applicatin=Flask(__name__) 
__location=None
__columns=None
__Bmodel=None

__mlocation=None
__mcolumns=None
__mmodel=None

def mumbai_prediction(Location,Area,Bedrooms):
    try:
        loc_index = __mcolumns.index(Location.lower())
    except:
        loc_index =-1

    x = np.zeros(len(__mcolumns))
    x[0] = Area
    x[1] = Bedrooms
    if loc_index >= 0:
        x[loc_index] = 1

    return round((__mmodel.predict([x])[0])/100000,2)
def mumbai_location():
    return __mlocation

def mumbai_artifacts():
    global __mcolumns
    global __mlocation

    with open("./artifacts/mumbai_columns.json",'r') as f:
        __mcolumns=json.load(f)['coloumsm']
        __mlocation=__mcolumns[3:]
    global __mmodel
    with open("./artifacts/Mumbai_model.pickle",'rb') as f:
        __mmodel= pickle.load(f)

def Banglore_prediction(location,sqrft,bath,bedrooms):
    try:
        loc_index = __columns.index(location.lower())
    except:
        loc_index =-1

    x = np.zeros(len(__columns))
    x[0] = sqrft
    x[1] = bath
    x[2] = bedrooms
    if loc_index >= 0:
        x[loc_index] = 1


    return round(__Bmodel.predict([x])[0],2)

def bangalore_location():
    return __location

def bangalore_artifacts():
    global __columns
    global __location

    with open("./artifacts/columns.json",'r') as f:
        __columns=json.load(f)['columns']
        __location=__columns[3:]
    global __Bmodel
    with open("./artifacts/Banglore_model.pickle",'rb') as f:
        __Bmodel= pickle.load(f)
    
@applicatin.route('/Bangalore_names')
def Bangalore_names():
    bangalore_artifacts()
    response=jsonify({
        'locations':bangalore_location()
    })
    return response

@applicatin.route('/mumbai_names')
def mumbai_names():
    mumbai_artifacts()
    response=jsonify({
        'm_locations':mumbai_location()
    })
    return response 
@applicatin.route('/')
def welcome():
    return render_template('fyh.html')

@applicatin.route('/area')
def area():
    return render_template('area.html')
@applicatin.route('/price')
def price():
    return render_template('price.html')
@applicatin.route('/explore1')
def explore1():
    return render_template('explore1.html')
@applicatin.route('/banglore')
def banglore():
    return render_template('Bangalore (2).html')
@applicatin.route('/mumbai')
def mumbai():
    return render_template('Bombay.html')
@applicatin.route('/sell')
def sell():
    return render_template('sell.html')
@applicatin.route('/explore')
def explore():
    return render_template ('explore.html')
@applicatin.route('/data',methods=['GET','POST'])
def data():
    name=request.form['name']
    address=request.form['address']
    city=request.form['city']
    state=request.form['state']
    pincode=request.form['pincode']
    sprice=request.form['sprice']
    old=request.form['old']
    client=pymongo.MongoClient('mongodb://localhost:27017/')
    mydb=client['mydata']
    mydatainfo=mydb.datainfo
    record={
        'name':name,
        'address':address,
        'city':city,
        'state':state,
        'pincode':pincode,
        'price':sprice,
        'years':old
    }
    mydatainfo.insert_one(record)
    return render_template('sell.html')
@applicatin.route('/buy')
def buy():
    return render_template('buy.html')

@applicatin.route('/predict',methods=['GET','POST'])
def predict():
    total_sqrft=float(request.form['Area'])
    blocation=request.form['blocation']
    bhk=int(request.form['bedroom'])
    bath=int(request.form['bathroom'])
    if (total_sqrft<=0 or bhk<=0 or bath<=0 ) :
        return render_template('Bangalore (2).html',prediction_text='Enter a valid size')
    else:
        bangalore_artifacts()
        return render_template('Bangalore (2).html',prediction_text='The predicted house price ',prediction_text2='Rs {} lakhs'.format(Banglore_prediction(blocation,total_sqrft,bath,bhk)))
@applicatin.route('/predict_mumbai',methods=['GET','POST'])
def predict_mumbai():
    total_sqrft=float(request.form['Area'])
    pmlocation=request.form['mlocation']
    bedrooms=int(request.form['bedroom'])
    mumbai_artifacts()
    return render_template('Bombay.html',Mumbai_prediction_text='The predicted house price is',Mumbai_prediction_text2=' Rs{} lakhs'.format(mumbai_prediction(pmlocation,total_sqrft,bedrooms)))
if __name__=='__main__':
    applicatin.run(debug=True)