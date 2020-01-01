import tensorflow as tf
from functools import partial
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import pickle
import time


params = {
    'dim' : 300,            # dimension of embeddings
    'maximum_steps' : 1000, # number of training steps
    'lstm_size' : 150,      # dimension of LSTM
    'batch_size' : 25,      # batch size
    'max_words' : 10000,    # maximum number of words to embed
    'padding_size' : 20,    # maximum sentence size
    'num_classes' : 14,     # number of unique classes
    'save_dir' : 'test_model/' # directory to save hash tables, model weights, etc.
}


def save_obj(directory, obj, name):
    '''Helper function using pickle to save and load objects'''
    with open(directory + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(directory, name):
    '''Helper function using pickle to save and load objects'''
    with open(directory + name + ".pkl", "rb") as f:
        return pickle.load(f)


def load_data(file="/data_train/data_loc_train.txt"):
    '''Helper function to load and transform inputs and labels
    included as a separate function due to NER-specific evaluation needs:
        tensorflow does not have multi-class precision/accuracy as a metric
        so data_y is needed to manually calculate evaluations'''
    file = open(file, 'r', encoding="UTF-8")
    sentence, labels = [], []
    data_x, data_y = [], []
    for line in file:
        line = line.strip("\n").split("\t")

        # lines with len > 1 are words
        if len(line) > 1:
            sentence.append(line[1])
            labels.append(line[0][2:]) if len(line[0]) > 1 else labels.append(line[0])

        # lins with len == 1 are sentence breaks
        if len(line) == 1:
            data_x.append(' '.join(sentence))
            data_y.append(labels)
            sentence, labels = [], []
    return data_x, data_y


def make_tokenizer(file="data_train/data_loc_train.txt", params=params):
    ''' In order for one hot encoding of words and labels to work,
    every word and label has to be seen at least once to make a hashing table.
    This function outputs hash tables for the words and the labels
    that can be used to one-hot-encode them in the generator
    '''
    # Load parameters and data
    max_words = params['max_words']
    padding_size = params['padding_size']
    save_dir = params['save_dir']
    data_x, data_y = load_data(file)

    # Use the Keras tokenizer API to generate hashing table for data_x
    tokenizer = Tokenizer(num_words=max_words)

    tokenizer.fit_on_texts(data_x)
    word_index = tokenizer.word_index

    # Flatten data_y and create hashing table using set logic
    data_y_flattened = [item for sublist in data_y for item in sublist]
    data_x_flattened = [item for sublist in data_x for item in sublist]

    labels_index = dict([(y, x + 1) for x, y in enumerate(sorted(set(data_y_flattened)))])
    labels = []
    for item in data_y:
        labels.append([labels_index.get(i) for i in item])
    labels_lookup = {v: k for k, v in labels_index.items()}  # reverse dictionary for lookup
    # save hash tables to disk for model serving
    for item, name in zip([word_index, labels_index, labels_lookup],
                          ["word_index", "labels_index", "labels_lookup"]):
        save_obj(save_dir, item, name)
    return word_index, labels_index, labels_lookup


word_index, labels_index, labels_lookup = make_tokenizer()


def generate_batches(file="data_train/data_loc_train.txt", params=params, train=True):
    ''' Generate minibatch with dimensions:
    batch_x : (batch_size, max_len)
    lengths : (batch_size,)
    batch_y : (batch_size, num_classes)

    file : path to .txt containing training data in BIO format
    '''

    batch_size = params['batch_size']
    max_len = params['padding_size']
    save_dir = params['save_dir']

    # load hash tables for tokenization
    for item, name in zip([word_index, labels_index, labels_lookup],
                          ["word_index", "labels_index", "labels_lookup"]):
        item = load_obj(save_dir, name)

    while True:
        with open(file, 'r') as f:
            batch_x, lengths, batch_y = [], [], []
            words, labels = [], []
            for line in f:
                line = line.strip("\n").split("\t")
                # lines with len > 1 are words
                if len(line) > 1:
                    labels.append(line[0][2:]) if len(line[0]) > 1 else labels.append(line[0])
                    words.append(line[1])

                # lines with len == 1 are breaks between sentences
                if len(line) == 1:
                    words = [word_index.get(x) if x in word_index.keys() else 0 for x in words]
                    labels = [labels_index.get(y) for y in labels]
                    batch_x.append(words)
                    batch_y.append(labels)
                    lengths.append(min(len(words), max_len))
                    words, labels = [], []

                if len(batch_x) == batch_size:
                    batch_x = pad_sequences(batch_x, maxlen=max_len, value=0, padding="post")
                    batch_y = pad_sequences(batch_y, maxlen=max_len, value=0, padding="post")
                    yield (batch_x, lengths), batch_y
                    batch_x, lengths, batch_y = [], [], []
            if train == False:
                break


def input_fn(file, params=None, train=True):
    params = params if params is not None else {}
    shapes = (([None, None], [None]), [None, None])  # batch_x, lengths, batch_y shapes
    types = ((tf.int32, tf.int32), tf.int32)  # batch_x, lengths, batch_y data types

    generator = partial(generate_batches, file, train=train)
    dataset = tf.data.Dataset.from_generator(generator, types, shapes)
    return dataset


# For model serving, we need a serving function that will feed tf.placeholders
def serving_input_fn():
    words = tf.placeholder(dtype=tf.int32, shape=[None, None], name='words')
    length = tf.placeholder(dtype=tf.int32, shape=[None], name='length')
    receiver_tensors = {'words': words, 'length': length}
    features = {'words': words, 'length': length}
    return tf.estimator.export.ServingInputReceiver(features, receiver_tensors)


def model_fn(features, labels, mode, params=params):
    # import the data and unpack the features
    # serving input_fn returns a dict, convert to multivalue obj
    if isinstance(features, dict):
        features = features['words'], features['length']

    words, length = features

    # Embedding
    embedding = tf.Variable(tf.random.normal([params['max_words'], params['dim']]))
    embedding_lookup_for_x = tf.nn.embedding_lookup(embedding, words)

    # LSTM
    lstm_cell_fw = tf.compat.v1.nn.rnn_cell.BasicLSTMCell(params['lstm_size'], state_is_tuple=True)
    lstm_cell_bw = tf.compat.v1.nn.rnn_cell.BasicLSTMCell(params['lstm_size'], state_is_tuple=True)
    states, final_state = tf.compat.v1.nn.bidirectional_dynamic_rnn(
        lstm_cell_fw,
        cell_bw=lstm_cell_bw,
        inputs=embedding_lookup_for_x,
        dtype=tf.float32,
        time_major=False,
        sequence_length=length)
    lstm_out = tf.concat([states[0], states[1]], axis=2)

    # Conditional random fields
    logits = tf.compat.v1.layers.dense(lstm_out, params['num_classes'])
    crf_params = tf.compat.v1.get_variable("crf", [params['num_classes'], params['num_classes']],
                                 dtype=tf.float32)
    pred_ids, _ = tf.contrib.crf.crf_decode(logits, crf_params, length)
    training = (mode == tf.estimator.ModeKeys.TRAIN)

    # Prediction
    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = {
            'pred_ids': pred_ids,
            'tags': words,
            'length': length,
        }
        export_outputs = {
            'prediction': tf.estimator.export.PredictOutput(predictions)
        }

        return tf.estimator.EstimatorSpec(mode, predictions=predictions,
                                          export_outputs=export_outputs)

    # Loss functions and optimizers
    log_likelihood, _ = tf.contrib.crf.crf_log_likelihood(
        logits, labels, length, crf_params)

    loss = tf.reduce_mean(-log_likelihood)
    train_op = tf.train.AdamOptimizer().minimize(
        loss, global_step=tf.train.get_or_create_global_step())

    # Training
    if mode == tf.estimator.ModeKeys.TRAIN:
        return tf.estimator.EstimatorSpec(mode=mode,
                                          loss=loss,
                                          train_op=train_op)
config = tf.estimator.RunConfig()
estimator = tf.estimator.Estimator(model_fn, 'test_model/model', config, params)

# Create extract_xpath spec
train_input_fn = partial(input_fn, "data_train/data_loc_train.txt", params = params)
train_spec = tf.estimator.TrainSpec(train_input_fn)

# Create evaluation spec
eval_input_fn = partial(input_fn, "data_train/data_loc_train.txt", params = params, train = False)
eval_spec = tf.estimator.EvalSpec(eval_input_fn)

ts = time.time()
estimator.train(input_fn = train_input_fn, max_steps = 1000)
te = time.time()
print("Completed in {} seconds".format(int(te - ts)))
estimator.export_savedmodel('test_model/saved_model/', serving_input_fn)