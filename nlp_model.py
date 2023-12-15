# Machine Learning
from transformers import DistilBertTokenizer
import tensorflow as tf
from transformers import TFDistilBertModel
from transformers import TextClassificationPipeline
import numpy as np
import pandas as pd

NUM_CLASSES = 10

model = TFDistilBertModel.from_pretrained('distilbert-base-uncased', num_labels=NUM_CLASSES)

input_ids = tf.keras.layers.Input(shape=(512,), name='input_ids', dtype='int32')
attn_masks = tf.keras.layers.Input(shape=(512,), name='attention_mask', dtype='int32')
distilbert_embds = model.distilbert(input_ids, attention_mask=attn_masks)[0]

loaded_model = tf.keras.models.load_model('../Models/3_Epochs_NLP.h5', custom_objects={"TFDistilBertMainLayer": distilbert_embds})

tokenizer =  DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

def prepare_data(input_text, tokenizer):
    token = tokenizer.encode_plus(
        input_text,
        max_length=512,
        truncation=True,
        padding='max_length',
        add_special_tokens=True,
        return_tensors='tf'
    )
    return {
        'input_ids': tf.cast(token.input_ids, tf.float64),
        'attention_mask': tf.cast(token.attention_mask, tf.float64)
    }

classes =  ['Cardiovascular / Pulmonary',
 'Consult - History and Phy.',
 'ENT - Otolaryngology',
 'Gastroenterology',
 'Hematology - Oncology',
 'Neurology',
 'Obstetrics / Gynecology',
 'Ophthalmology',
 'Orthopedic',
 'Urology']