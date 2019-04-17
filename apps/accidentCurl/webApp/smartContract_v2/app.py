from flask import Flask, request, render_template
from solc import compile_source
from web3 import Web3, HTTPProvider
import json

from web3.contract import ConciseContract

app = Flask(__name__)

http_provider = HTTPProvider('http://localhost:8545')
eth_provider = Web3(http_provider).eth

default_account = eth_provider.accounts[0]
transaction_details = {'from': default_account,}

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

participant = [b'Car', b'Witness', b'Police']

def accidentContract(participant , counterValue , accelerationValue):
    contract_constructor = contract_factory.constructor( participant , counterValue , accelerationValue)
    transaction_hash = contract_constructor.transact(transaction_details)
    transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
    contract_address = transaction_receipt['contractAddress']

    contract_instance = eth_provider.contract(
        abi=contract_abi,
        address=contract_address,
        ContractFactoryClass=ConciseContract,
    )
    return contract_address



DATA_FILENAME = 'accident_hashes.json'
with open(DATA_FILENAME, mode='w', encoding='utf-8') as f:
    json.dump([], f)

@app.route('/', methods=['GET' , 'POST'])
def index():
    data = request.get_json()
    if request.method == 'POST' and data :
        counterValue = data['counter']
        accelerationValue = data['acceleration']
        contract_address = accidentContract(participant , counterValue , accelerationValue)

        with open (DATA_FILENAME) as outfile:
            oldData = json.load(outfile)
            oldData.append(contract_address)
        with open (DATA_FILENAME, mode = 'w') as outfile:
            outfile.write (json.dumps(oldData))

    with open (DATA_FILENAME) as outfile:
        oldData = json.load(outfile)
    return render_template('homePage.html', hashes = oldData )


# For every contract there is a page that sets the values:


@app.route('/contract/<string:contractHash>', methods=['GET' , 'POST'])
def accidentSetter(contractHash):

    with open (DATA_FILENAME) as outfile:
        allHashes = json.load(outfile)
    if ( not contractHash in allHashes):
        return "The hash " + contractHash + " is not valid"

    contract_instance = eth_provider.contract(
        abi=contract_abi,
        address=contractHash,
        ContractFactoryClass=ConciseContract,
    )

    alert = ''
    person_name = request.form.get('person'+contractHash)

    if request.method == 'POST' and person_name:
        person_name_bytes = person_name.encode()
        try:
            contract_instance.agreeByPerson(person_name_bytes, transact=transaction_details)
        except ValueError:
            alert = f'{person_name} is not a valid person in the current accident!'

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

    return render_template('index.html', persons=persons, contractHash = contractHash , alert=alert)

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    app.run(debug=True)
