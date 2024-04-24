import numpy as np
import pandas as pd
from sklearn import  preprocessing
from sklearn.metrics import accuracy_score 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier



data = pd.read_csv("Datasets/Training.csv")

features = list(data.columns)
x = data.iloc[:,:-1]
y = data.iloc[:, -1]

data_test = pd.read_csv("Datasets/Testing.csv")
x_test = data_test.drop(columns=["prognosis"])
y_test = data_test[['prognosis']]

label = LabelEncoder()

label.fit(y)
y = label.transform(y)

label.fit(y_test)
y_test = label.transform(y_test)


clf = LogisticRegression(penalty = 'l2', C=0.1, max_iter=10000)
clf.fit(x,y)
y_pred_clf = clf.predict(x_test)
acc_clf = accuracy_score(y_test,y_pred_clf)

dt = DecisionTreeClassifier()
dt.fit(x,y)
y_predict_dt = dt.predict(x_test)
acc_dt = accuracy_score(y_test,y_predict_dt)


kfold = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(dt, x, y, cv=kfold)

specialists = {
    'Fungal infection': 'Dermatologist',
    'Allergy': 'Allergist',
    'GERD': 'Gastroenterologist',
    'Chronic cholestasis': 'Hepatologist',
    'Drug Reaction': 'Immunologist',
    'Peptic ulcer diseae': 'Gastroenterologist',
    'AIDS': 'Infectious Disease Specialist',
    'Diabetes ': 'Endocrinologist',
    'Gastroenteritis': 'Gastroenterologist',
    'Bronchial Asthma': 'Pulmonologist',
    'Hypertension ': 'Cardiologist',
    'Migraine': 'Neurologist',
    'Cervical spondylosis': 'Orthopedic Surgeon',
    'Paralysis (brain hemorrhage)': 'Neurologist',
    'Jaundice': 'Hepatologist',
    'Malaria': 'Infectious Disease Specialist',
    'Chicken pox': 'Pediatrician',
    'Dengue': 'Infectious Disease Specialist',
    'Typhoid': 'Infectious Disease Specialist',
    'hepatitis A': 'Hepatologist',
    'Hepatitis B': 'Hepatologist',
    'Hepatitis C': 'Hepatologist',
    'Hepatitis D': 'Hepatologist',
    'Hepatitis E': 'Hepatologist',
    'Alcoholic hepatitis': 'Hepatologist',
    'Tuberculosis': 'Pulmonologist',
    'Common Cold': 'General Practitioner',
    'Pneumonia': 'Pulmonologist',
    'Dimorphic hemmorhoids(piles)': 'General Surgeon',
    'Heart attack': 'Cardiologist',
    'Varicose veins': 'Vascular Surgeon',
    'Hypothyroidism': 'Endocrinologist',
    'Hyperthyroidism': 'Endocrinologist',
    'Hypoglycemia': 'Endocrinologist',
    'Osteoarthristis': 'Orthopedic Surgeon',
    'Arthritis': 'Rheumatologist',
    '(vertigo) Paroymsal  Positional Vertigo': 'ENT Specialist',
    'Acne': 'Dermatologist',
    'Urinary tract infection': 'Urologist',
    'Psoriasis': 'Dermatologist',
    'Impetigo': 'Dermatologist'
}

def random_forest(x,y,x_test,y_test):
    dt = RandomForestClassifier(n_estimators=2, random_state=42,max_depth=20,max_features=10)
    
    dt.fit(x,y)
    y_pred = dt.predict(x_test)
    accuracy = accuracy_score(y_test,y_pred)
    return accuracy*100
    # print("Accuracy score by decision tree: ", accuracy_score)
rf = RandomForestClassifier()
a=random_forest(x , y, x_test, y_test)


def xgb_model():
    model = XGBClassifier()
    return model
xgb = xgb_model()
xgb.fit(x,y)
y_pred_xgb = xgb.predict(x_test)
accuracy = accuracy_score(y_test, y_pred_xgb)

symptoms = x.columns.values

 
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index
 
data_dict = {
    "symptom_index":symptom_index,
    "predictions_classes":label.classes_
}
def predictDisease(symptoms):
    symptoms = symptoms.split(",")
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1
         
    input_data = np.array(input_data).reshape(1,-1)
     
    xgboost_prediction = data_dict["predictions_classes"][xgb.predict(input_data)[0]]
    specialist = specialists.get(xgboost_prediction, "General Practitioner")
    return f" {xgboost_prediction} and you should go to a {specialist}"
    # predictions = xgboost_prediction
    # return predictions

print(predictDisease("Itching"))
