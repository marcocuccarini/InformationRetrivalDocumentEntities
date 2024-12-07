class Local_LLama():

  def __init__(self):
    
    import ollama

    self.client = ollama.Client(host="http://127.0.0.1:11434")





  def print_prompt(self, prompt):

    
   
    from langdetect import detect





    response = self.client.chat (model='llama3.1', messages=[
      {'role': 'system', 'content': 'You are  assistant that answers the request of the user',
      'role': 'user', 'content': prompt}

    ])


    if 'message' in response and 'content' in response['message']: 
      return response['message']['content'].strip()


    else:


      return "Non posso rispondere alla domanda."


