# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from .utils import (
    caused_by, find_parasite, get_disease_and_correlated_disease,
    find_disease_from_vulnerability, find_all_users,
    parasite_symptoms, vulnerable_treatments, user_disease_causes
)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# In-memory chat history
chat_history = []

def chat_view(request):
    """Render the chat interface as the default page."""
    return render(request, 'chatbot/chat.html')

def chat_api(request):
    """Handle POST requests to process chat messages with MeTTa context and Gemini responses."""
    if request.method == 'POST':
        try:
            # Parse JSON from request.body
            data = json.loads(request.body)
            user_message = data.get('message')
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            # Add user message to chat history
            chat_history.append({'role': 'user', 'content': user_message})

            # Normalize user input for parsing (case-insensitive matching)
            user_message_lower = user_message.lower()

            # Initialize context for Gemini
            context = ""
            metta_results = None

            # Parse and execute MeTTa queries based on user input
            try:
                # Check for disease-related queries
                if "cause" in user_message_lower or "why" in user_message_lower:
                    for disease in ["typoiad", "cold", "malaria"]:  # Add more diseases as needed
                        if disease in user_message_lower:
                            metta_results = caused_by(disease.capitalize())
                            context = f"Causes of {disease.capitalize()}: {metta_results}"
                            break

                elif "parasite" in user_message_lower:
                    for parasite_type in ["bacteria", "virus", "protozoa"]:
                        if parasite_type in user_message_lower:
                            metta_results = parasite_symptoms(parasite_type.capitalize())
                            context = f"Symptoms of {parasite_type.capitalize()} parasites: {metta_results}"
                            break
                        elif "typoiad" in user_message_lower:  # Specific disease fallback
                            metta_results = find_parasite("Typoiad")
                            context = f"Parasite info for Typoiad: {metta_results}"
                            break

                elif "who" in user_message_lower or "users" in user_message_lower:
                    metta_results = find_all_users()
                    context = f"All users: {metta_results}"

                elif any(name in user_message_lower for name in ["bisrat", "amina", "sara"]):
                    for name in ["bisrat", "amina", "sara"]:  # Add more names as needed
                        if name in user_message_lower:
                            if "correlation" in user_message_lower or "related" in user_message_lower:
                                metta_results = get_disease_and_correlated_disease(name.capitalize())
                                context = f"Diseases and correlations for {name.capitalize()}: {metta_results}"
                            else:
                                metta_results = user_disease_causes(name.capitalize())
                                context = f"Causes of {name.capitalize()}’s diseases: {metta_results}"
                            break

                elif "vulnerable" in user_message_lower or "immune" in user_message_lower:
                    if "treatment" in user_message_lower or "treat" in user_message_lower:
                        metta_results = vulnerable_treatments("lowImmuneSystem")
                        context = f"Treatments for diseases vulnerable to low immune system: {metta_results}"
                    else:
                        metta_results = find_disease_from_vulnerability("lowImmuneSystem")
                        context = f"Diseases linked to low immune system: {metta_results}"

                # Parse symptoms explicitly mentioned (uppercase them)
                symptoms = ["fever", "cough", "chills", "diarrhea", "fatigue", "memoryloss", "pain"]
                for symptom in symptoms:
                    if symptom in user_message_lower:
                        symptom_upper = symptom.upper()
                        # Here we could extend to find diseases by symptom, but for now, just note it
                        context += f"\nMentioned symptom: {symptom_upper}"

                # Default context if no specific match
                if not context:
                    context = "I can help with diseases, parasites, users, vulnerabilities, or symptoms. What do you want to know?"

            except ValueError as ve:
                # Handle parsing errors (e.g., invalid input format)
                print(f"Parsing error: {ve}")
                context = f"Error parsing your input: {str(ve)}. Please clarify your question."
            except Exception as me:
                # Handle MeTTa execution errors
                print(f"MeTTa error: {me}")
                context = "Error retrieving medical data. Try again with a different question."

            # Prepare full prompt with chat history and MeTTa context
            conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
            full_prompt = (
                "You are a medical chatbot. Use the provided medical context to answer the user’s question accurately. "
                "If symptoms are mentioned, note them in uppercase in your response. "
                f"Medical context: {context}\nConversation history:\n{conversation}"
            )

            # Call Gemini API
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(full_prompt)
            bot_response = response.text if response.text else "Sorry, I couldn’t respond."

            # Add bot response to chat history
            chat_history.append({'role': 'assistant', 'content': bot_response})

            return JsonResponse({'response': bot_response})

        except json.JSONDecodeError as je:
            print(f"JSON error: {je}")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)