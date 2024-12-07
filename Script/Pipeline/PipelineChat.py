from Script.Varius import util
import pandas as pd
import numpy as np
from numpy.linalg import norm


#Questo oggetto predice dato un vettore di un documento già codificato predice la best answer 

class Pipeline_Chatbot:
  def __init__(self, model_BERT, question, path_doc, path_doc_vector, path_index):


    self.question=question
    self.model_BERT=model_BERT
    self.vector_doc=path_doc_vector
    self.question_encoded=model_BERT.text_emebedding(question)
    self.doc=path_doc

  def pred_best_answer(self):

    list_scores, list_answers_sort =zip(*sorted(zip(self.sentence_ranking("dist"),self.doc),reverse=True))
    return list_answers_sort[0]


  def sentence_ranking(self, distance_function):


    return [self.cosine_similarity(i, self.question_encoded) for i in self.vector_doc]


  def cosine_similarity(self, sentence, question):



    
    return np.dot(sentence, question)/(norm(sentence)*norm(question))







  def  distance_function(self, sentence, question):

    return np.dot(sentence, question)









    








           