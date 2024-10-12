import tensorflow as tf
import tensorflow_recommenders as tfrs

class TFRecommender(tfrs.Model):
    def __init__(self, user_ids, item_ids, user_features=None, item_features=None):
        super().__init__()

        # Convert IDs to strings for embedding lookup
        user_ids = [str(user_id) for user_id in user_ids]
        item_ids = [str(item_id) for item_id in item_ids]

        embedding_dimension = 32

        # Define user model
        self.user_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=user_ids, mask_token=None),
            tf.keras.layers.Embedding(len(user_ids) + 1, embedding_dimension)
        ])

        if user_features:
            self.user_model.add(tf.keras.layers.DenseFeatures(user_features))

        # Define item model
        self.item_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=item_ids, mask_token=None),
            tf.keras.layers.Embedding(len(item_ids) + 1, embedding_dimension)
        ])

        if item_features:
            self.item_model.add(tf.keras.layers.DenseFeatures(item_features))

        # Define retrieval and ranking tasks
        self.retrieval_task = tfrs.tasks.Retrieval()
        self.rating_task = tfrs.tasks.Ranking(loss=tf.keras.losses.MeanSquaredError(), metrics=[tf.keras.metrics.RootMeanSquaredError()])

    def compute_loss(self, features, training=False):
        # Pass the user features into the user model
        user_embeddings = self.user_model(features["user_id"])
        # Pass the item features into the item model
        item_embeddings = self.item_model(features["item_id"])

        # Compute retrieval loss
        retrieval_loss = self.retrieval_task(user_embeddings, item_embeddings)

        # Compute ranking loss (if applicable)
        ranking_loss = self.rating_task(user_embeddings, item_embeddings)

        # Return combined loss for training both tasks
        return retrieval_loss + ranking_loss

    def train(self, interactions, user_features=None, item_features=None, epochs=5, batch_size=1024):
        # Convert interactions to strings and prepare tensors
        user_ids = [str(interaction[0]) for interaction in interactions]
        item_ids = [str(interaction[1]) for interaction in interactions]

        dataset_dict = {
            "user_id": tf.constant(user_ids),
            "item_id": tf.constant(item_ids),
        }

        # Add optional user and item features if provided
        if user_features:
            dataset_dict.update(user_features)

        if item_features:
            dataset_dict.update(item_features)

        # Create the dataset, shuffle and batch it
        train = tf.data.Dataset.from_tensor_slices(dataset_dict).shuffle(100_000).batch(batch_size).cache().prefetch(buffer_size=tf.data.AUTOTUNE)

        # Compile and train the model
        self.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))
        self.fit(train, epochs=epochs)

    def recommend(self, user_id, top_k=5):
        # Ensure user_id is a string
        user_id = str(user_id)

        # Get the user embedding
        user_embedding = self.user_model(tf.constant([user_id]))

        # Calculate scores for all items
        item_embeddings = self.item_model.weights[0].numpy()
        scores = item_embeddings @ user_embedding.numpy().T

        # Get the indices of the top K items
        top_scores_indices = (-scores).flatten().argsort()[:top_k]

        # Return the top K recommended item IDs
        return [self.item_model.layers[0].get_vocabulary()[i] for i in top_scores_indices]

    def evaluate_model(self, test_data, batch_size=1024):
        """
        Evaluate the model on a test dataset.
        
        :param test_data: The test interactions (user-item pairs)
        :param batch_size: The batch size for evaluation
        :return: Dictionary of evaluation metrics
        """
        # Convert test data to tensors
        user_ids = [str(interaction[0]) for interaction in test_data]
        item_ids = [str(interaction[1]) for interaction in test_data]

        test = tf.data.Dataset.from_tensor_slices({
            "user_id": tf.constant(user_ids),
            "item_id": tf.constant(item_ids),
        }).batch(batch_size)

        # Evaluate the model on the test dataset using the ranking task metrics
        metrics = self.evaluate(test)
        return metrics

