

class Local_LLama():

  def __init__(self):
    
    from llamaapi import LlamaAPI
    import json

    self.llama = llama = LlamaAPI('LL-7As6A60uUGdh8UCRpQpBmojyiTcERtTiKIGB4SXaEE3cqauDg3AZRnIyvahiakTc')


  def answer(self, question, text):

    
    #possible model



    api_request_json = {"model": "llama3-8b",
    "messages": [
    {"role": "system", "content": "Sei un assistente che mi spiega le regole di un hotel o struttura alberghiera."},
    {'role': 'user', 'content': "Rispondi in italiano a questa domanda " + question + " considerando questo testo:'"+ text + "'rispondendo brevemente, nel caso l'informazione non è presente rispondere con: 'L'informazione richiesta non è presnetente nel dataset'"}]}
    response = self.llama.run(api_request_json)
    return(json.dumps(response.json(), indent=2))
    #return response
    


