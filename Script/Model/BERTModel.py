

class BERT_Model:

  def __init__(self, model_name, SentenceTransformer):


    self.model_name = model_name
    self.model=SentenceTransformer(self.model_name)





  def text_emebedding(self, text):


    return self.model.encode(text, convert_to_tensor=False)


