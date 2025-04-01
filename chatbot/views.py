from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
# Configure Gemini API with your API key (set this in your environment variables)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace with your actual API key

# api_key = "AIzaSyDTYi30PmGAajYVBR3qdIoJfOJw1RzsnZU"
# genai.configure(api_key = api_key)

# In-memory chat history (resets on server restart)
chat_history = []

def chat_view(request):
    """Render the chat interface as the default page."""
    return render(request, 'chatbot/chat.html')

def chat_api(request):
    """Handle POST requests to process chat messages and return Gemini API responses."""
    if request.method == 'POST':
        print("Request body:", request.body)  # Debugging: Log the raw request body

        try:
            # Parse JSON from request.body
            data = json.loads(request.body)
            print("Parsed data:", data)  # Debugging: Log the parsed data
            user_message = data.get('message')
            if not user_message:
                print("No message provided")  # Debugging
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Add user message to chat history
            chat_history.append({'role': 'user', 'content': user_message})
            
            # Prepare conversation context for Gemini
            conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
            
            # Call Gemini API
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(conversation)
            
            # Extract bot response
            bot_response = response.text if response.text else "Sorry, I couldn’t respond."
            
            # Add bot response to chat history
            chat_history.append({'role': 'assistant', 'content': bot_response})
            
            return JsonResponse({'response': bot_response})
        except json.JSONDecodeError as e:
            print("JSON error:", e)  # Debugging: Log JSON parsing errors
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print("Unexpected error:", e)  # Debugging: Catch other errors
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)