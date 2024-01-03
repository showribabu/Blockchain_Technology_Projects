from flask import Flask,request

from ledger import votecast,result

app=Flask(__name__)

@app.route('/votecast',methods=['GET'])
def votecast1():
    wallet= request.args.get('wallet')
    id=int(request.args.get('id'))
    print(wallet,id)
    response=votecast(wallet,id)
    return {'response':response}

@app.route('/result',methods=['GET'])
def result1():
    wallet= request.args.get('wallet')
    response = result(wallet)
    return {'response':response}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000,debug=True)
    
    