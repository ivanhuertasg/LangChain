# -*- coding: utf-8 -*-
"""
Quiz Generator Agent with Chatbot Interface
Uses LangChain + Google Gemini to generate quizzes
"""

import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Initialize session state for API key
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = None

# Function to initialize the LLM with the provided API key
def initialize_llm(api_key):
    os.environ['GOOGLE_API_KEY'] = api_key
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        google_api_key=api_key
    )

def generate_quiz(topic: str, num_questions: int = 5) -> str:
    """Generate a quiz with multiple choice questions"""
    # Check if API key is set
    if not st.session_state.google_api_key:
        return "⚠️ Por favor, introduce tu API key de Google en la barra lateral primero."
    
    prompt = f"""
    Genera un cuestionario sobre el tema: {topic}.
    Incluye {num_questions} preguntas de opción múltiple.
    
    FORMATO OBLIGATORIO (JSON):
    [
      {{
        "pregunta": "Texto de la pregunta",
        "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
        "respuesta_correcta": "Opción correcta"
      }}
    ]
    
    Asegúrate de que las preguntas sean claras y educativas.
    """
    try:
        llm = initialize_llm(st.session_state.google_api_key)
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"Error al generar el cuestionario: {str(e)}"

def main():
    # Page configuration
    st.set_page_config(
        page_title="Quiz Bot - Generador de Cuestionarios",
        page_icon="📚",
        layout="centered"
    )
    
    # Custom CSS for chatbot style
    st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("📚 Quiz Bot")
    st.markdown("### Generador de Cuestionarios con IA")
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("¿Sobre qué tema quieres generar un cuestionario?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate quiz
        with st.chat_message("assistant"):
            with st.spinner("🤔 Generando cuestionario..."):
                # Extract topic from prompt
                topic = prompt
                quiz_result = generate_quiz(topic, num_questions=5)
                
                st.markdown("📝 **Cuestionario Generado:**")
                st.markdown(quiz_result)
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"📝 **Cuestionario sobre '{topic}':**\n\n{quiz_result}"
                })
    
    # Sidebar with API key input and instructions
    with st.sidebar:
        st.header("🔑 API Key")
        api_key_input = st.text_input(
            "Introduce tu Google API Key:",
            type="password",
            value=st.session_state.google_api_key if st.session_state.google_api_key else "",
            help="Obtén tu API key gratuita en: https://aistudio.google.com/app/apikey"
        )
        
        if api_key_input:
            st.session_state.google_api_key = api_key_input
            st.success("✅ API Key configurada correctamente!")
        
        st.markdown("---")
        st.header("ℹ️ Instrucciones")
        st.markdown("""
        1. Introduce tu API key arriba
        2. Escribe un tema en el chat
        3. El bot generará un cuestionario
        4. ¡Listo para usar!
        
        **Ejemplos de temas:**
        - Sistema Solar
        - Historia de España
        - Biología celular
        - Programación Python
        """)
        
        if st.button("🗑️ Limpiar chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
