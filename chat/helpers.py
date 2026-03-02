import ollama
# from serpapi import GoogleSearch
import serpapi

# 1. Define the Google Search Tool
# def google_search(query: str):
#     """
#     Search Google for real-time information when the internal knowledge 
#     is insufficient or outdated.
#     """
#     params = {
#         "engine": "google",
#         "q": query,
#         "api_key": "YOUR_SERPAPI_KEY" # Best practice: use os.getenv("SERPAPI_KEY")
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict()
    
#     # Return a summary of organic results
#     if "organic_results" in results:
#         return [res.get("snippet") for res in results["organic_results"][:3]]
#     return "No results found."

# # 2. Map function names to actual functions
# available_functions = {
#     'google_search': google_search,
# }

# def chat_with_fallback(user_input):
#     # Pass the tool and instructions to Ollama
#     response = ollama.chat(
#         model='llama3.1',
#         messages=[
#             {'role': 'system', 'content': 'You are a helpful assistant. If you do not know the answer or need current data, use the google_search tool.'},
#             {'role': 'user', 'content': user_input}
#         ],
#         tools=[google_search], # Pass the function reference directly
#     )

#     # 3. Handle Tool Calls
#     if response.message.tool_calls:
#         for tool in response.message.tool_calls:
#             function_to_call = available_functions.get(tool.function.name)
#             if function_to_call:
#                 print(f"--- Calling tool: {tool.function.name} ---")
#                 tool_output = function_to_call(**tool.function.arguments)
                
#                 # Send the tool output back to the model for a final answer
#                 final_response = ollama.chat(
#                     model='llama3.1',
#                     messages=[
#                         {'role': 'user', 'content': user_input},
#                         response.message,
#                         {'role': 'tool', 'content': str(tool_output), 'name': tool.function.name}
#                     ]
#                 )
#                 return final_response.message.content
    
#     return response.message.content

# # Example usage
# print(chat_with_fallback("What is the current price of Bitcoin?"))




import ollama
from serpapi import GoogleSearch

def google_search(query):
    # Search logic (same as before)
    params = {"engine": "google", "q": query, "api_key": "c29f0591448ed2a936a07e3d6cc69a07627df621765757c5483d64b7a70be244"}
    search = GoogleSearch(params)
    results = search.get_dict()
    return [res.get("snippet") for res in results.get("organic_results", [])[:3]]

def smart_chat(user_query):
    try:
        # 1. ATTEMPT FIRST: Ask Ollama directly
        # We include a prompt instruction to admit if it doesn't know.
        initial_response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': 'Answer from memory. If you are unsure or need current data, start your response with [NEED_SEARCH].'},
                {'role': 'user', 'content': user_query}
            ]
        )
        
        content = initial_response.message.content

        # 2. CHECK: Does the result indicate missing info?
        if "[NEED_SEARCH]" in content or "I don't have" in content.lower():
            print("--- Ollama lacks knowledge. Falling back to Google Search... ---")
            
            # 3. WEB SEARCH: Get real-time data
            search_results = google_search(user_query)
            
            # 4. FINAL ANSWER: Give the search data to Ollama
            final_response = ollama.chat(
                model='llama3',
                messages=[
                    {'role': 'system', 'content': 'Answer the user using these search results.'},
                    {'role': 'user', 'content': f"Search Results: {search_results}\n\nQuestion: {user_query}"}
                ]
            )
            response={
                "response":final_response.message.content,
                "tool":"web search"
            }
            return final_response.message.content
        response={
                "response":content,
                "tool":None
            }
        return content
    except Exception as e:
        print(e)

# Test it
# print(smart_chat("What is the current stock price of Apple?"))