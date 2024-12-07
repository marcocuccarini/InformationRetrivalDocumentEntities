from Script.Varius import util
import pandas as pd


class Pipeline_Dataset_Creation:
  def __init__(self, model_doc, model_llama, index_document):
    
   self.document=model_doc.load_document(index_document)
   self.model_llama=model_llama
   self.model_doc=model_doc
   self.index_document=index_document
  

  def document_division(self):


    self.periods=self.model_doc.document_splitting("£")


  def df_encode(self,list_question,list_answer,list_answer_index,list_question_index):

    df=pd.DataFrame()
    df["question"]=list_question
    df["answer"]=list_answer
    df["question_index"]=list_question_index
    df["answer_index"]=list_answer_index
    df["document_index"]=[self.index_document]*len(list_answer)
    
    return df

  def question_creation(self):


    list_question=[]
    list_answer=[]
    list_question_index=[]
    list_answer_index=[]

    for i in range(len(self.periods)):


      #calcolo il numero di domande secondo il numero di frasi presenti nel periodo

      n_quest=max(1,len(util.split_into_sentences(self.periods[i]))-1)

      #verifico che il periodo abbia del testo

      if(len(self.periods[i])>0):

        #In base al numero di domande scelgo il prompt da dare
        #Cambia anche la funzione per raggruppare doamnda e risposta, nel ramo vero,
        #Avrò un unica domanda, nel ramo falso un multidomanda per ogni risposta

        if n_quest==1:
          prompt="Can you produce one question about this text without write anything more and with out any introduction? "+self.periods[i]
          output_model=self.model_llama.print_prompt(prompt)
          print(output_model)




          list_question.append(output_model)
          list_answer.append(self.periods[i])

          list_question_index.append(i)
          list_answer_index.append("O")

        else:

          prompt="Can you produce "+str(n_quest)+" differents questions about this text without write anything more separeted by the sign '£' with out any introduction? "+self.periods[i]
          output_model=self.model_llama.print_prompt(prompt)
          print(output_model)






          output_model_split=output_model.split("£")

          for j in range(len(output_model_split)):

            list_question.append(output_model_split[j])
            list_answer.append(self.periods[i])

            list_question_index.append(i)

            if(j):
              list_answer_index.append("C")
            else:
              list_answer_index.append("O")

    return self.df_encode(list_question,list_answer,list_question_index,list_answer_index)











       

          





           