import torch

from torch.utils.data import Dataset



class AustenDataset(Dataset):
  def __init__(self, sentences, tokenizer, max_length=768, gpt2_type="gpt2"):
    self.tokenizer = tokenizer
    self.input_ids = []
    self.attn_masks = []

    for sentence in sentences:

     # encodings_dict = tokenizer("<|startoftext|>"+sentence["sentence"]+"<|endoftext|>",
      #                           truncation=True,
       #                          max_length=max_length,
        #                         padding="max_length")
      
      #use fasttokenizer to use the return_overflow_tokens options to chunk and tokenize long input sequences
      encodings_dict = tokenizer("<|startoftext|>"+sentence["sentence"]+"<|endoftext|>",
                                 truncation=True,
                                 max_length=max_length,
                                 return_overflowing_tokens=True,
                                 return_length= True,
                                 padding="max_length")
      
      #add encodings in the right format for training
      if len(encodings_dict["input_ids"]) > 1:
        for inputs, masks in zip(encodings_dict["input_ids"], encodings_dict["attention_mask"]):
          self.input_ids.append(torch.tensor([inputs]).squeeze())
          self.attn_masks.append(torch.tensor([masks]).squeeze())
      else:
        self.input_ids.append(torch.tensor(encodings_dict["input_ids"]).squeeze())
        self.attn_masks.append(torch.tensor(encodings_dict["attention_mask"]).squeeze())
    
  def __len__(self):
    return len(self.input_ids)

  def __getitem__(self, idx):
    return self.input_ids[idx], self.attn_masks[idx]