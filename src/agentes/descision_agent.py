import chromadb
from chromadb.utils import embedding_functions
from semantic_kernel import Kernel


class DecisionSupportAgent:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.client = chromadb.Client()
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Configurar la base de datos vectorial (esto sería en la inicialización)
        self.collection = self.client.get_or_create_collection(
            name="emergency_plans",
            embedding_function=self.ef
        )
        
        # Aquí cargaríamos los documentos (esto sería parte de una función de inicialización)
        #plans = [...]  # Lista de planes de emergencia y papers
        #self.collection.add(
        #    documents=plans,
        #    ids=[str(i) for i in range(len(plans))]
        #)
    
    async def get_relevant_plans(self, situation_description):
        # Buscar en la base de datos vectorial
        results = self.collection.query(
            query_texts=[situation_description],
            n_results=3
        )
        
        # Procesar con Azure OpenAI para resumen ejecutivo
        prompt = f"""
        Resume los siguientes planes de emergencia relevantes para la situación:
        Situación: {situation_description}
        Planes encontrados: {results['documents']}
        
        Proporciona un resumen ejecutivo con:
        1. Acciones clave recomendadas
        2. Lecciones aprendidas de casos similares
        3. Consideraciones legales y éticas
        4. Pasos siguientes inmediatos
        """
        
        summary = await self.kernel.invoke_prompt(prompt)
        return summary