import streamlit as st
from streamlit_folium import folium_static
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from agentes.fire_agent import FirePredictionAgent
from agentes.risk_agent import RiskAssessmentAgent
from agentes.resource_agent import ResourceAllocationAgent
from agentes.descision_agent import DecisionSupportAgent


def main():
    # Configuración inicial
    st.title("Sistema Multiagente para Gestión de Incendios Forestales")
    
    # Inicializar Kernel Semantic
    kernel = Kernel()
    #kernel(
    #    "azure_openai",
    #    AzureChatCompletion(
    #        deployment_name="your-deployment-name",
    #        endpoint="your-azure-openai-endpoint",
    #        api_key="your-api-key"
    #    )
    #)
    
    # Inicializar agentes
    fire_agent = FirePredictionAgent(kernel)
    risk_agent = RiskAssessmentAgent(kernel)
    resource_agent = ResourceAllocationAgent(kernel)
    decision_agent = DecisionSupportAgent(kernel)
    
    # Interfaz de usuario
    tab1, tab2, tab3, tab4 = st.tabs([
        "Predicción", "Evaluación de Riesgos", 
        "Asignación de Recursos", "Toma de Decisiones"
    ])
    
    with tab1:
        st.header("Predicción de Propagación de Incendios")
        location = st.text_input("Ubicación del incendio (lat, long)", "37.7749, -122.4194")
        weather_data = st.text_area("Datos meteorológicos actuales")
        terrain_data = st.text_area("Datos del terreno")
        
        if st.button("Predecir propagación"):
            #prediction, fire_map = await fire_agent.predict_fire_spread(
            #    location, weather_data, terrain_data
            #)
            #st.write(prediction)
           #folium_static(fire_map)
           pass
    
    with tab2:
        st.header("Evaluación de Riesgos")
        radius = st.slider("Radio de evaluación (km)", 1, 50, 10)
        
        if st.button("Evaluar riesgos"):
            #risk_df = await risk_agent.assess_risks(location, radius)
            
            #st.dataframe(risk_df)
            
            # Gráfico de riesgos
            #fig, ax = plt.subplots()
            #risk_df.set_index('Sector')['Riesgo Total'].plot(kind='bar', ax=ax)
            #st.pyplot(fig)
            st.write("hola")
    
    with tab3:
        st.header("Asignación de Recursos y Evacuación")
        resources = st.text_area("Recursos disponibles (formato JSON)")
        
        if st.button("Generar recomendaciones"):
            ##recommendations = await resource_agent.recommend_allocation(risk_df, resources)
            ##st.write(recommendations)
            pass
    
    with tab4:
        st.header("Apoyo a la Toma de Decisiones")
        situation = st.text_area("Describa la situación actual")
        
        if st.button("Buscar planes relevantes"):
            #summary = await decision_agent.get_relevant_plans(situation)
            #st.write(summary)
            pass

if __name__ == "__main__":
    main()