import webbrowser

# from datetime import datetime
import logging
import gc
import sys
import os
try:
    from flask import Flask ,render_template,request, jsonify,send_file
    import pandas as pd
except:
    # os.system('pip install flask')
    os.system('pip install -r .//requirements.txt')
import toolkit as tk
# from flask import Flask ,render_template,request, jsonify,send_file
# import pandas as pd

# -------------------------------
# THIS SECTION FOR DISALBE console output

# logging.basicConfig(filename=tk.STD_PATH+"std.log", format='%(asctime)s %(message)s' ) 
# logger=logging.getLogger() 
# logger.setLevel(logging.DEBUG) 
# class runSingle:
#     def __init__(self, fileName) -> None:
#         self.f = open(fileName, "w")
#         self.f.close()
#         try:
#             os.remove(fileName)
#             self.f = open(fileName, "w")
#         except WindowsError:
#             sys.exit()
# a = runSingle(tk.STD_PATH+"A")

#----------------------------------------------------- 

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')
@app.route('/login',methods=['POST','GET'])
def hello2():
    k=request.get_json()['data']
    output=tk.get_matching_list(k['d1'],k['d2'])
    # print('this is text',type(k),k,output)
    return jsonify({"data":output})
@app.route('/handle',methods=['POST','GET'])
def hello3():
    gc.collect()
    k=request.get_json()['data']
    try:
        k=tk.direct_function(k['function'],k['data'])
    except Exception as Argument:
        logging.exception(Argument)
        sys.exit()
    
    gc.collect()
    return jsonify({"data":k})
@app.route('/setting')
def hello4():
   
    
    if tk.get_gen('LOGIN'):
        return render_template('setting.html')
    else:
        return render_template('login.html')
@app.route('/entry_page',methods=['POST','GET'])
def hello5():
    return render_template('entry.html')
@app.route('/report',methods=['POST','GET'])
def hello6():
    return render_template('report.html')
@app.route('/home',methods=['POST','GET'])
def hello7():
    return render_template('home.html')
@app.route('/template',methods=['POST','GET'])
def hello8():
    return render_template('template.html')
@app.route('/down_load',methods=['POST','GET'])
def hello9():
    k=request.get_json()['data']
    return send_file(k,as_attachment=True)
@app.route('/upload',methods=['POST','GET'])
def hello10():
    if request.method == 'POST':
        k=request.files
        c=k[list(k.keys())[0]]
        c.save(tk.STD_PATH+'temp.csv')
        return jsonify({"action":"success"})
if __name__=="__main__":
    # p = multiprocessing.Process(target=x, args=[])
    url = 'http://127.0.0.1:5000'
    br="C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
    # br="C://Program Files//Google//Chrome//Application//chrome.exe"
    webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser(br))
    webbrowser.get('chrome').open(url)
    # app.run(debug=False,threaded=False)
    # app.run(host='192.168.213.140', port=8000, debug=True, threaded=False)
    app.run(debug=True,threaded='False')






