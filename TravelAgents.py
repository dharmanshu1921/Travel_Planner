import streamlit as st
from crewai import Agent
from langchain_groq import ChatGroq
from TravelTools import SearchTool
import re
import os
from crewai import LLM
from crewai_tools import TXTSearchTool, PDFSearchTool

from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model="gemini/gemini-1.5-pro-002",
    api_key=os.environ["GOOGLE_API_KEY"]
)

# llm = ChatGroq(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])
# llm = ChatGroq(model="groq/gemma2-9b-it", api_key=os.environ["GROQ_API_KEY"])
# llm = ChatGroq(model="groq/mixtral-8x7b-32768", api_key=os.environ["GROQ_API_KEY"])

Reader_tool = TXTSearchTool(
    txt="TravelPlanner/travel.txt",
    config={
        "llm": {
            "provider": "groq",  
            "config": {
                "model": "groq/mixtral-8x7b-32768",
            },
        },
        "embedder": {
            "provider": "cohere",
            "config": {
                "model": "embed-english-v3.0",
                "api_key": os.environ["COHERE_API_KEY"],
            }
        },
    }
)
pdf_Reader_tool = PDFSearchTool(
    txt="TravelPlanner/travel.pdf",
    config={
        "llm": {
            "provider": "groq",  
            "config": {
                "model": "groq/mixtral-8x7b-32768",
            },
        },
        "embedder": {
            "provider": "cohere",
            "config": {
                "model": "embed-english-v3.0",
                "api_key": os.environ["COHERE_API_KEY"],
            }
        },
    }
)

# AGENTS
class TravelAgents():
    
    # LLM Setting
    llm = ChatGroq(model="llama3-70b-8192", temperature=0, api_key=st.secrets['GROQ_API'])
    
    # Agent city expert
    def location_expert(self):
        return Agent(
            role="Travel Trip Expert",
            goal="Adapt to the user destination city language (Hindi if ciy in India. Gather helpful information about to the city and city during travel.",
            backstory="""A seasoned traveler who has explored various destinations and knows the ins and outs of travel logistics.""",
            tools=[SearchTool.search_web_tool,Reader_tool,pdf_Reader_tool],
            verbose=True,
            max_iter=5,
            llm=llm,
            allow_delegation=False,
            # step_callback=streamlit_callback,
            )
    
    # Agent Resercher
    def guide_expert(self):
        return Agent( 
            role="City Local Guide Expert",
            goal="Provides information on things to do in the city based on the user's interests.",
            backstory="""A local expert with a passion for sharing the best experiences and hidden gems of their city.""",
            tools=[SearchTool.search_web_tool,Reader_tool,pdf_Reader_tool],
            verbose=True,
            max_iter=5,
            llm=llm,
            allow_delegation=False,
            # step_callback=streamlit_callback,
            )
    
    # Agent Resercher
    def planner_expert(self):
        return Agent(
            role="Travel Planning Expert",
            goal="Compiles all gathered information to provide a comprehensive travel plan.",
            backstory="""
            You are a professional guide with a passion for travel.
            An organizational wizard who can turn a list of possibilities into a seamless itinerary.
            """,
            tools=[SearchTool.search_web_tool,Reader_tool,pdf_Reader_tool],
            verbose=True,
            max_iter=5,
            llm=llm,
            allow_delegation=False,
            # step_callback=streamlit_callback,
            )



class StreamToExpander:
    
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  
        self.color_index = 0 

    def write(self, data):
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            self.color_index = (self.color_index + 1) % len(self.colors) 
            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "City Selection Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("City Selection Expert", f":{self.colors[self.color_index]}[City Selection Expert]")
        if "Local Expert at this city" in cleaned_data:
            cleaned_data = cleaned_data.replace("Local Expert at this city", f":{self.colors[self.color_index]}[Local Expert at this city]")
        if "Amazing Travel Concierge" in cleaned_data:
            cleaned_data = cleaned_data.replace("Amazing Travel Concierge", f":{self.colors[self.color_index]}[Amazing Travel Concierge]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []
