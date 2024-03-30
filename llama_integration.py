# # llama_integration.py
# import replicate
#
#
# def generate_trip_plan(source, destination, start_date, return_date, flight_info, top_hotels):
#     # Construct a prompt from the flight and hotel information
#     prompt = f"Plan a detailed itinerary for a trip from {source} to {destination}, departing on {start_date} and returning on {return_date}. Here are the flight details: These are top 5 flight details fetched from api along with their prices, choose the cheapest cost of all: {flight_info}. Here is the hotel information of top 5 hotels: {top_hotels}, use this information to pick best and reasonable hotel to plan the trip. Include suggested activities and places to visit."
#
#     # Assuming you have a mechanism to call LLaMA correctly, as previously described
#     output = replicate.run(
#         "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
#         input={
#             "debug": False,
#             "top_p": 1,
#             "prompt": prompt,
#             "temperature": 0.5,
#             "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
#             "max_new_tokens": 50000,
#             "min_new_tokens": -1,
#             "prompt_template": "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
#             "repetition_penalty": 1.15
#         }
#     )
#
#     # Collect and return the model's output
#     trip_plan = ""
#     for item in output:
#         trip_plan += str(item)
#
#     return trip_plan
#
# #print(generate_trip_plan("atlanta","miami","03-22-2024","03=25-2024",""))

import ollama

def generate_trip_plan_stream(source, destination, start_date, return_date, flight_info, top_hotels,adults,children,infants):
    # Create a client
    prompt = f"Plan a detailed itinerary for a trip " \
             f"from {source} to {destination}, departing on {start_date} and " \
             f"returning on {return_date}. Here are the flight details: " \
             f"These are top 5 flight details fetched from api along with " \
             f"their prices, choose the cheapest cost of all: {flight_info}. " \
             f"Here is the hotel information of top 5 hotels: {top_hotels}, " \
             f"use this information to pick best and reasonable hotel to plan " \
             f"the trip. Also consider the number of adults are: {adults},children:{children}, infants:{infants}." \
             f"Include suggested activities and places to visit."

    stream = ollama.chat(
        model='llama2',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    for chunk in stream:
        yield f"{chunk['message']['content']}"
        #print(chunk['message']['content'], end='', flush=True)

#generate_trip_plan("atlanta","miami","03-31-2024","04-05-2024","","")