from semantic_kernel import Kernel
import pandas as pd

class RiskAssessmentAgent:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.risk_model = self._load_risk_model()
        
    def _load_risk_model(self):
        # Modelo matemático para evaluación de riesgos
        # Podría ser un modelo de regresión, red neuronal, etc.
        return lambda infra, natural, community: 0.4*infra + 0.3*natural + 0.3*community
    
    async def assess_risks(self, location, radius_km):
        # Consultar Azure Maps/OpenStreetMap para infraestructura
        infra_prompt = f"""
        Consulta Azure Maps para la ubicación {location} con radio {radius_km}km.
        Identifica:
        1. Infraestructura crítica (hospitales, escuelas, plantas de energía)
        2. Carreteras principales
        3. Áreas residenciales
        Proporciona datos cuantificables.
        """
        infra_data = await self.kernel.invoke_prompt(infra_prompt)
        
        # Consultar recursos naturales
        natural_prompt = f"""
        Consulta bases de datos ecológicas para {location} con radio {radius_km}km.
        Identifica:
        1. Áreas protegidas
        2. Especies en peligro
        3. Recursos hídricos
        4. Tipos de vegetación
        """
        natural_data = await self.kernel.invoke_prompt(natural_prompt)
        
        # Consultar datos de comunidades
        community_prompt = f"""
        Obtén datos demográficos para {location} con radio {radius_km}km.
        Incluye:
        1. Población total
        2. Densidad poblacional
        3. Centros de evacuación
        4. Comunidades vulnerables
        """
        community_data = await self.kernel.invoke_prompt(community_prompt)
        
        # Calcular riesgos
        risk_table = []
        for sector in infra_data.sectors:
            risk_score = self.risk_model(
                infra_data.sectors[sector].value,
                natural_data.impact_values[sector],
                community_data.vulnerability[sector]
            )
            risk_table.append({
                "Sector": sector,
                "Infraestructura": infra_data.sectors[sector].value,
                "Recursos Naturales": natural_data.impact_values[sector],
                "Comunidad": community_data.vulnerability[sector],
                "Riesgo Total": risk_score,
                "Recomendación": "Alta prioridad" if risk_score > 0.7 else "Media prioridad" if risk_score > 0.4 else "Baja prioridad"
            })
        
        return pd.DataFrame(risk_table)