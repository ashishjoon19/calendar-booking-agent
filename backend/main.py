from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Simple response without complex agent framework
load_dotenv()

app = FastAPI(title="Calendar Booking Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Simple response for testing
        message = request.message.lower()
        
        if "appointment" in message or "book" in message:
            response = "I'd be happy to help you book an appointment! To get started, I'll need:\n\n1. What's the appointment for?\n2. What date would you prefer?\n3. What time works best for you?\n4. How long should the appointment be?\n\nPlease provide these details and I'll book it for you!"
        elif "schedule" in message or "upcoming" in message:
            response = "Let me check your upcoming appointments... Currently showing a simplified response. Your calendar integration will be added once we resolve the package issues."
        elif "availability" in message or "free" in message:
            response = "I can check your availability! Please let me know what date you'd like me to check, and I'll see what time slots are available."
        elif "cancel" in message:
            response = "I can help you cancel an appointment. Please provide the appointment details or event ID you'd like to cancel."
        else:
            response = "Hello! I'm your calendar booking assistant. I can help you with:\n\n• 📅 Check your availability\n• ➕ Book new appointments\n• 📋 View upcoming appointments\n• ❌ Cancel appointments\n\nWhat would you like to do?"
        
        return ChatResponse(response=response, session_id=request.session_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is running successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
