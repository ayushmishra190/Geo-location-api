from flask import Flask, make_response, request
from dicttoxml import dicttoxml as toxml
import requests

# ---------------intializing-app-variables-and-functions

my_app = Flask(__name__)
api_key = 'Forbidden to show'  # ---google-api-key
base_url = "https://maps.googleapis.com/maps/api/geocode/json"

# ----------------flask-app-routes

@my_app.route('/getAddressDetails', methods=['POST'])

def getAddressDetails():
    request_content = request.json
    address = request_content['address']
    output_format = request_content['output_format']

    return make_response(address_response(address, output_format), 200)

# ------------------main-function-to-process-request-and-return-a-good-response

def address_response(address: str,output_format: str = "json"):

    # --Fetching-latitude-and-longitude-data-from-google-maps-api
    google_url_for_fetching_raw_location_data = f"{base_url}?address={address}&key={api_key}"
    try :

        raw_data = requests.post(google_url_for_fetching_raw_location_data)
        results = raw_data.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']

        response = {

            "coordinates": {
                "lat": lat,
                "lng": lng
            },
            "address": address
            
        }

        if output_format == "json":

            return response

        else:

            xml_response = toxml(response)
            return xml_response
    
    except :
        return 'Error'

# ------------main-function
if __name__ == "__main__":

    my_app.run(debug=True)
