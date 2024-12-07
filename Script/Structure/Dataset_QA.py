
import pandas as pd
import numpy as np


class Dataset_QA:

  def __init__(self, path, llama_model, index):
    
    self.dataset_path = path
    self.model_llama=llama_model
    self.index_document=index




  def load_dataset(self):

    self.dataset=pd.read_csv(self.dataset_path, sep=",")
    return self.dataset


  def df_encode_quest(self, list_question, list_answer, list_answer_reformulate, list_question_index, list_answer_index):
    
    df=self.dataset
    df["question"]=list_question
    df["answer"]=list_answer
    df["question_index"]=list_question_index
    df["question_reformulate"]=list_answer_reformulate
    df["answer_index"]=list_answer_index
    df["document_index"]=[self.index_document]*len(list_answer)

    #for i in range(len(list_answer_reformulate[0])):

      #df["reformulate_question_"+str(i)]=list(np.array(list_answer_reformulate)[:,i])



    self.dataset=df


    
    return df


  def df_encode_answer(self, list_question, list_answer, list_answer_reformulate, list_question_index, list_answer_index):

    df=pd.DataFrame()
    df["question"]=list_question
    df["answer"]=list_answer
    df["question_index"]=list_question_index
    df["answer_reformulate"]=list_answer_reformulate
    df["answer_index"]=list_answer_index
    df["document_index"]=[self.index_document]*len(list_answer)

    #for i in range(len(list_answer_reformulate[0])):

      #df["reformulate_answer_"+str(i)]=list(np.array(list_answer_reformulate)[:,i])



    self.dataset=df


    
    return df


  def question_augmentation(self, n):

    list_question=[]
    list_answer=[]
    list_answer_reformulate=[]
    list_question_index=[]
    list_answer_index=[]

    #len(self.dataset['question'])

    for i in range(len(self.dataset['question'])):

        
      prompt="Can you reformulate this question in " + str(n) + " different ways changing the lexicon of the text, separated by the sign '£' without writing anything more and without any introduction? "+self.dataset['question'][i]
      output_model=self.model_llama.print_prompt(prompt)

      print(i)



      output_model_split=output_model.split("£")
      list_question.append(self.dataset['question'][i])
      list_answer.append(self.dataset['answer'][i])

      list_question_index.append(i)
      list_answer_index.append(self.dataset['answer_index'][i])


      list_10_answer=[]

      for j in range(len(output_model_split)):

        if j:

          list_10_answer.append(output_model_split[j])

      list_answer_reformulate.append(list_10_answer)



    return self.df_encode_quest(list_question, list_answer, list_answer_reformulate, list_question_index, list_answer_index)



  def period_augmentation(self, n):

    list_question=[]
    list_answer=[]
    list_answer_reformulate=[]
    list_question_index=[]
    list_answer_index=[]

    #len(self.dataset['question'])

    for i in range(len(self.dataset['question'])):

      if (self.dataset['question_index'][i]=="O"):
        
        prompt="Can you reformulate this text in " + str(n) + " different ways changing the lexicon of the text separated by the sign '£' without writing anything more and without any introduction? "+self.dataset['answer'][i]
        output_model=self.model_llama.print_prompt(prompt)
        print(i)


      #output_model="Cia £ Cia £ Cia"



      output_model_split=output_model.split("£")
      list_question.append(self.dataset['question'][i])
      list_answer.append(self.dataset['answer'][i])

      list_question_index.append(i)
      list_answer_index.append(self.dataset['answer_index'][i])


      list_10_answer=[]

      for j in range(len(output_model_split)):

        if j:

          list_10_answer.append(output_model_split[j])

      list_answer_reformulate.append(list_10_answer)





       

    return self.df_encode_answer(list_question, list_answer, list_answer_reformulate, list_question_index, list_answer_index)


















    