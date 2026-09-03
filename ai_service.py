import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models import IncidentPayload

load_dotenv()

# 1. Define the mandatory output structure
class AIDecision(BaseModel):
    decision: str = Field(
        description="Must be exactly one of: 'respond', 'ask', or 'escalate'"
    )
    message: str = Field(
        description="The solution, clarifying question, or escalation reason"
    )

def load_kb_articles():
    with open("Knowledge_Base/kb_articles.json", "r") as file:
        return json.load(file)["articles"]

def analyze_incident(incident: IncidentPayload) -> dict:
    kb_articles = load_kb_articles()
    
    # 2. Set up the model
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="qwen/qwen3.8-27b",
        temperature=0
    )
    
    # 3. Force the model to adhere to the structure
    structured_llm = llm.with_structured_output(AIDecision)
    
    # 4. Build the Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an IT support agent. Analyze the support ticket and decide the next action based ONLY on the provided knowledge base articles.

        Knowledge Base:
        {kb_articles}

        Rules:
        - If the issue explicitly matches an article, your decision is 'respond' and provide the solution.
        - If the issue might match but needs more details, your decision is 'ask' and ask a clarifying question.
        - If the issue does not match any article, your decision is 'escalate' and state that it needs human review."""),
        ("user", "Ticket Number: {number}\nShort Description: {short_desc}\nDescription: {desc}")
    ])
    
    # 5. Combine the Prompt with the model (LCEL Chain)
    chain = prompt | structured_llm
    
    # 6. Execute and retrieve the result as a Dictionary
    result = chain.invoke({
        "kb_articles": json.dumps(kb_articles, indent=2),
        "number": incident.number,
        "short_desc": incident.short_description,
        "desc": incident.description
    })
    
    # The result will be returned as a Pydantic object, we convert it to a dict so the rest of the code works normally
    return result.model_dump()