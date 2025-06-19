import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
tenant_id = os.getenv('AZURE_TENANT_ID')
redirect_uri = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:8501')

# URLs de Azure AD
authorize_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
userinfo_url = "https://graph.microsoft.com/oidc/userinfo"

# Verificar configuración
if not all([client_id, client_secret, tenant_id]):
    st.error("❌ Configura las variables de entorno de Azure AD")
    st.stop()

# Detectar código de retorno en la URL
params = st.query_params
code = params.get("code")

if "token" not in st.session_state and not code:
    # MOSTRAR ENLACE DE LOGIN
    oauth = OAuth2Session(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=['openid', 'email', 'profile'],
    )
    auth_url, _ = oauth.create_authorization_url(authorize_url)
    st.write("### Iniciar sesión con Azure AD")
    st.markdown(f"**[👆 Haz clic aquí para iniciar sesión]({auth_url})**")
    st.info("Después de iniciar sesión, serás redirigido aquí automáticamente.")
    st.stop()

elif code and "token" not in st.session_state:
    # PROCESAR CÓDIGO DE RETORNO
    st.info("Procesando autenticación...")
    try:
        oauth = OAuth2Session(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
        token = oauth.fetch_token(token_url, code=code)
        st.session_state["token"] = token
        st.query_params.clear()  # Limpia los parámetros de la URL
        st.success("¡Autenticación exitosa! Puedes usar la app.")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        if st.button("Reintentar"):
            st.query_params.clear()
            st.rerun()
        st.stop()

else:
    # USUARIO AUTENTICADO
    try:
        oauth = OAuth2Session(client_id=client_id, token=st.session_state["token"])
        userinfo = oauth.get(userinfo_url).json()
        st.success(f"¡Hola, {userinfo.get('name', 'usuario')}!")
        st.write(f"Email: {userinfo.get('email', 'No disponible')}")
        if st.button("Cerrar sesión"):
            del st.session_state["token"]
            st.query_params.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        if st.button("Reiniciar"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()