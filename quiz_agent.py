# -*- coding: utf-8 -*-
"""
Quiz Generator Agent with Chatbot Interface
Uses LangChain + Google Gemini to generate quizzes
"""

import os
import sys
import io
import json
import re

# Fix for Windows encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Initialize session state
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = None

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None

if 'quiz_topic' not in st.session_state:
    st.session_state.quiz_topic = None

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to initialize the LLM with the provided API key
def initialize_llm(api_key):
    os.environ['GOOGLE_API_KEY'] = api_key
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        google_api_key=api_key
    )

def clean_json_response(response: str) -> str:
    """Clean the JSON response from markdown formatting"""
    response = re.sub(r'^```json\s*', '', response)
    response = re.sub(r'^```\s*', '', response)
    response = re.sub(r'```$', '', response)
    response = response.strip()
    return response

def generate_quiz(topic: str, num_questions: int = 5) -> str:
    """Generate quiz questions without answers"""
    if not st.session_state.google_api_key:
        return "Por favor, introduce tu API key de Google en la barra lateral primero."
    
    prompt = f"""
Genera un cuestionario sobre el tema: {topic}.
Incluye {num_questions} preguntas de opcion multiple.

FORMATO OBLIGATORIO (solo JSON, sin texto adicional):
[
  {{
    "pregunta": "Texto de la pregunta",
    "opciones": ["Opcion A", "Opcion B", "Opcion C", "Opcion D"],
    "respuesta_correcta": "Opcion correcta"
  }}
]

Asegurate de que las preguntas sean claras y educativas.
Devuelve SOLO el JSON, sin texto adicional.
"""
    try:
        llm = initialize_llm(st.session_state.google_api_key)
        response = llm.invoke([HumanMessage(content=prompt)])
        return clean_json_response(response.content)
    except Exception as e:
        return f"Error al generar el cuestionario: {str(e)}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="Quiz Bot - Generador de Cuestionarios",
        page_icon="📚",
        layout="centered"
    )
    
    # Header
    st.title("Quiz Bot")
    st.markdown("### Generador de Cuestionarios con IA")
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Check if quiz is active
    if st.session_state.quiz_active and st.session_state.quiz_data:
        # Display current question
        current_idx = st.session_state.current_question
        if current_idx < len(st.session_state.quiz_data):
            question = st.session_state.quiz_data[current_idx]
            
            st.markdown(f"### Pregunta {current_idx + 1}/{len(st.session_state.quiz_data)}")
            st.markdown(f"**{question['pregunta']}**")
            
            options = question['opciones']
            st.markdown(f"A) {options[0]}")
            st.markdown(f"B) {options[1]}")
            st.markdown(f"C) {options[2]}")
            st.markdown(f"D) {options[3]}")
            
            # Get user answer
            user_answer = st.text_input("Tu respuesta (A, B, C o D):", key=f"answer_{current_idx}")
            
            if st.button("Responder", key=f"submit_{current_idx}"):
                correct_option = question['respuesta_correcta']
                user_choice = user_answer.upper().strip()
                
                # Check if answer is correct
                if user_choice == correct_option[0]:
                    st.session_state.score += 1
                    st.success("Correcto!")
                else:
                    st.error(f"Incorrecto. La respuesta correcta era: {correct_option}")
                
                # Move to next question
                st.session_state.current_question += 1
                st.rerun()
        else:
            # Show final results
            total = len(st.session_state.quiz_data)
            score = st.session_state.score
            percentage = int((score / total) * 100) if total > 0 else 0
            
            st.markdown("---")
            st.markdown("## Resultado Final")
            st.markdown(f"**Puntuacion: {score}/{total}** ({percentage}%)")
            
            if percentage >= 80:
                st.balloons()
                st.markdown("Excelente trabajo!")
            elif percentage >= 60:
                st.markdown("Bien hecho!")
            else:
                st.markdown("Sigue practicando!")
            
            if st.button("Nuevo Cuestionario"):
                st.session_state.quiz_data = None
                st.session_state.quiz_topic = None
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.quiz_active = False
                st.rerun()
    else:
        # Chat input for new quiz
        if prompt := st.chat_input("Sobre que tema quieres generar un cuestionario?"):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate quiz
            with st.chat_message("assistant"):
                with st.spinner("Generando cuestionario..."):
                    topic = prompt
                    quiz_result = generate_quiz(topic, num_questions=5)
                    
                    try:
                        quiz_data = json.loads(quiz_result)
                        
                        # Save quiz data to session state
                        st.session_state.quiz_data = quiz_data
                        st.session_state.quiz_topic = topic
                        st.session_state.current_question = 0
                        st.session_state.score = 0
                        st.session_state.quiz_active = True
                        
                        st.success("Cuestionario generado! Comenzando...")
                        st.rerun()
                        
                    except json.JSONDecodeError:
                        st.error("Error al procesar el cuestionario. Intenta de nuevo.")
                        st.markdown(quiz_result)
            
            # Add bot message to history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Cuestionario sobre '{topic}' generado."
            })
    
    # Sidebar with API key input and instructions
    with st.sidebar:
        st.header("API Key")
        api_key_input = st.text_input(
            "Introduce tu Google API Key:",
            type="password",
            value=st.session_state.google_api_key if st.session_state.google_api_key else "",
            help="Obtén tu API key gratuita en: https://aistudio.google.com/app/apikey"
        )
        
        if api_key_input:
            st.session_state.google_api_key = api_key_input
            st.success("API Key configurada correctamente!")
        
        st.markdown("---")
        st.header("Instrucciones")
        st.markdown("""
        1. Introduce tu API key arriba
        2. Escribe un tema en el chat
        3. El bot generara un cuestionario
        4. Responde cada pregunta
        5. Veras tu puntuacion final
        
        **Ejemplos de temas:**
        - Sistema Solar
        - Historia de España
        - Biologia celular
        - Programacion Python
        """)
        
        if st.button("Limpiar todo"):
            st.session_state.messages = []
            st.session_state.quiz_data = None
            st.session_state.quiz_topic = None
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.quiz_active = False
            st.rerun()

if __name__ == "__main__":
    main()