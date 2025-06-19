import streamlit as st
from login import login_azure_ad
from azure.core.credentials import AccessToken, TokenCredential

# Llama al login y detén la app si el usuario no está autenticado
if not login_azure_ad():
    st.stop()

# Mensaje de bienvenida personalizado
st.title("👩‍🚒 Asistente de Incendios - Bienvenido")
st.markdown("""
¡Hola! Has accedido correctamente al Asistente de Incendios de FireWizard-Ai.

Aquí podrás consultar información y recibir ayuda especializada sobre la gestión y prevención de incendios. Si tienes alguna pregunta, escribe en el chat y nuestro asistente te responderá.
""")

# Permitir al usuario ingresar un token manualmente
st.subheader("Conexión a Azure AI")
user_token = st.text_input("Pega aquí tu token de acceso para Azure AI:", type="password")

if user_token:
    class MyTokenCredential(TokenCredential):
        def __init__(self, token):
            self._token = token
        def get_token(self, *scopes, **kwargs):
            return AccessToken(self._token, 9999999999)  # Expiry en epoch

    from azure.ai.projects import AIProjectClient
    from azure.ai.agents.models import ListSortOrder

    credential = MyTokenCredential(user_token)
    project = AIProjectClient(
        credential=credential,
        endpoint="https://euipo3.services.ai.azure.com/api/projects/firstProject")
    agent = project.agents.get_agent("asst_xle8aTkMbIqLPHxqjNZtfKUP")
    thread = project.agents.threads.get("thread_XQxMW54AGF76JC1tTEGQc8S7")

    # Campo de entrada del usuario
    user_input = st.chat_input("Consulta...")

    # Cuando el usuario envía un mensaje
    if user_input:
        # Crear el mensaje del usuario
        message = project.agents.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Ejecutar el agente
        run = project.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )

        if run.status == "failed":
            st.error(f"Run failed: {run.last_error}")
        else:
            messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

            for message in messages:
                if message.text_messages:
                    with st.chat_message("Assistant"):
                        st.write("Hello 👋")
                        st.write(message.text_messages[-1].text.value)
                        print(f"{message.role}: {message.text_messages[-1].text.value}")
else:
    st.info("Debes ingresar un token válido para conectarte a Azure AI.")


