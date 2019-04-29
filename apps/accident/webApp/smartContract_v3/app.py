from flask import Flask, request, render_template , jsonify
from solc import compile_source
from web3 import Web3, HTTPProvider
import json

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.models import AjaxDataSource









from web3.contract import ConciseContract

app = Flask(__name__ , static_url_path='/static')

http_provider = HTTPProvider('http://localhost:8545')
eth_provider = Web3(http_provider).eth

default_account = eth_provider.accounts[0]
transaction_details = {'from': default_account,}

# # For knowing how much money is left from this account, we should try as follows:
# balance = eth_provider.getBalance(default_account)
# Web3.fromWei(balance , 'ether')
# # The gives for example an outcome of form Decimal('99.85705776')


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






def AppendOnFile ( fileName , dataToAppend ) :
    with open (fileName) as outfile:
        oldData = json.load(outfile)
        oldData.append(dataToAppend)
    with open (fileName, mode = 'w') as outfile:
        outfile.write (json.dumps(oldData[-60:]))


DATA_FILENAME_HASHES = 'accident_hashes.json'
with open(DATA_FILENAME_HASHES, mode='w', encoding='utf-8') as f:
    json.dump([], f)

DATA_FILENAME_ACCEL = 'accelerations.json'
with open(DATA_FILENAME_ACCEL, mode='w', encoding='utf-8') as f:
    json.dump([], f)







@app.route('/', methods=['GET' , 'POST'])
def index():
    data = request.get_json()
    if request.method == 'POST' and data :
        counterValue = data['counter']
        accelerationValue = data['acc']
        accX = data['accX']
        accY = data['accY']
        accZ = data['accZ']
        a = (accX**2 + accY**2 + accZ**2)**(0.5)
        jsonToAppend = { 'counter' : counterValue , 'accX' : accX , 'accY' : accY , 'accZ' : accZ}
        # jsonToAppend = a
        AppendOnFile ( DATA_FILENAME_ACCEL , jsonToAppend )

        if a>25000:
            contract_address = accidentContract(participant , counterValue , accelerationValue)
            AppendOnFile ( DATA_FILENAME_HASHES , contract_address )

    with open (DATA_FILENAME_HASHES) as outfile:
        hashes = json.load(outfile)
    isFinalisedList = {}

    for hash in hashes :
        contract_instance = eth_provider.contract(
            abi=contract_abi,
            address=hash,
            ContractFactoryClass=ConciseContract,
        )

        if contract_instance.isFinalised():
            isFinalisedList[hash] = "YES"
        else:
            isFinalisedList[hash] = "NO"

    return render_template('index.html', hashes = hashes , isFinalisedList = isFinalisedList )








# Plotting part

@app.route('/fig', methods=['GET'])
def myPlot():

    with open (DATA_FILENAME_ACCEL) as outfile:
        data = json.load(outfile)[-60:]

    accXdata = [ {'t' : i , 'accX' : data[i]['accX'] } for i in range( len(data)) ]
    accYdata = [ {'t' : i , 'accY' : data[i]['accY'] } for i in range( len(data)) ]
    accZdata = [ {'t' : i , 'accZ' : data[i]['accZ'] } for i in range( len(data)) ]

    return render_template('plot.html' , accXdata = accXdata , accYdata = accYdata , accZdata = accZdata)

# For every contract there is a page that sets the values:


@app.route('/contract/<string:contractHash>', methods=['GET' , 'POST'])
def accidentSetter(contractHash):

    with open (DATA_FILENAME_HASHES) as outfile:
        allHashes = json.load(outfile)
    if ( not contractHash in allHashes):
        return "The hash " + contractHash + " is not valid"


    contract_instance = eth_provider.contract(
        abi=contract_abi,
        address=contractHash,
        ContractFactoryClass=ConciseContract,
    )

    latitude = contract_instance.getLatitude()
    longitude = contract_instance.getLongitude()

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
        isFinalised = "YES"
    else:
        isFinalised = "NO"

    return render_template('accident.html', persons=persons, contractHash = contractHash , isFinalised = isFinalised , alert=alert)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    app.run(debug=True)
