from PIL import Image
from flask import Flask,request
import base64
import io
from IA.Spam2 import escribir, train,graficar


app = Flask(__name__) 

def get_encoded_img(image_path):
    img = Image.open(image_path, mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response

@app.route('/test/<n_total>/<n_test>')
def test(n_total,n_test):
    accuracy, y_pred, y = train(int(n_total), int(n_test))
    spams = 0
    hams = 0
    accuracy = (accuracy*100)//1
    for i in range(len(y)):
        if y[i].strip() == 'ham':
            hams +=1
        else:
            spams += 1
    graficar(spams,hams)
    imagen = get_encoded_img('grap.png')
    y = y[int(n_test):]
    return {
        'gradosDePreddicion':accuracy,
        "tipo":y_pred[-1],
        'prediccion':list(y_pred),
        'png':str(imagen),
        "originals":y,
        "spams":spams,
        'hams':hams
    }

@app.route('/add',methods=['POST'])
def add():
    body = request.get_json()
    mail=None
    tag=None
    if 'mail'in body and 'tag' in body :
        mail=body['mail']
        tag=body['tag']
        escribir(mail,tag)
        return({'ok':True})
    return({'ok':False})


# if __name__== '__main__':
#     app.run()
