# Quiz Bot - Generador de Cuestionarios con IA

Un chatbot interactivo que genera cuestionarios sobre cualquier tema usando LangChain y Google Gemini.

## Cómo ejecutar localmente

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar tu API Key de Google
Crea un archivo `.env` en la raíz del proyecto:
```
GOOGLE_API_KEY=tu_api_key_aqui
```

O puedes obtener una clave gratuita en: https://aistudio.google.com/app/apikey

### 3. Ejecutar la aplicación
```bash
streamlit run quiz_agent.py
```

La aplicación se abrirá en: http://localhost:8501

## Despliegue (Deploy)

### Opción 1: Streamlit Cloud (GRATIS)

1. **Sube tu código a GitHub**
   - Crea un repositorio nuevo
   - Sube los archivos: `quiz_agent.py`, `requirements.txt`, y `.streamlit/config.toml`
   - Crea un archivo `.streamlit/secrets.toml` con tu API key:
     ```toml
     GOOGLE_API_KEY = "tu_api_key_aqui"
     ```

2. **Despliega en Streamlit Cloud**
   - Ve a https://share.streamlit.io
   - Inicia sesión con GitHub
   - Selecciona tu repositorio
   - ¡Listo! Obtendrás un URL como: `https://tu-app.streamlit.app`

3. **Comparte el enlace con tu profesor** 🎉

### Opción 2: Render (Alternativa gratuita)

1. Sube el código a GitHub
2. Ve a https://render.com
3. Crea un nuevo "Web Service"
4. Conecta tu repositorio
5. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run quiz_agent.py`

## Cómo usar el Quiz Bot

1. Escribe un tema en el chat (ej: "Sistema Solar" o "Historia de España")
2. El bot generará un cuestionario con preguntas de opción múltiple
3. Cada pregunta incluye la respuesta correcta

## Características

- ✅ Interfaz de chatbot moderna
- ✅ Genera cuestionarios en JSON
- ✅ Historial de conversación
- ✅ Diseño responsivo
- ✅ Despliegue gratuito en la nube

## Notas

- Necesitas una API key de Google Gemini (es gratuita)
- El modelo usado es `gemini-2.0-flash`
- Puedes modificar el número de preguntas en el código
