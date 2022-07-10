from flask_restful import Resource
from IA.Spam2 import train

class Main(Resource):
    def get(self):
        accuracy, y_pred, y = train(300, 105)
        spams = 0
        hams = 0
        for i in range(len(y)):
            if y[i].strip() == 'ham':
                hams +=1
            else:
                spams += 1
        return {
            'gradosDePreddicion':accuracy,
            'prediccion':y_pred,
            "spams":spams,
            'hams':hams
        }

