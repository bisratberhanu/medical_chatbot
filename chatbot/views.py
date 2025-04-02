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

def parse_user_message(user_message):
    """
    Uses Gemini API to parse the user message and extract entities like diseases, symptoms, etc.
    Returns a dictionary with extracted entities in a specific format.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "You are a medical entity parser. Parse the following user message and extract relevant entities "
        "(diseases, parasite types, symptoms, names, vulnerabilities) into a JSON dictionary. "
        "Capitalize the first letter of diseases, parasite types, and names; uppercase symptoms entirely. "
        "Return the result in this format:\n"
        "{\n"
        "  \"diseases\": [\"Disease1\", \"Disease2\"],\n"
        "  \"parasite_types\": [\"Type1\", \"Type2\"],\n"
        "  \"symptoms\": [\"SYMPTOM1\", \"SYMPTOM2\"],\n"
        "  \"names\": [\"Name1\", \"Name2\"],\n"
        "  \"vulnerabilities\": [\"condition1\", \"condition2\"],\n"
        "  \"intent\": \"query_type\"  // e.g., 'causes', 'symptoms', 'treatments', 'users', 'correlations', or 'general'\n"
        "}\n"
        "If an entity type is not found, return an empty list for it. Detect intent based on keywords like "
        "'cause', 'why', 'symptom', 'treat', 'who', 'related'. If no clear intent, use 'general'. "
        "Return only the raw JSON string without backticks or markdown formatting.\n"
        "Examples:\n"
        "- 'What causes Typoiad?' -> {\"diseases\": [\"Typoiad\"], \"parasite_types\": [], \"symptoms\": [], \"names\": [], \"vulnerabilities\": [], \"intent\": \"causes\"}\n"
        "- 'Symptoms of bacterial parasites' -> {\"diseases\": [], \"parasite_types\": [\"Bacteria\"], \"symptoms\": [], \"names\": [], \"vulnerabilities\": [], \"intent\": \"symptoms\"}\n"
        f"User message: {user_message}"
    )

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip()
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:-3].strip()
        elif raw_response.startswith("```"):
            raw_response = raw_response[3:-3].strip()
        parsed_json = json.loads(raw_response)
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Parsing JSON error: {e}")
        return {
            "diseases": [],
            "parasite_types": [],
            "symptoms": [],
            "names": [],
            "vulnerabilities": [],
            "intent": "general"
        }
    except Exception as e:
        print(f"Parsing error: {e}")
        return {
            "diseases": [],
            "parasite_types": [],
            "symptoms": [],
            "names": [],
            "vulnerabilities": [],
            "intent": "general"
        }

def format_metta_result(result):
    """Convert MeTTa Atom objects to readable strings."""
    if isinstance(result, list):
        return [format_metta_result(item) for item in result]
    elif hasattr(result, 'get_name'):  # Check if it’s an Atom
        return str(result.get_name())
    return str(result)

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

            # Parse user message with Gemini
            parsed_entities = parse_user_message(user_message)
            diseases = parsed_entities.get("diseases", [])
            parasite_types = parsed_entities.get("parasite_types", [])
            symptoms = parsed_entities.get("symptoms", [])
            names = parsed_entities.get("names", [])
            vulnerabilities = parsed_entities.get("vulnerabilities", [])
            # print(parsed_entities)  # Debugging output

            # Initialize context
            context = []

            # Gather all possible context from MeTTa functions
            try:
                # Disease-related queries
                for disease in diseases:
                    causes = format_metta_result(caused_by(disease))
                    if causes:
                        context.append(f"Causes of {disease}: {causes}")
                    parasite_info = format_metta_result(find_parasite(disease))
                    if parasite_info:
                        context.append(f"Parasite info for {disease}: {parasite_info}")

                # Parasite type-related queries
                for parasite_type in parasite_types:
                    symptoms_result = format_metta_result(parasite_symptoms(parasite_type))
                    if symptoms_result:
                        context.append(f"Symptoms of {parasite_type} parasites: {symptoms_result}")

                # Name-related queries
                for name in names:
                    causes = format_metta_result(user_disease_causes(name))
                    if causes:
                        context.append(f"Causes of {name}’s diseases: {causes}")
                    correlations = format_metta_result(get_disease_and_correlated_disease(name))
                    if correlations:
                        context.append(f"Diseases and correlations for {name}: {correlations}")

                # Vulnerability-related queries
                for vulnerability in vulnerabilities:
                    diseases_result = format_metta_result(find_disease_from_vulnerability(vulnerability))
                    if diseases_result:
                        context.append(f"Diseases linked to {vulnerability}: {diseases_result}")
                    treatments = format_metta_result(vulnerable_treatments(vulnerability))
                    if treatments:
                        context.append(f"Treatments for diseases vulnerable to {vulnerability}: {treatments}")

                # Users query (if "who" or "users" is mentioned)
                if "who" in user_message.lower() or "users" in user_message.lower():
                    users = format_metta_result(find_all_users())
                    if users:
                        context.append(f"All users: {users}")

                # Add symptoms to context if present
                if symptoms:
                    context.append(f"Mentioned symptoms: {', '.join(symptoms)}")

                # Default context if no specific match
                if not context:
                    context.append("I can help with diseases, parasites, users, vulnerabilities, or symptoms. What do you want to know?")
                else:
                    context = "\n".join(context)  # Join all context lines
                    print(context)

            except Exception as me:
                print(f"MeTTa error: {me}")
                context = "Error retrieving medical data. Try again with a different question."

            # Prepare full prompt with chat history and MeTTa context
            conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
            full_prompt = (
                "You are a medical chatbot. Use the provided medical context to answer the user’s question accurately. "
                "If symptoms are mentioned, include them in uppercase in your response as provided. "
                f"Medical context: {context}\nConversation history:\n{conversation}"
            )

            # Call Gemini API for final response
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