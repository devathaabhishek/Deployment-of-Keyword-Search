 

from flask import Flask, jsonify, request, render_template
import re
#import time 
import concurrent.futures

 

 
app = Flask(__name__)


def process_doc(T):
    name = T[0] 
    review_text = T[1]
    with open(name, "r") as f:#provide the link for accessing the document
        f1 = f.read()
        f5 = re.sub(r'[\(\[].*?[\)\]]', '', f1, flags=re.MULTILINE)
        f6 = re.sub(r'\s\S+:', '', f5)
        f7 = re.sub('[^A-Za-z0-9]+', ' ', f6)
        final_text = f7.lower()
        if review_text.lower() in final_text:
            return name
         
        return None
 
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index')
def index():
    return  render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    #print('Hi')
    #time.sleep(50)    
    to_predict_list = request.form.to_dict()
    review_text = to_predict_list['review_text']
    name_list = []
    for i in range(1,4):
        name = "Doc" + str(i) + ".txt"
        name_list.append([name,review_text])
    res_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        L = executor.map(process_doc, name_list)    
        for j in L:
            print(j)
            if j is not None: 
                res_list.append(j)
                
    return jsonify(res_list)

if __name__ == '__main__':    
    app.run(host='127.0.0.1', port=8080)





