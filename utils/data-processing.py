import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def process_location(ip):
    response = requests.get(f"https://geolocation.com/{ip}").json()
    dictList = []
    for key, value in response.items():
        dictList.append([key, value])
    return dictList

def predict_occupation(a, cv, clf):
    test_name = [a]
    vector = cv.transform(test_name).toarray()
    prediction = clf.predict(vector)
    return prediction

def predict_gender(a, cv, clf):
    test_name = [a]
    vector = cv.transform(test_name).toarray()
    gender = 'FEMALE' if clf.predict(vector) == 0 else 'MALE'
    return gender
