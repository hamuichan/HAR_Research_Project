import tensorflow as tf
from tensorflow.keras.layers import (
    Dense, Conv1D, BatchNormalization, Activation, 
    GlobalAveragePooling1D, GlobalMaxPooling1D, 
    Add, Multiply, Reshape, Dropout, LayerNormalization, MultiHeadAttention
)
from tensorflow.keras import backend as K
import keras

# --- 1. Loss Function ---
@keras.saving.register_keras_serializable()
def focal_loss_fixed(y_true, y_pred, gamma=2.0, alpha=0.25):
    y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
    cross_entropy = -y_true * K.log(y_pred)
    weight = alpha * y_true * K.pow((1 - y_pred), gamma)
    return K.sum(weight * cross_entropy, axis=-1)

def categorical_focal_loss(gamma=2.0, alpha=0.25):
    def focal_loss(y_true, y_pred):
        return focal_loss_fixed(y_true, y_pred, gamma=gamma, alpha=alpha)
    return focal_loss

# --- 2. Helper Functions for CBAM  ---
# Lambda 안에서 쓰던 로직을 별도 함수로 분리하고 등록

@keras.saving.register_keras_serializable()
def spatial_shape(input_shape):
    return (input_shape[0], input_shape[1], 1)

@keras.saving.register_keras_serializable()
def cbam_reduce_mean(x):
    # 함수 안에서 tf를 명시적으로 사용
    import tensorflow as tf 
    return tf.reduce_mean(x, axis=-1, keepdims=True)

@keras.saving.register_keras_serializable()
def cbam_reduce_max(x):
    import tensorflow as tf
    return tf.reduce_max(x, axis=-1, keepdims=True)

# --- 3. Attention Blocks ---
def squeeze_excite_block(inputs, ratio=16):
    filters = inputs.shape[-1]
    se = GlobalAveragePooling1D()(inputs)
    se = Dense(filters // ratio, activation='relu', use_bias=False)(se)
    se = Dense(filters, activation='sigmoid', use_bias=False)(se)
    se = Reshape((1, filters))(se)
    return Multiply()([inputs, se])

def cbam_block(inputs, ratio=16):
    # Channel Attention
    filters = inputs.shape[-1]
    
    avg_pool = GlobalAveragePooling1D()(inputs)
    max_pool = GlobalMaxPooling1D()(inputs)
    
    mlp = tf.keras.Sequential([
        Dense(filters // ratio, activation='relu', use_bias=False),
        Dense(filters, use_bias=False)
    ])
    
    channel_out = Add()([mlp(avg_pool), mlp(max_pool)])
    channel_out = Activation('sigmoid')(channel_out)
    channel_out = Reshape((1, filters))(channel_out)
    x = Multiply()([inputs, channel_out])
    
    # Spatial (Time) Attention
    avg_pool = tf.keras.layers.Lambda(
        cbam_reduce_mean, 
        output_shape=spatial_shape
    )(x)
    
    max_pool = tf.keras.layers.Lambda(
        cbam_reduce_max, 
        output_shape=spatial_shape
    )(x)
    
    spatial = tf.keras.layers.concatenate([avg_pool, max_pool], axis=-1)
    spatial = Conv1D(1, 7, padding='same', activation='sigmoid')(spatial)
    
    return Multiply()([x, spatial])

@keras.saving.register_keras_serializable()
class PositionalEmbedding(tf.keras.layers.Layer):
    def __init__(self, sequence_length, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.position_embeddings = tf.keras.layers.Embedding(
            input_dim=sequence_length, output_dim=output_dim
        )
        self.sequence_length = sequence_length
        self.output_dim = output_dim

    def call(self, inputs):
        # inputs shape: (Batch, Time, Features)
        length = tf.shape(inputs)[1]
        positions = tf.range(start=0, limit=length, delta=1)
        embedded_positions = self.position_embeddings(positions)
        return inputs + embedded_positions

    def get_config(self):
        config = super().get_config()
        config.update({
            "sequence_length": self.sequence_length,
            "output_dim": self.output_dim,
        })
        return config
    
# --- 4. Transformer Encoder ---
def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0.1):
    # 입력: (Batch, Time, Feat)
    x = PositionalEmbedding(sequence_length=inputs.shape[1], output_dim=inputs.shape[-1])(inputs)
    
    # 2. Attention
    x = LayerNormalization(epsilon=1e-6)(x)
    x = MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(x, x)
    res = Add()([x, inputs])
    
    # 3. Feed Forward
    x = LayerNormalization(epsilon=1e-6)(res)
    x = Conv1D(filters=ff_dim, kernel_size=1, activation="swish")(x)
    x = Dropout(dropout)(x)
    x = Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    return Add()([x, res])