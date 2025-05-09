import os
from openai import AzureOpenAI  
from azure.identity import DefaultAzureCredential, get_bearer_token_provider  
  
endpoint = os.getenv("ENDPOINT_URL", "https://isaac-mah6w1z5-eastus2.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")
  
# Initialize Azure OpenAI client with Entra ID authentication  
cognitiveServicesResource = os.getenv('AZURE_COGNITIVE_SERVICES_RESOURCE', 'YOUR_COGNITIVE_SERVICES_RESOURCE')  
token_provider = get_bearer_token_provider(  
    DefaultAzureCredential(),  
    f'{cognitiveServicesResource}.default'  
)  
        
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    azure_ad_token_provider=token_provider,  
    api_version='2024-05-01-preview',  
)  
       
completion = client.chat.completions.create(  
    model=deployment,  
    messages=[
    {
        "role": "system",
        "content": "Você é um especialista em NLP focado em ferramentas de tradução automática que utilizam LLM/NMT como base e você irá me ajudar com dúvidas sobre o tema."
    },
    {
        "role": "user",
        "content": "Como o contexto é considerado no momento de traduzir conjuntos de dados? Quais os desafios para essas ferramentas?"
    },
    {
        "role": "assistant",
        "content": "O contexto é considerado na tradução de conjuntos de dados por meio da aplicação de abordagens empíricas baseadas em evidências, como a organização e categorização dos dados textuais de acordo com variáveis contextuais, incluindo gênero discursivo, registro, campo temático, situação comunicativa e perfil sociolinguístico dos falantes. Esse processo permite investigar como diferentes aspectos do contexto influenciam a frequência, distribuição e combinação de unidades linguísticas, como palavras, colocações e padrões discursivos [doc2].\n\nOs desafios enfrentados pelas ferramentas de tradução automática incluem a dificuldade de traduzir expressões multipalavras (EMPs), especialmente as menos transparentes (EMPs NC - não convencionais). Estudos indicam que sistemas como Google Tradutor e ChatGPT-3 apresentam desempenho inferior na tradução de EMPs NC em comparação com EMPs PC (convencionais). Isso se deve ao caráter menos transparente das EMPs NC, que dificulta a correspondência com os equivalentes idiomáticos e contextuais na língua-alvo [doc3]."
    }
],  
    past_messages=10,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,  
    stop=None,  
    extra_body={  
        "data_sources": [  
            {  
                "type": "azure_search",  
                "parameters": {  
                    "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],  
                    "index_name": os.environ["AZURE_AI_SEARCH_INDEX"],  
                    "authentication": {  
                        "type": "system_assigned_managed_identity"  
                    }  
                }  
            }  
        ]  
    }  
)

print(completion.model_dump_json(indent=2))  
