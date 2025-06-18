from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import streamlit as st

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://euipo3.services.ai.azure.com/api/projects/firstProject")

agent = project.agents.get_agent("asst_xle8aTkMbIqLPHxqjNZtfKUP")

thread = project.agents.threads.get("thread_XQxMW54AGF76JC1tTEGQc8S7")

st.title("Asistente de incendios")

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
        print(f"Run failed: {run.last_error}")
    else:
        messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

        for message in messages:
            if message.text_messages:
                with st.chat_message("Assistant"):
                    st.write("Hello 👋")
                    st.write(message.text_messages[-1].text.value)
                    print(f"{message.role}: {message.text_messages[-1].text.value}")


