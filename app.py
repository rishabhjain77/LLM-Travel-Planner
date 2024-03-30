# app.py
from flask import Flask, render_template, request, jsonify,Response, stream_with_context
from flight_api_integration import get_flight_one_way,get_flight_two_way, resolve_airport_entity_id
from hotel_api_integration import resolve_hotel_entity_id, get_hotel_info
from llama_integration import generate_trip_plan_stream

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plan-trip', methods=['POST'])
def plan_trip():
    # Extract form data
    source = request.form['source']
    destination = request.form['destination']
    start_date = request.form['startDate']
    return_date = request.form['returnDate']
    transport_mode = request.form['transportMode']
    adults=request.form['adults']
    children=request.form['children']
    infants = request.form['infants']

    print("Source",source)
    print("destination", destination)
    print("start_date", start_date)
    print("return_date", return_date)
    print("transport_mode", transport_mode)
    print("Adults", adults)
    print("Children", children)
    print("Infants", infants)


    # Resolve entity IDs for flights and hotels
    source_id = resolve_airport_entity_id(source)
    destination_id = resolve_airport_entity_id(destination)
    print("Entity",source_id)
    print("Destination",destination_id)

    if not source_id or not destination_id:
        return jsonify({"error": "Failed to resolve airport IDs"}), 400

    if transport_mode == "flight":
        if return_date:
            response = get_flight_two_way(source_id, destination_id, start_date, return_date, adults,children,infants)
        else:
            response = get_flight_one_way(source_id, destination_id, start_date, adults,children,infants)


    print("Token...",response['data']['token'])
    itineraries_data = response["data"]["itineraries"]
    top_itineraries = []

    for itinerary in itineraries_data[:5]:  # Limit to top 5 itineraries
        price = itinerary["price"]["formatted"]
        carrier_name = itinerary["legs"][0]["carriers"]["marketing"][0]["name"]
        departure = itinerary["legs"][0]["departure"]
        arrival = itinerary["legs"][-1]["arrival"]

        top_itineraries.append({
            "price": price,
            "carrier_name": carrier_name,
            "departure": departure,
            "arrival": arrival
        })

    print("Top 5..",top_itineraries)

    hotel_entity_id = resolve_hotel_entity_id(destination)

    hotel_result = get_hotel_info(hotel_entity_id,start_date,return_date,adults)

    hotels = hotel_result["data"]["results"]["hotelCards"]

    top_hotels = []

    for hotel in hotels[:5]:
        name = hotel["name"]
        stars = hotel["stars"]
        relevantPoiDistance = hotel["relevantPoiDistance"]
        price = hotel["lowestPrice"]["price"]

        top_hotels.append({
            "price": price,
            "hotel_name": name,
            "stars": stars,
            "relevantPoiDistance": relevantPoiDistance
        })

    print("Hotel Information...",top_hotels)

    return Response(stream_with_context(generate_trip_plan_stream(source, destination, start_date, return_date, str(top_itineraries), str(top_hotels), adults,children,infants)), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True)
