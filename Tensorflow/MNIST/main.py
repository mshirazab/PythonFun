import tensorflow as tf
from keras.datasets import mnist
from keras.utils import np_utils
from matplotlib import pyplot

# get all images and make the data proper
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

# Inialize the X, weight and biases
X = tf.placeholder(tf.float32, [None, 28, 28, 1])
W = tf.Variable(tf.zeros([784, 10]))
B = tf.Variable(tf.zeros([10]))

# Intialize a placeholder to predict
Y = tf.nn.sigmoid(tf.matmul(tf.reshape(X, [-1, 784]), W) + B)
Y_ = tf.placeholder(tf.float32, [None, 10])

init = tf.initialize_all_variables()
cross_entropy = -tf.reduce_sum(Y_*tf.log(Y + 1e-10))
isCorrect = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(isCorrect, tf.float32))
optimizer = tf.train.GradientDescentOptimizer(0.0003)
train_step = optimizer.minimize(cross_entropy)

sess = tf.Session()
sess.run(init)

for i in range(600):
    train_data = {X: X_train[i*1000:(i+1)*1000],
                  Y_: Y_train[i*1000:(i+1)*1000]}
    sess.run(train_step, feed_dict=train_data)
    test_data = {X: X_test, Y_: Y_test}
    c = sess.run(accuracy, feed_dict=test_data)
    print c
