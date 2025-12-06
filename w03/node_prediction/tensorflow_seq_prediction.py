import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# import the text data from node_seq_data.txt into a data variable
# replace ::3.0 and ::2.0 with empty string
with open('node_seq.txt', 'r') as file:
    data = file.readlines()
    data = [line.replace('::3.0', '').replace('::2.0', '').strip() for line in data]

# print (f'Total sequences: {len(data)}')

# # print all lines
# for line in data:
#     print(line)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(data)
sequences = tokenizer.texts_to_sequences(data)
vocab_size = len(tokenizer.word_index) + 1

input_sequences = []
for seq in sequences:
    for i in range(1, len(seq)):
        n_gram_sequence = seq[:i+1]
        input_sequences.append(n_gram_sequence)
        
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

X, y = input_sequences[:,:-1], input_sequences[:,-1]
y = np.array(y)

model = Sequential([
    Embedding(vocab_size, 10, input_length=max_sequence_len-1),
    LSTM(100, return_sequences=False),
    Dense(vocab_size, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, y, epochs=50, verbose=2)

def predict_next_node(seed_text, num_words=1):
    for _ in range(num_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = model.predict(token_list, verbose=0)
        predicted_word_index = np.argmax(predicted, axis=1)[0]
        
        for word, index in tokenizer.word_index.items():
            if index == predicted_word_index:
                seed_text += ' ' + word
                break
    return seed_text

print(predict_next_node("alembic unpack normal", num_words=3))