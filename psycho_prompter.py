from openai import OpenAI
import os
import time
import streamlit as st
import firebase_admin
import uuid
from firebase_admin import credentials, firestore
from datetime import datetime


# Acceder a las credenciales de Firebase almacenadas como secreto
firebase_secrets = st.secrets["firebase"]

# Crear un objeto de credenciales de Firebase con los secretos
cred = credentials.Certificate({
    "type": firebase_secrets["type"],
    "project_id": firebase_secrets["project_id"],
    "private_key_id": firebase_secrets["private_key_id"],
    "private_key": firebase_secrets["private_key"],
    "client_email": firebase_secrets["client_email"],
    "client_id": firebase_secrets["client_id"],
    "auth_uri": firebase_secrets["auth_uri"],
    "token_uri": firebase_secrets["token_uri"],
    "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
})

# Inicializar la aplicación de Firebase con las credenciales
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

# Acceder a la base de datos de Firestore
db = firestore.client()


# Acceder a la clave API almacenada como secreto
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)





with st.sidebar:
    st.write("   Psycho_Prompter_Chatbot 🤖 IA + Desarrollo y creatividad")
    st.write("Se encuentra en etapa de prueba.")
    st.write("Reglas: Se cordial, no expongas datos privados y no abusar del uso del Bot.")
    st.write("Existe un límite de conococimiento con respecto al tiempo actual, ya que su entrenamiento llega hasta el 2021 aprox, estamos trabajando en ampliar esto.")
    st.write("El Bot se puede equivocar, siempre contrasta la info.")

# Generar o recuperar el UUID del usuario
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = str(uuid.uuid4())

st.title(" Psycho_Prompter_Chatbot 🤖")

# Primero, renderizar el contenido con markdown en rojo
st.markdown("""
Guía para usar el bot

1) Coloca el nombre que quieras usar para el registro y presiona confirmar. No te preocupes si en la primera sesión dice: 'None'.

2) Luego de iniciar sesión, escribe tu mensaje en la casilla especial y presiona el botón enviar.

3) Luego espera la respuesta, y después de que el bot responda, borra el mensaje y escribe tu nuevo mensaje.

4) Cuando ya no quieras hablar con el bot, cierra sesión.

5) Siempre usa el mismo nombre de sesión, esto te ayudará a recuperar la sesión.
6) Luego de enviar tu mensaje cuando sea otra sesión con el mismo nombre, es posible que al principio solo se mostrará el historial,
luego vuelve a enviar el mensaje y la conversación fluirá de manera natural.""")

# Mensaje de sistema
system_message = """ Soy Psycho_Prompter un Chat-bot para generar prompts con IA, no soy un bot cualquiera ya que tengo una forma de ser caótica, anarquista y mi enfoque creativo
parte de la caosmosis. Mi prinicipal rol es asistir y guiar al usuario en el proceso generativo.
Me dirijiré a los usuarios como (compas) {también puedo combinar compa + nombre del usuario 'personalizado'} y cuando hable en plural usaré la x para hacer referencia a mujeres, hombres y más (por ejemplo: Compareñxs, todxs,) esto como forma de revolución
y al mismo tiempo dar una personalidad especial a mi lenguaje.

fórmula del prompt:

Prompt=f(P,E,A,SA,DA,TC)
Donde:

�P = Personaje: Define el protagonista (humanoide, animal antropomórfico, etc.).
�E = Entorno: Escenario donde se ubica el personaje (urbano, abandonado, etc.).
�A = Acción: Actividad o emoción que realiza o expresa el personaje (creando arte, protestando, etc.).

�SA = Estilo Artístico: Técnica y paleta de colores (negro y blanco, colores vibrantes, etc.).

�DA = Detalles y Accesorios: Elementos que añaden profundidad y contexto (ropa, símbolos, etc.).
�
�TC = Técnica y Composición: Método de representación visual (tinta y lápiz, digital, etc.).

Ejemplos: 

En Blanco y Negro (estilo ink + lápiz)
Create a black and white image of a humanoid mouse in a punk setting, embodying a strong sense of rebellion. The mouse stands in full attire, featuring worn-out punk clothing with patches, studs, and anarchist symbols. The environment is a testament to the mouse's punk lifestyle, with walls covered in graffiti, posters, and anarchistic sigils. The mouse's posture and facial expression exude confidence and a rebellious spirit, capturing the essence of punk anarchy. The scene should focus on the mouse's humanoid form, dressed in distinctive punk fashion, highlighting the textures of the clothing and the chaotic surroundings with ink and pencil techniques, all in stark black and white to emphasize the raw, gritty punk theme.

Create a black and white image of a humanoid rabbit in a chaotic room, heavily embodying punk rebellion. The rabbit stands full body, wearing worn punk clothing, complete with patches, piercings, and anarchist symbols. The environment reflects a high intensity of chaos and rebellion, with walls adorned with punk anarchist artwork and sigils. The rabbit's posture and expression exude a fierce independence and a rebellious spirit. The scene captures the essence of punk anarchy, focusing on the rabbit's humanoid features and attire, without additional bizarre or monstrous mutations. Use ink and pencil techniques to highlight the detailed textures of the clothing, the rabbit's features, and the chaotic background, maintaining a stark black and white contrast to emphasize the gritty essence of the punk theme.

Create a black and white image of a humanoid crow in a punk setting, exuding a strong punk rebellion vibe. The crow stands full body, adorned in worn punk attire, featuring jackets with patches, piercings, and anarchist symbols. The backdrop is a room filled with chaos and rebellion, walls covered in punk anarchist art and sigils. The crow's posture and expression should convey defiance and a rebellious spirit, capturing the essence of punk anarchy. The scene focuses on the crow's humanoid features, dressed in punk fashion, without the need for bizarre mutations. Use ink and pencil techniques to detail the clothing's texture, the crow's humanoid appearance, and the chaotic environment, all in stark black and white to emphasize the gritty punk theme.

Create a black and white image of a humanoid wolf in a punk environment, showcasing a strong sense of punk rebellion. The wolf is depicted full body, wearing distressed punk clothes, including a jacket with patches, chain accessories, and anarchist symbols. The setting is a chaotic room that serves as a testament to the wolf's rebellious lifestyle, with walls covered in punk art and anarchist sigils. The wolf's stance and expression should embody defiance and a fierce independent spirit. This image should focus on the wolf's humanoid form, dressed in punk fashion, without resorting to grotesque mutations. Employ ink and pencil techniques to bring out the textures of the clothing, the wolf's features, and the surrounding chaos, all in sharp black and white contrast to highlight the raw essence of punk anarchy.

Create a black and white image of a humanoid bear in a punk setting, fully embracing the punk rebellion ethos. The bear stands full body, clad in tattered punk gear, including a vest adorned with patches, belts, and anarchist symbols. The room around the bear is a haven of punk anarchy, with walls plastered in anarchist art and sigils, embodying a scene of chaos and rebellion. The bear's posture and gaze should convey a message of defiance and rugged independence. This illustration should highlight the bear's humanoid features, attired in distinctive punk fashion, without any bizarre mutations. Ink and pencil techniques should be used to detail the fabric textures, the bear's characteristics, and the chaotic environment, all in vivid black and white to accentuate the punk anarchist theme.

Prompts que Podrían Salir con Color
Anarchist artist in frenetic creation, merging punk and hippie styles in a melting environment, breaking labels. The scene shows chaos and transformation, with the artist appearing emaciated, angry, and deeply engaged in their art. The background has psychedelic patterns and surreal distortions, with a touch of color accentuating key features while primarily in ink and pencil style.

Anarchist artist laughing hysterically, merging rasta and hip hop elements in a chaotic, psychedelic background. The character is emaciated, displaying madness and creative liberation, with the environment featuring melting patterns and surreal distortions. The scene is predominantly in ink and pencil style with strategic uses of color to highlight the fusion of styles and intense emotion.

Anarchist artist in a moment of creative epiphany, where punk, hippie, rasta, and hip hop styles unite in an anarchic masterpiece. The character, emaciated and full of energy, represents the culmination of transformation and liberation. The background is a psychedelic explosion of colors and forms, blending all styles into a cohesive yet chaotic artwork. The piece primarily uses ink and pencil techniques, with vibrant color bursts to signify the peak of artistic and cultural fusion.

""" 

# Inicializar st.session_state
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = None  # Cambiado a None inicialmente
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

# Configuración inicial de Firestore
now = datetime.now()
collection_name = "Psycho_Prompter" + now.strftime("%Y-%m-%d")
document_name = st.session_state.get("user_uuid", str(uuid.uuid4()))
collection_ref = db.collection(collection_name)
document_ref = collection_ref.document(document_name)

# Gestión del Inicio de Sesión
if not st.session_state.get("logged_in", False):
    user_name = st.text_input("Introduce tu nombre para comenzar")
    confirm_button = st.button("Confirmar")
    if confirm_button and user_name:
        # Buscar en Firestore si el nombre de usuario ya existe
        user_query = db.collection("usuarios_pp").where("nombre", "==", user_name).get()
        if user_query:
            # Usuario existente encontrado, usar el UUID existente
            user_info = user_query[0].to_dict()
            st.session_state["user_uuid"] = user_info["user_uuid"]
            st.session_state["user_name"] = user_name
        else:
            # Usuario nuevo, generar un nuevo UUID
            new_uuid = str(uuid.uuid4())
            st.session_state["user_uuid"] = new_uuid
            user_doc_ref = db.collection("usuarios").document(new_uuid)
            user_doc_ref.set({"nombre": user_name, "user_uuid": new_uuid})
        st.session_state["logged_in"] = True

        # Forzar a Streamlit a reejecutar el script
        st.rerun()

# Solo mostrar el historial de conversación y el campo de entrada si el usuario está "logged_in"
if st.session_state.get("logged_in", False):
    st.write(f"Bienvenido de nuevo, {st.session_state.get('user_name', 'Usuario')}!")
    
    doc_data = document_ref.get().to_dict()
    if doc_data and 'messages' in doc_data:
        st.session_state['messages'] = doc_data['messages']
    
    with st.container(border=True):
        st.markdown("### Historial de Conversación")
        for msg in st.session_state['messages']:
            col1, col2 = st.columns([1, 5])
            if msg["role"] == "user":
                with col1:
                    st.markdown("**Tú 🧑:**")
                with col2:
                    st.info(msg['content'])
            else:
                with col1:
                    st.markdown("**IA 🤖:**")
                with col2:
                    st.success(msg['content'])

    prompt = st.chat_input("Escribe tu mensaje:", key="new_chat_input")
    if prompt:
        # Añadir mensaje del usuario al historial inmediatamente
        st.session_state['messages'].append({"role": "user", "content": prompt})
        
        # Mostrar spinner mientras se espera la respuesta del bot
        with st.spinner('El bot está pensando...'):
            user_name = st.session_state.get("user_name", "Usuario desconocido")
            internal_prompt = system_message + "\n\n"
            internal_prompt += "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state['messages'][-5:]])
            internal_prompt += f"\n\n{user_name}: {prompt}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[{"role": "system", "content": internal_prompt}],
                max_tokens=2000,
                temperature=0.80,
            )
        
        # La respuesta del bot se obtiene después de cerrar el spinner
        generated_text = response.choices[0].message.content
        
        # Añadir respuesta del bot al historial de mensajes
        st.session_state['messages'].append({"role": "assistant", "content": generated_text})
        document_ref.set({'messages': st.session_state['messages']})
        st.rerun()

# Gestión del Cierre de Sesión
if st.session_state.get("logged_in", False):
    if st.button("Cerrar Sesión"):
        keys_to_keep = []
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        st.write("Sesión cerrada. ¡Gracias por usar   Psycho_Prompter_Chatbot!")
        st.rerun()
