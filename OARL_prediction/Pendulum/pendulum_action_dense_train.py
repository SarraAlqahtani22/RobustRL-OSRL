#LIBRARIES
import numpy as np
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import LSTM, Dense, Input
from tensorflow.python.keras.models import Model, load_model, Sequential
import tensorflow as tf
from keras.utils import to_categorical
from keras.regularizers import l2
from keras.losses import kullback_leibler_divergence
from keras.losses import CategoricalCrossentropy
from scipy.spatial.distance import cosine
from sklearn.metrics import confusion_matrix,accuracy_score


#same results for same model, makes it deterministic
np.random.seed(1234)
tf.random.set_seed(1234)


#reading data
input = np.load("../Datasets/Pendulum_DDPG_transition.npy", allow_pickle=True)

#flattens and unpacks the np arrays
pre = np.concatenate(input[:,0]).ravel()
pre = np.reshape(pre, (pre.shape[0]//4,4))
action = np.concatenate(input[:,1]).ravel()
action = np.reshape(action, (action.shape[0]//1,1))
post = np.concatenate(input[:,2]).ravel()
post = np.reshape(post, (post.shape[0]//4,4))
done = np.concatenate(input[:,3]).ravel()
done = np.reshape(done, (done.shape[0]//1,1))

#re-concatenates them
data = np.column_stack((pre,action,post,done))

inputX = data[:,:4].astype('float64')
inputY = data[:,4:5].astype('float64')
print(inputX.shape)
print(inputY.shape)


trainX = inputX[:80000]
trainY = inputY[:80000]
valX = inputX[80000:]
valY = inputY[80000:]



es = EarlyStopping(monitor='val_mae', mode='min', verbose=1, patience=50)

# design network
model = Sequential()
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(16))
model.add(Dense(valY.shape[1]))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

# fit network
history = model.fit(trainX, trainY, epochs=5000, batch_size=5000, verbose=2,validation_data = (valX,valY),shuffle=False, callbacks=[es])

model.save('Pend_Action_Dense_Network1.keras')
print(model.summary())

np.save("history_Pend_Action_Dense_Network1.npy", history.history, allow_pickle=True)