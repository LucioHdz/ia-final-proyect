from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from IA.Parser import Parser
from pymongo import MongoClient as client
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


DATASET_PATH = "datasets/trec07p"

# sirve para conectarse a mongodb y obtener la colecion de la base de datos


def get_database_collection(collection=True):
    if collection:
        clientdb = client('mongodb://localhost:27017/')
        db = clientdb.test_database
        db = clientdb['machine_learning']
        return db.mails
    else:
        clientdb = client('mongodb+srv://lucioVero:mbf8jss17c@cluster0.yijke.mongodb.net/?retryWrites=true&w=majority')
        db = clientdb['machine_learning']
        col = db['processed']
        return col
        # clientdb = client('mongodb://localhost:27017/')
        # db = clientdb.test_database
        # db = clientdb['machine_learning']
        # return db.processed


def get_indexes(collection, n_elements):
    X = []
    y = []
    if (n_elements == 75180):
        elements = collection.find()
    else:
        elements = collection.find(limit=n_elements)
    for element in elements:
        X.append(element['mail'])
        y.append(element['type'])
    if n_elements != 75180:
        e = collection.find(limit=-1)[0]
        X.append(e['mail'])
        y.append(e['type'])
    return X, y


def create_prep_dataset(db, n_elements):
    X = []
    y = []
    x_data, y_data = get_indexes(db, n_elements)
    for i in range(len(x_data)):
        print("\rParsing email: {0}".format(i+1), end='')
        X.append(" ".join(x_data[i]['subject']) + " ".join(x_data[i]['body']))
        y.append(y_data[i])
    return X, y


def parse_email(index):
    p = Parser()
    pmail = p.parse(index["mail"])
    print(pmail)
    return pmail, index["label"]


def create_trains(n):
    db = get_database_collection(collection=False)
    x_train, y_train = create_prep_dataset(db, n)
    return x_train, y_train


def vectorizer_data(X_train, vectorizerC=None):
    if vectorizerC == None:
        vectorizer = CountVectorizer()
    else:
        vectorizer = vectorizerC
    X_train = vectorizer.fit_transform(X_train)
    return X_train, vectorizer


def train_with_LogReg(x, y):
    clf = LogisticRegression(max_iter=300000)
    clf.fit(x, y)
    return clf


def train_IA(x, y, vectorizer):
    x = vectorizer.fit_transform(x)
    clf = train_with_LogReg(x, y)
    return clf


def predict(x, clf):
    y_pred = clf.predict(x)
    return y_pred


def train(n_data=75180, n_trains=0):
    if n_trains == 0:
        n_trains = 3000
    X, y = create_trains(n_data)
    X_train, y_train = X[:n_trains], y[:n_trains]
    X_test, y_test = X[n_trains:], y[n_trains:]

    vectorizer = CountVectorizer()
    clf = train_IA(X_train, y_train, vectorizer)
    X_test = vectorizer.transform(X_test)
    y_pred = predict(X_test, clf)
    return accuracy_score(y_test, y_pred), y_pred, y


def parse_index(db, label, mail):
    obj = {"label": label, "mail": mail}
    e_mail, label_e = parse_email(obj)
    db.insert_one({
        "type": label_e,
        "mail": e_mail
    })


def graficar(spams,hams):
    correos = [spams,hams]
    tags = ['spam','ham']
    plt.pie(correos, labels=tags, autopct="%0.1f %%")
    plt.axis("equal")
    plt.savefig("grap.png")
    plt.clf()
    plt.cla()
    plt.close()

def test():
    accuracy, y_pred, y = train(300, 105)
    print("\naccuracy: ", accuracy)
    print("\n\n\ny_pred: ", y_pred[-1])
    spams = 0
    hams = 0
    for i in range(len(y)):
        # print(str(y[i]) == "ham")
        # print(str(y[i]) == 'spam')
        if y[i].strip() == 'ham':
            hams +=1
        else:
            spams += 1
    print('No. spams: {}\nNo. hams: {}'.format(spams, hams))
    graficar(spams,hams)


def escribir(mail,tag):
    db =  get_database_collection(collection=False)
    email,label = parse_email({'label':tag,'mail':mail})
    db.insert_one({"type":label, 'mail':email})


if __name__== '__main__':
    test()
