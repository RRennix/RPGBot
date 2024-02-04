from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from googletrans import Translator
model_name = "microsoft/DialoGPT-large"
#model_name = "microsoft/DialoGPT-medium"
# model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
translator = Translator()
def bot(mensagem):
  for step in range(1):
      text = translator.translate(mensagem, dest='en').text
      input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
      bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids
      chat_history_ids_list = model.generate(
          bot_input_ids,
          max_length=1000,
          do_sample=True,
          top_p=0.95,
          top_k=50,
          temperature=1,
          num_return_sequences=1,
          pad_token_id=tokenizer.eos_token_id
      )
      for i in range(len(chat_history_ids_list)):
        mensagem = translator.translate(tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True), dest='pt').text
      chat_history_ids = torch.unsqueeze(chat_history_ids_list[0], dim=0)
      return mensagem