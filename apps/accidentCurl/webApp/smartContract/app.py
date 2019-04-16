from flask import Flask, request, render_template
from solc import compile_source
from web3 import Web3, HTTPProvider

from web3.contract import ConciseContract

app = Flask(__name__)

PERSONS = [b'Driver1', b'Driver2', b'Police']

http_provider = HTTPProvider('http://localhost:8545')
eth_provider = Web3(http_provider).eth

default_account = eth_provider.accounts[0]
transaction_details = {
    'from': default_account,
}

with open('accident.sol') as file:
    source_code = file.readlines()

compiled_code = compile_source(''.join(source_code))
contract_name = 'accident'
contract_bytecode = compiled_code[f'<stdin>:{contract_name}']['bin']
contract_abi = compiled_code[f'<stdin>:{contract_name}']['abi']
contract_factory = eth_provider.contract(
    abi=contract_abi,
    bytecode=contract_bytecode,
)

contract_constructor = contract_factory.constructor(PERSONS)

transaction_hash = contract_constructor.transact(transaction_details)
transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
contract_address = transaction_receipt['contractAddress']

contract_instance = eth_provider.contract(
    abi=contract_abi,
    address=contract_address,
    ContractFactoryClass=ConciseContract,
)

print(contract_address)


@app.route('/', methods=['GET' , 'POST'])
def index():
    # if (request.method == 'POST'):
    # data = request.get_json()
    data = {'counter' : 0 , 'acceleration' : 1}
    contract_instance.setInfo (data['counter'] , data['acceleration'] )
    alert = ''

    person_name = request.form.get('person')

    if request.method == 'POST' and person_name:
        person_name_bytes = person_name.encode()
        try:
            contract_instance.agreeByPerson(person_name_bytes, transact=transaction_details)
        except ValueError:
            alert = f'{person_name} is not a voting option!'

    person_names = contract_instance.getPersonList()
    persons = {}

    for person_name in person_names:
        note_for_person = contract_instance.notesFor(person_name)
        person_name_string = person_name.decode().rstrip('\x00')
        persons[person_name_string] = note_for_person

    if contract_instance.isFinalised():
        persons['Finalised'] = "YES"
    else:
        persons['Finalised'] = "NO"

    return render_template('index.html', persons=persons, alert=alert)


if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    app.run(debug=True)
