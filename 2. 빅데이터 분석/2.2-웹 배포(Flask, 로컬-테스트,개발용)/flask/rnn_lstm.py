import tensorflow as tf
import numpy as np

text = open('./data/model/onepiece_text.txt', 'rb').read().decode(encoding='utf-8')
weight_path = './data/model/onepiece_w.h5'

def make_model(text, weight_path, batch_size=256, embedding_dim = 256, rnn_units = 1024):
    vocab = sorted(set(text))
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(len(vocab), embedding_dim,
                                  batch_input_shape=[1, None]),
        tf.keras.layers.LSTM(rnn_units,
                            return_sequences=True,
                            stateful=True,
                            recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(len(vocab))])

    model.load_weights(weight_path)

    model.build(tf.TensorShape([1, None]))
    return model, char2idx, idx2char

model, char2idx,idx2char = make_model(text, weight_path)

def generate_text(start_string):
    num_generate = 200
    
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    text_generated = []

    temperature = 0.2

    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))

if __name__ == '__main__':
    input_word = input()
    # module test code
    print(generate_text(start_string=u"{}".format(input_word)))