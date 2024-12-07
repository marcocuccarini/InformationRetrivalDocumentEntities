
import pandas as pd
import json
import requests
from llama_index.llms.llama_api import LlamaAPI
from llama_index.core.llms import ChatMessage


#classe che gestisce il modello LLama 

class LLama_Model:


  #carica il modello 

  def __init__(self):

    api_key = "LL-7As6A60uUGdh8UCRpQpBmojyiTcERtTiKIGB4SXaEE3cqauDg3AZRnIyvahiakTc"
    self.llm = LlamaAPI(api_key=api_key)




    


  #Riceve in input un prompt e restituisce l'output del modello 


  def print_prompt(self,prompt):


    
 
    list_macro=[]

    messages = [ChatMessage(role="user", content=prompt),]


    resp = self.llm.chat(messages)
    res = json.loads(resp.json())
    return res['message']['content']



     

    