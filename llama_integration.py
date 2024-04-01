# llama_integration.py

import ollama
from rag import rag_chain


def generate_trip_plan_stream(source, destination, start_date, return_date, flight_info, top_hotels,adults,children,infants):
    rag_question = f"What are some highlights and tips for visiting {destination}?"

    # Get RAG-based context
    rag_context = rag_chain(rag_question)
    # Create a client

    # prompt = f"Plan a detailed itinerary for a trip " \
    #          f"from {source} to {destination}, departing on {start_date} and " \
    #          f"returning on {return_date}. Here are the flight details: " \
    #          f"These are top 5 flight details fetched from api along with " \
    #          f"their prices, choose the cheapest cost of all: {flight_info}. " \
    #          f"Here is the hotel information of top 5 hotels: {top_hotels}, " \
    #          f"use this information to pick best and reasonable hotel to plan " \
    #          f"the trip. Also consider the number of adults are: {adults},children:{children}, infants:{infants}." \
    #          f"Include suggested activities and places to visit."

    print("Rag Context",rag_context)

    prompt = f"Plan a detailed itinerary for a trip from " \
             f"{source} to {destination}, departing on {start_date}" \
             f" and returning on {return_date}. Here are the flight details: " \
             f"These are top 5 flight details fetched from api along with " \
             f"their prices, choose the cheapest cost of all: {flight_info}. " \
             f"Here is the hotel information of top 5 hotels: {top_hotels}, " \
             f"use this information to pick best and reasonable hotel to plan " \
             f"the trip. Also consider the number of adults are: {adults}, " \
             f"children: {children}, infants: {infants}. Include suggested " \
             f"activities and places to visit based on this context: {rag_context}"

    stream = ollama.chat(
        model='llama2',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    for chunk in stream:
        yield f"{chunk['message']['content']}"
        #print(chunk['message']['content'], end='', flush=True)

