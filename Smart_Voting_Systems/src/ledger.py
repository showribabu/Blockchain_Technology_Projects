from web3 import Web3,HTTPProvider

import json


blockchain = 'http://127.0.0.1:7545'

def voting_contract(wallet):
    #1 connect to server
    web3=Web3(HTTPProvider(blockchain))
    #2 get the contract
    with open('./build/contracts/voting.json') as f:
        artifact_data= json.load(f)
        c_abi= artifact_data['abi']
        c_address=artifact_data['networks']['5777']['address']
        
    contract =web3.eth.contract(abi=c_abi,address=c_address)
    
    web3.eth.defaultAccount=wallet
    return(web3,contract)

def votecast(wallet,id):
    try:
        web3,contract=voting_contract(wallet)
        print("Ganache server connected and Contract selected")
        print('Function call')
        tx_hash=contract.functions.votecast(wallet,id).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print('After function call of contract')
        return 'You voted successfully'
    except:
        return 'you already voted'

def result(wallet):
    try:
        web3,contract=voting_contract(wallet)
        print("Ganache server connected and Contract selected")

        data = contract.functions.result().call()
        return data
    except:
        return 'Something Wrong to get results'

    
        
    
    
        