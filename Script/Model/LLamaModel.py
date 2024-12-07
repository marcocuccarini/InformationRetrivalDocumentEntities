

import transformers
import torch
import json


#classe che gestisce il modello LLama

class LLama_Model:


  #carica il modello

  def __init__(self):


    self.model_id="meta-llama/Meta-Llama-3-8B-Instruct"

    self.pipeline= transformers.pipeline("text-generation",
          model=self.model_id,
          model_kwargs={"torch_dtype": torch.bfloat16},
          device_map="auto",)

#Riceve in input un prompt e restituisce l'output del modello


  def print_prompt(self,prompt):




    list_macro=[]

    self.messages = [
    {"role": "system", "content": "You are a system that aswer to my request!"},
    {"role": "user", "content": prompt},]

    self.terminators = [self.pipeline.tokenizer.eos_token_id,
                        self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")]

    self.outputs = self.pipeline(self.messages,
                            max_new_tokens=256,
                            eos_token_id=self.terminators,
                            do_sample=True,
                            temperature=0.6,
                            top_p=0.9)





    return self.outputs[0]['generated_text'][2]['content']

    