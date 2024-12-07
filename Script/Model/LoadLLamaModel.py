
from transformers import GenerationConfig
from unsloth import FastLanguageModel


#classe che gestisce il modello LLama 

class LLama_Model:


  #carica il modello 

  def __init__(self, max_seq_length, dtype,load_in_4bit, model_name, max_new_tokens):


    self.max_seq_length = max_seq_length # Choose any! Unsloth supports RoPE Scaling internally!
    self.dtype = dtype # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
    self.load_in_4bit = load_in_4bit # Use 4bit quantization to reduce memory usage. Can be False.
    self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                                        model_name = model_name,
                                        max_seq_length = max_seq_length,
                                        dtype = dtype,
                                        load_in_4bit = load_in_4bit)

    gen_kwargs = {"max_new_tokens": max_new_tokens}
    self.generation_config = GenerationConfig(**gen_kwargs)


  #Riceve in input un prompt e restituisce l'output del modello 


  def print_prompt(self,prompt):

    inputs = self.tokenizer(prompt, return_tensors="pt",  max_length=2048, truncation=True)
    outputs = self.model.generate(input_ids=inputs["input_ids"].to("cuda"), generation_config=self.generation_config)
    return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


     

    