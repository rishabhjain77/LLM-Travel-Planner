# app.py
from flask import Flask, render_template, request, jsonify,Response, stream_with_context
from flight_api_integration import get_flight_one_way,get_flight_two_way, resolve_airport_entity_id
from hotel_api_integration import resolve_hotel_entity_id, get_hotel_info
import replicate
import time
from llama_integration import generate_trip_plan

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
    members="1"
    print("Source",source)
    print("destination", destination)
    print("start_date", start_date)
    print("return_date", return_date)
    print("transport_mode", transport_mode)



    # Resolve entity IDs for flights and hotels
    source_id = resolve_airport_entity_id(source)
    destination_id = resolve_airport_entity_id(destination)
    print("Entity",source_id)
    print("Destination",destination_id)

    if not source_id or not destination_id:
        return jsonify({"error": "Failed to resolve airport IDs"}), 400

    if transport_mode == "flight":
        if return_date:
            response = get_flight_two_way(source_id, destination_id, start_date, return_date, members)
        else:
            response = get_flight_one_way(source_id, destination_id, start_date, members)

    #response = response.json()

    print("Token...",response['data']['token'])
    itineraries_data = response["data"]["itineraries"]
    top_itineraries = []
    flight_info = ""

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


    #flight_info = ". ".join(top_itineraries)


    hotel_entity_id = resolve_hotel_entity_id(destination)

    hotel_result = get_hotel_info(hotel_entity_id,start_date,return_date)

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

    def generate_trip_plan_stream():
        # Construct a prompt from the flight and hotel information
        prompt = f"Plan a detailed itinerary for a trip from {source} to {destination}, departing on {start_date} and returning on {return_date}. Here are the flight details: These are top 5 flight details fetched from api along with their prices, choose the cheapest cost of all: {flight_info}. Here is the hotel information of top 5 hotels: {top_hotels}, use this information to pick best and reasonable hotel to plan the trip. Include suggested activities and places to visit."

        # Assuming you have a mechanism to call LLaMA correctly, as previously described
        output = replicate.run(
            "meta/llama-2-70b-chat",
            input={
                "debug": False,
                "top_p": 1,
                "prompt": prompt,
                "temperature": 0.5,
                "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
                "max_new_tokens": 50000,
                "min_new_tokens": -1,
                "prompt_template": "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
                "repetition_penalty": 1.15
            },
            stream=True,
        )

        yield "data: Starting trip plan generation...\n\n"

        # for item in output:
        #     if item.get("choices"):
        #         for choice in item["choices"]:
        #             trip_plan_chunk = choice["text"]
        #             yield f"data: {trip_plan_chunk}\n\n"
        #             time.sleep(0.1)  # Adjust the delay as needed
        accumulated_output = ""
        for item in output:
            accumulated_output += str(item)
            if len(accumulated_output) >= 100 or '\n' in accumulated_output:
                yield f"data: {accumulated_output}\n\n"
                accumulated_output = ""

        if accumulated_output:
            yield f"data: {accumulated_output}\n\n"

        yield "data: End of trip plan\n\n"

    return Response(stream_with_context(generate_trip_plan_stream()), mimetype="text/event-stream")
    # Uncomment below for AI
    #trip_plan = generate_trip_plan(source, destination, start_date, return_date, top_itineraries,top_hotels)

    #return render_template('trip_plan.html', trip_plan=trip_plan)


if __name__ == '__main__':
    app.run(debug=True)
