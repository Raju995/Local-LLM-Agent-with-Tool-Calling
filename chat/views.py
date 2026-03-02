from django.shortcuts import render

from .helpers import smart_chat
# from langchain.agents import AgentExecutor
# from langchain_classic.agents import AgentExecutor

# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_community.llms import Ollama
# from langchain_core.prompts import PromptTemplate
# from langgraph.prebuilt import create_react_agent,AgentExecutor
# from langchain_ollama import ChatOllama
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain.tools import Tool
# from langchain.agents import initialize_agent,Tool
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# llm = ChatOllama(
#     model="llama3.1",
#     temperature=0,
#     # other params...
# )
# search_tool = DuckDuckGoSearchRun()
# tools=[
#     Tool(
#         name="Web Search",
#         func=search_tool.run

#     )
# ]
# agent=initialize_agent(
#     tools=tools,  # Adding our previously created tool
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:


            # 1. Setup local LLM (e.g., Llama 3)
            # llm = Ollama(model="llama3")

            # # # 2. Setup Search Tool (requires API key from tavily.com)
            # # search_tool = TavilySearchResults(max_results=2)
            # tools = [search_tool]
            # search_tool = DuckDuckGoSearchRun()
            # tools=[search_tool.run
            
            # ]

            # # # # 3. Create Agent with specialized prompt
            # prompt = PromptTemplate.from_template(
            #     "Use the following search tool if you do not know the answer: {input}\n{agent_scratchpad}"
            # )
            # agent = create_react_agent(llm, tools, prompt)
            # agent_executor = AgentExecutor(agent=agent, tools=tools)

            # # 4. Run query
            # response = agent_executor.invoke({"input": "What is the price of Bitcoin today?"})
            # print(response['output'])
            data=request.data
            query=data["query"]
            ans=smart_chat(query)
            # print(ans)
            # content = {'message': 'Hello, World!'}
            return Response(ans)
        except Exception as e:
            content = {'error': e}
            return Response(content)

