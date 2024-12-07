
import pandas as pd
import numpy as np

#Questa classe gestisce un interro documento, carica, lo divide in frasi e le codifica sencondo il contextual emebdding
class Document:

  def __init__(self, path, dataset_name):


    self.dataset_path = path + dataset_name


  #dato un indice carica un documento


  def load_document(self, index):

    data_set=pd.read_csv(self.dataset_path, sep=";")
    col_text=data_set['hotel_rule']

    self.document_text = col_text[index]


    return col_text[index].replace("\n","")


    #Divide il documento secondo lo splttitng character passato

  def document_splitting(self, splitting_character):

    self.splitting_character = splitting_character
    self.document_split=self.document_text.split(self.splitting_character)
    return self.document_split



  #codifica il document a seconda del modello presente nella istanza model:BERT


  def document_encoding(self, model_BERT):


    self.document_encode=model_BERT.text_emebedding(self.document_split)
    return self.document_encode



  def document_save(self):


    index=[i for i in range(len(self.document_encode))]


    array=np.array(self.document_split)
    array1=-np.array(self.document_encode)

    np.save('doc_sentece_encode.npy', array1)
    np.save('doc_sentence.npy', array)









    