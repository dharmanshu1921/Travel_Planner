# CrewAI Travel Planner

## Overview
This Travel Planner is an intelligent AI-powered application built using CrewAI that helps users create comprehensive and personalized travel itineraries. The system leverages multiple AI agents to research, plan, and optimize travel experiences.

## Prerequisites
- Python 3.8+
- CrewAI
- Gemini and GROQ Api key
- Internet connection for real-time research

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/travel-planner-crewai.git
cd travel-planner-crewai
```

### 2. Create Virtual Environment
```bash
python -m venv planner
source planner/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_openai_api_key_here
```

### 5. Running 
`python -m streamlit run TravelCrewApp.py`
