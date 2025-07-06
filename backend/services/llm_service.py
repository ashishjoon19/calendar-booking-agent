from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms.base import LLM
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.model_name = "gemini-pro"
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
    def get_llm(self) -> LLM:
        """Get the LLM instance"""
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )