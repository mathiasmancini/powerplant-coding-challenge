import json
import numpy as np

from flask import Flask, request, jsonify

################ FLASK ##################

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/productionplan', endpoint='productionplan', methods=['POST'])
def productionplan():
    payload = request.get_json()
    response = power_distribution(payload)
    return jsonify(response)

################ POWER ##################

def grab_payload(path_to_payload):
    file = open(path_to_payload)
    payload = json.loads(file.read())
    file.close()
    return payload

def calculate_merit_order(payload):
    # Set the price per MWh for each plant in the dict from the json
    for plant in payload["powerplants"]:
        if plant["type"] == "windturbine":
            base_price = 0
        if plant["type"] == "turbojet":
            base_price = payload["fuels"]["kerosine(euro/MWh)"]
        if plant["type"] == "gasfired":
            base_price = payload["fuels"]["gas(euro/MWh)"]
        plant["price"] = base_price / plant["efficiency"]
    # Get the merit order by sorting the list with all the prices and recovering the indices
    price_list = [plant["price"] for plant in payload["powerplants"]]
    merit_order = np.argsort(price_list)
    return payload, merit_order

def unit_commitment(total_load, payload, merit_order):
    list_response = []
    remaining_load = total_load
    plants = payload["powerplants"]
    for i in merit_order:
        current_plant = plants[i]
        if remaining_load == 0:
            new_plant_dict = {"name":current_plant["name"], "p":0}
            list_response.append(new_plant_dict)
        else:
            # case: pmin is too much for what is remaining
            if remaining_load - current_plant["pmin"] < 0:
                difference_load = remaining_load - current_plant["pmin"]
                # Adjust the power from the previous plant used
                list_response[-1]["p"] += difference_load
                new_plant_dict = {"name":current_plant["name"], "p":current_plant["pmin"]}
                list_response.append(new_plant_dict)
                remaining_load = 0
            # case: pmax is not enough, send full power
            if remaining_load - current_plant["pmax"] > 0:
                if current_plant["type"] == "windturbine":
                    pmax = (payload["fuels"]["wind(%)"] / 100) * current_plant["pmax"]
                else:
                    pmax = current_plant["pmax"]
                new_plant_dict = {"name":current_plant["name"], "p":round(pmax,1)}
                list_response.append(new_plant_dict)
                remaining_load = remaining_load - pmax
            # case: choose remaining power based on the difference
            else:
                new_plant_dict = {"name":current_plant["name"], "p":round(remaining_load,1)}
                list_response.append(new_plant_dict)
                remaining_load = 0
    return list_response
        

def power_distribution(payload):
    total_load = payload["load"]
    payload, merit_order = calculate_merit_order(payload)
    response = unit_commitment(total_load, payload, merit_order)
    return response

def power_distribution_unit_test():
    path_to_examples = ["example_payloads/payload1.json","example_payloads/payload2.json","example_payloads/payload3.json"]
    payload = grab_payload(path_to_examples[0])
    response = power_distribution(payload)
    print(json.dumps(response, indent=2))
    return 0
    
################ MAIN ##################

if __name__ == '__main__':
    app.run(port=8888) # run on port 8888 for the requirements
    #power_distribution_unit_test()
