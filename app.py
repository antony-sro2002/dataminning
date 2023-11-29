import pandas as pd
from flask import Flask, render_template, request, jsonify
import csv
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__, template_folder='views',static_folder='static')
@app.route('/')
def index():
    data = []
    headers = []
    with open('static/assets/tables/resultados_modelos.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # Lee la primera fila como encabezados
        for row in csvreader:
            # Redondear valores decimales a 3 decimales
            rounded_row = [f'{float(value):.3f}' if '.' in value else value for value in row]
            data.append(rounded_row)
    return render_template('index.html', headers=headers, data=data)

@app.route('/index', methods=['POST'])
def cliente():
    # Obtener los datos enviados por el formulario
    age=int(request.form['age'])
    job=request.form['job']
    marital=request.form['marital']
    education =request.form['education']
    default  =(request.form['default'])
    housing   =(request.form['housing'])
    loan     =(request.form['loan'])
    contact   =(request.form['contact'])    
    month    =(request.form['month'])
    day_of_week  =(request.form['day_of_week']) 
    duration  =int(request.form['duration'])    
    campaign =int(request.form['campaign'])   
    pdays =int(request.form['pdays'])              
    previous  =int(request.form['previous'])        
    poutcome  =(request.form['poutcome'])      
    emp_var_rate  =float(request.form['emp.var.rate']) 
    cons_price_idx =float(request.form['cons.price.idx']) 
    cons_conf_idx =float(request.form['cons.conf.idx'])    
    euribor3m  =float(request.form['euribor3m'])     
    nr_employed =float(request.form['nr.employed'])       
    # arreglo de la data
    data = [age, job, marital, education, default, housing, loan, contact,
        month, day_of_week, duration, campaign, pdays, previous, poutcome,
        emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed]
    print(data)     
    # Evaluamos mediane las reglas
    result= evaluar(age, job, marital, education, default, housing, loan, contact,
        month, day_of_week, duration, campaign, pdays, previous, poutcome,
        emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed)
    
    if result == 1:
        result = "Yes"
    elif result == 0:
        result = "No"
    #Devolver una respuesta
    return jsonify({'mensaje': result})

def evaluar(age, job, marital, education, default, housing, loan, contact,
        month, day_of_week, duration, campaign, pdays, previous, poutcome,
        emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed):
    data = [age, job, marital, education, default, housing, loan, contact,
        month, day_of_week, duration, campaign, pdays, previous, poutcome,
        emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m, nr_employed]

    columns = ['age', 'job', 'marital', 'education', 'default', 'housing', 'loan', 'contact',
            'month', 'day_of_week', 'duration', 'campaign', 'pdays', 'previous', 'poutcome',
            'emp_var_rate', 'cons_price_idx', 'cons_conf_idx', 'euribor3m', 'nr_employed']

    form_data = pd.DataFrame([data], columns=columns)

    # Codificar y normalizar los datos del formulario
    # Aplicar la misma codificación que se usó en el conjunto de entrenamiento
    label_encoder = LabelEncoder()
    scaler = StandardScaler()
    # Codificar las variables categóricas
    for column in ['job', 'marital', 'contact', 'education', 'month', 'day_of_week', 'poutcome', 'default', 'housing', 'loan']:
        form_data[column] = label_encoder.fit_transform(form_data[column])

    # Normalizar las características numéricas
    numeric_columns = form_data.columns[:-1]  # Excluyendo la última columna ('subscribed')
    form_data[numeric_columns] = scaler.fit_transform(form_data[numeric_columns])

    # Cargar el modelo entrenado
    lda = joblib.load('modelo_lda.joblib')

    # Hacer predicciones con el modelo entrenado usando los datos del formulario
    predictions = lda.predict(form_data)
    # Las predicciones contendrán el resultado de tu modelo para los datos del formulario
    return predictions

if __name__== '__main__':
    app.run(debug=True, port=1234)