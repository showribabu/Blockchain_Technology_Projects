from flask import Flask,request,redirect,render_template,session

# for files...

from werkzeug.utils import secure_filename

#for ganache..
from web3 import Web3,HTTPProvider
import json

# for Ipfs
import ipfsapi
import os

app= Flask(__name__)
app.secret_key ='showri'

#for the files...
app.config['uploads']='uploads'

#for the  Smart contract connection..
def connect_with_register(wallet):
    web3= Web3(HTTPProvider('http://127.0.0.1:7545'))
    print('connect to Blockchain server')
    with open('./build/contracts/register.json') as f:
        artifact_register= json.load(f)
        abi= artifact_register['abi']
        address= artifact_register['networks']['5777']['address']
    contract = web3.eth.contract(abi=abi,address=address)
    print('Contract selected')
    if wallet==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet
    print('Account selected')
    
    return (web3,contract)
    
def connect_with_file(wallet):
    web3= Web3(HTTPProvider('http://127.0.0.1:7545'))
    print('connect to Blockchain server')
    with open('./build/contracts/file.json') as f:
        artifact_file= json.load(f)
        abi= artifact_file['abi']
        address= artifact_file['networks']['5777']['address']
    contract = web3.eth.contract(abi=abi,address=address)
    if wallet==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet
    print('Account selected')
    return (web3,contract)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboardPage():
    data=[]
    web3,contract=connect_with_file(0)
    _owners,_files=contract.functions.viewfiles().call()
    for i in range(len(_owners)):
        if _owners[i]==session['username']:
            dummy=[]
            dummy.append(_files[i])
            data.append(dummy)
    print(data)
    l=len(data)
    return render_template('dashboard.html',num=l,data=data)


#here we need to logout also..
@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/login')


#register
@app.route('/indexdata',methods=['POST'])
def indexdata():
    username= request.form['username']
    password= request.form['password']
    print(username,password)
    try:
        web3,contract= connect_with_register(0)
        tx_hash= contract.functions.signup(username,int(password)).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('index.html',res='Register success')
    except:
        return render_template('index.html',err='Already have Account')  

# login...  
@app.route('/logindata',methods=['POSt'])
def logindata():
    username1= request.form['username1']
    password1= request.form['password1']
    print(username1,password1)
    try:
        web3,contract= connect_with_register(0)
        response=contract.functions.login(username1,int(password1)).call()
        if response==True:
            session['username']=username1
            return redirect('/dashboard')
        else:
            return render_template('login.html',err='Login failed')
    except:
        return render_template('login.html',err='Dont have account')

#filedata...

@app.route('/uploadfile',methods=['POST'])
def uploadfile():
    choosefile= request.files['chooseFile']
    doc= secure_filename(choosefile.filename)
    print(doc)
    #save into local folder
    choosefile.save('./src/'+app.config['uploads']+'/'+ doc)
    print('File saved locally')
    # choosefile.save(os.path.join(app.config['uploads'],doc))  -> this executed if we are at 'src' folder   
    # #upload the doc into ipfs.
    client = ipfsapi.Client('127.0.0.1',5001)
    response= client.add('./src/'+app.config['uploads']+'/'+doc)
    print(response)
    filehash= response['Hash']
    print('Files hash:',filehash)
    try:
        web3,contract= connect_with_file(0)
        print('try')
        print(session['username'])
        #here we use the session for the owner who uploads the file 
        tx_hash= contract.functions.uploadfile(session['username'],filehash).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
    except:
        print('file already existed') 
    return redirect('/dashboard')
      
    
    
# @app.route('/uploadfile',methods=['post'])
# def uploadfile():
#     chooseFile=request.files['chooseFile']
#     doc=secure_filename(chooseFile.filename)
#     chooseFile.save(app.config['uploads']+'/'+doc)
#     client=ipfsapi.Client('127.0.0.1',5001)
#     response=client.add(app.config['uploads']+'/'+doc)
#     filehash=response['Hash']
#     print(filehash)
#     contract,web3=connect_with_file(0)
#     tx_hash=contract.functions.uploadFile(session['username'],filehash).transact()
#     web3.eth.waitForTransactionReceipt(tx_hash)
#     return redirect('/dashboard')

    
    

if __name__=='__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)
    
    

