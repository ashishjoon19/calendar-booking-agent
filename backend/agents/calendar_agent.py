from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from typing import Dict, Any
import json
from datetime import datetime, timedelta

from services.llm_service import LLMService
from services.calendar_service import CalendarService
from .tools import get_calendar_tools

class CalendarBookingAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.calendar_service = CalendarService()
        self.sessions: Dict[str, Any] = {}
        self.tools = get_calendar_tools(self.calendar_service)
        self.agent_executor = self._create_agent()
    
    def _create_agent(self):
        """Create the LangChain agent with tools"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful calendar booking assistant. You can help users:
            1. Check calendar availability
            2. Book appointments
            3. List existing appointments
            4. Cancel appointments
            
            Always be conversational and helpful. When booking appointments:
            - Ask for appointment title/description
            - Ask for preferred date and time
            - Ask for duration if not specified
            - Confirm details before booking
            
            Use the available tools to interact with the calendar. Be natural in your responses."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        agent = create_openai_functions_agent(
            self.llm_service.get_llm(),
            self.tools,
            prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            memory=ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        )
    
    async def process_message(self, message: str, session_id: str) -> str:
        """Process user message and return response"""
        try:
            # Get or create session
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "memory": ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True
                    )
                }
            
            # Update agent memory
            self.agent_executor.memory = self.sessions[session_id]["memory"]
            
            # Process message
            response = await self.agent_executor.ainvoke({"input": message})
            
            return response["output"]
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."