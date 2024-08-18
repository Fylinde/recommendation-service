import tensorflow as tf
import tensorflow_recommenders as tfrs

class TFRecommender(tfrs.Model):  # Inherit directly from tfrs.Model
    def __init__(self, user_ids, item_ids):
        super().__init__()
        
        # Convert user_ids and item_ids to strings
        user_ids = [str(user_id) for user_id in user_ids]
        item_ids = [str(item_id) for item_id in item_ids]

        # Define the embedding dimensions
        embedding_dimension = 32

        # Define the user model
        self.user_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=user_ids, mask_token=None),
            tf.keras.layers.Embedding(len(user_ids) + 1, embedding_dimension)
        ])

        # Define the item model
        self.item_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=item_ids, mask_token=None),
            tf.keras.layers.Embedding(len(item_ids) + 1, embedding_dimension)
        ])

        # Define the retrieval task
        self.task = tfrs.tasks.Retrieval()

    def compute_loss(self, features, training=False):
        # We pick out the user features and pass them into the user model.
        user_embeddings = self.user_model(features["user_id"])
        # And pick out the item features and pass them into the item model,
        item_embeddings = self.item_model(features["item_id"])

        # The task computes the loss and metrics.
        return self.task(user_embeddings, item_embeddings)

    def train(self, interactions, epochs=5):
        # Convert interactions to strings and prepare tensors
        user_ids = [str(interaction[0]) for interaction in interactions]
        item_ids = [str(interaction[1]) for interaction in interactions]

        # Create the dataset with a tuple of tensors
        train = tf.data.Dataset.from_tensor_slices({
            "user_id": tf.constant(user_ids),
            "item_id": tf.constant(item_ids),
        }).batch(1)
        
        # Compile and train the model
        self.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))
        self.fit(train, epochs=epochs)

    def recommend(self, user_id, top_k=5):
        # Ensure user_id is a string
        user_id = str(user_id)

        # Get recommendations for a user
        user_embedding = self.user_model(tf.constant([user_id]))

        # Retrieve the top recommended items for the user
        scores = self.item_model.weights[0].numpy()
        top_scores_indices = (-scores @ user_embedding.numpy().T).flatten().argsort()[:top_k]

        return [self.item_model.layers[0].get_vocabulary()[i] for i in top_scores_indices]
