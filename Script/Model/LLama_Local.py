class Local_LLama():

  def __init__(self):
    
    import ollama

    self.client = ollama.Client(host="http://127.0.0.1:11434")





  def answer(self, question, text):

    
    #possible model
    #llama3
    dictionary= {
            'en': 'English', 
            'es': 'Spanish', 
            'it': 'Italian',
            'fr': 'French',
            'de': 'German',
            'pt': 'Portuguese',
            'ru': 'Russian'
          }

    from langdetect import detect

    if detect(question) in dictionary:

      leng=dictionary[detect(question)]

    else:

      leng="English"




    response = self.client.chat (model='llama3', messages=[
      {'role': 'system', 'content': 'You are  assistant that answers the question in '+leng,
      'role': 'user', 'content': "Answer to the question: '" + question + "' considering the text:'"+ text + "' in " +leng+". Just write the answer. In case the information is not present answer with: 'The information is not provided by the document'."}

    ])


    if 'message' in response and 'content' in response['message']: 
      return response['message']['content'].strip()


    else:


      return "Non posso rispondere alla domanda."


