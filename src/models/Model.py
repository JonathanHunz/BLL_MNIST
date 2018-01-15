import time
import tensorflow as tf
import matplotlib.pyplot as plt

# Define constants
learning_rate = 0.00001
log_path = "../../logs/Model1/" + time.strftime("%Y-%m-%d_%H-%M-%S")

# Read input data
# Create reader and read serialized example from files in filename_queue
reader = tf.TFRecordReader()
filename_queue = tf.train.string_input_producer(["../../data/processed/mnist.tfrecords"])
_, serialized_example = reader.read(filename_queue)

feature_set = {
    'image': tf.FixedLenFeature([], tf.string),
    'label': tf.FixedLenFeature([], tf.int64)
}

# Read features
features = tf.parse_single_example(serialized_example, features=feature_set)
label_feature, image_feature = features['label'], features['image']

# One hot encode labels
label_feature = tf.one_hot(label_feature, 10)

# Decode and reshape image feature
image_feature = tf.decode_raw(image_feature, tf.float32)
image_feature = tf.reshape(image_feature, [784])

# Batching
images, labels = tf.train.shuffle_batch([image_feature, label_feature], batch_size=64, capacity=50000, num_threads=2, min_after_dequeue=10000)

# Build graph
# Create input and output placeholders
X = tf.placeholder(tf.float32, [None, 784], "X")
Y = tf.placeholder(tf.float32, [None, 10], "Y")

# Initialize weights
w_h1 = tf.Variable(tf.random_normal([784, 625], stddev=0.01), name="w_h1")  # Layer 1
w_h2 = tf.Variable(tf.random_normal([625, 625], stddev=0.01), name="w_h2")  # Layer 2
w_o = tf.Variable(tf.random_normal([625, 10], stddev=0.01), name="w_o")  # Output layer

# Define model
with tf.name_scope("hidden_1"):
    X = tf.nn.dropout(X, 0.7)
    h1 = tf.nn.relu(tf.matmul(X, w_h1))
with tf.name_scope("hidden_2"):
    h1 = tf.nn.dropout(h1, 0.5)
    h2 = tf.nn.relu(tf.matmul(h1, w_h2))
with tf.name_scope("output"):
    h2 = tf.nn.dropout(h2, 0.5)
    p_y = tf.matmul(h2, w_o)

# Define cost function
with tf.name_scope("cost"):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=p_y, labels=Y))
    # Define train operation
    train = tf.train.RMSPropOptimizer(learning_rate).minimize(cost)
    # Add summary to cost tensor
    tf.summary.scalar("cost", cost)

# Accuracy function
with tf.name_scope("accuracy"):
    #  Count correct predictions
    correct_pred = tf.equal(tf.argmax(p_y, 1), tf.argmax(Y, 1))
    # Calculate average accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    tf.summary.scalar("accuracy", accuracy)

# Create session
with tf.Session() as sess:
    # Create log writer
    writer = tf.summary.FileWriter(log_path, sess.graph)
    merged_summary = tf.summary.merge_all()

    # Initialize variables
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    sess.run(init_op)
    # Create training coordinator
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(1000):

        # Get next batch of images and labels
        image_batch, label_batch = sess.run([images, labels])

        # Run training
        sess.run(train, feed_dict={X: image_batch, Y: label_batch})

        summary, acc = sess.run([merged_summary, accuracy], feed_dict={X: image_batch, Y: label_batch})

        # Write summray
        writer.add_summary(summary, i)

        if i % 10 == 0:
            print('step {:d} train accuracy: {:f}'.format(i, acc))

    coord.request_stop()
    coord.join(threads)
