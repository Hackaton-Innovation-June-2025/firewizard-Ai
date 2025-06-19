from semantic_kernel import Kernel
import streamlit as st

class ResourceAllocationAgent:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        
    async def get_user_role(self):
        st.session_state.role = st.selectbox(
            "¿Cuál es su rol en la gestión de emergencias?",
            options=["Coordinador", "Bombero", "Logística", "Gobierno Local", "Protección Civil"]
        )
        return st.session_state.role
    
    async def recommend_allocation(self, risk_df, available_resources):
        role = st.session_state.get('role', await self.get_user_role())
        
        prompt = f"""
        Eres un experto en gestión de emergencias. Basado en:
        1. Tabla de riesgos: {risk_df.to_dict()}
        2. Recursos disponibles: {available_resources}
        3. Rol del usuario: {role}
        
        Proporciona recomendaciones específicas para:
        - Asignación de recursos (equipos, personal)
        - Rutas de evacuación óptimas
        - Puntos de reunión seguros
        - Coordinación con otras agencias
        
        Las recomendaciones deben ser accionables y específicas para el rol {role}.
        """
        
        recommendations = await self.kernel.invoke_prompt(prompt)
        return recommendations