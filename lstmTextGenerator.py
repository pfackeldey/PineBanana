import numpy as np
import sys
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import BulkWriteError
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

# DB Import
# configure mongoDB TODO: MongoConfig auslagern
client = MongoClient("localhost:27017")
db=client.PineBanana
serverStatusResult=db.command("serverStatus")

# TODO: Connect MongoDB clean collection to lstm trainer

data = open(path).read().lower()
if sys.version_info < (3, 0):
    # for use of python 2
    text = text.translate(None, "%&*;<>[]_`{|}~")
else:
    # python 3
    text = text.translate(str.maketrans("%&*;<>[]_`{|}~", "              "))
print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 24
step = 2
tweets = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    tweets.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(tweets))
# print(next_chars)

print('Vectorization...')
X = np.zeros((len(tweets), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(tweets), len(chars)), dtype=np.bool)
for i, tweet in enumerate(tweets):
    for t, char in enumerate(tweet):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


# train the model, output generated text after each iteration
for iteration in range(1, 50):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y,
              batch_size=94,
              epochs=2)

    start_index = random.randint(0, len(text) - maxlen - 1)

    for diversity in [0.3, 0.4, 0.5, 0.6]:
        print()
        print('----- diversity:', diversity)

        generated = ''
        tweet = text[start_index: start_index + maxlen]
        generated += tweet
        print('----- Generating with seed: "' + tweet + '"')
        sys.stdout.write(generated)

        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(tweet):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            generated += next_char
            tweet = tweet[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
