# Script de Treinamento Principal

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
# Importa a função de pré-processamento específica do InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau # Importa o ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os

# --- VERIFICAÇÃO DA GPU ---
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU encontrada e configurada: {gpus[0].name}")
else:
    print("⚠️ AVISO: Nenhuma GPU foi encontrada. O treinamento será em CPU.")

# --- 1. Configuração dos Caminhos ---
pasta_raiz_origem = '/data'
caminho_modelo_salvo = '/modelo_garbage_inception_v1.keras'

# --- 2. Data Augmentation com PRÉ-PROCESSAMENTO ---
datagen = ImageDataGenerator(
    # Usamos a função específica do InceptionV3
    preprocessing_function=preprocess_input,

    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Lógica para lidar com uma possível pasta aninhada (ex: /Resistores_HR/Resistores/)
caminho_real_dataset = pasta_raiz_origem
subpastas_iniciais = os.listdir(pasta_raiz_origem)
if len(subpastas_iniciais) == 1 and os.path.isdir(os.path.join(pasta_raiz_origem, subpastas_iniciais[0])):
    caminho_real_dataset = os.path.join(pasta_raiz_origem, subpastas_iniciais[0])

# Geradores de dados
train_generator = datagen.flow_from_directory(
    caminho_real_dataset,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    caminho_real_dataset,
    target_size=(299, 299),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

num_classes = train_generator.num_classes
print(f"Encontradas {train_generator.samples} imagens de treino e {validation_generator.samples} imagens de validação em {num_classes} classes.")

# --- 3. Class Weights (ajuste para classes desbalanceadas) ---
labels = train_generator.classes
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(labels), y=labels)
class_weights = dict(enumerate(class_weights))
print("Pesos de classe calculados para lidar com desbalanceamento.")

# --- 4. Modelo com InceptionV3 (Transfer Learning) ---
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(299, 299, 3))
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# --- 5. Callbacks para um Treinamento mais Inteligente ---
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-6, verbose=1)
callbacks_list = [early_stop, reduce_lr]

# --- 6. Treinamento Inicial ---
print("\n--- Iniciando Treinamento Principal (camadas de topo) ---")
history = model.fit(
    train_generator,
    epochs=20, # O EarlyStopping provavelmente vai parar antes
    validation_data=validation_generator,
    callbacks=callbacks_list,
    class_weight=class_weights
)

# --- 7. Fine-tuning ---
print("\n--- Iniciando Fine-Tuning (descongelando parte da base) ---")
base_model.trainable = True
fine_tune_at = 249
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), # Taxa de aprendizado bem baixa
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# O fine-tuning também se beneficia dos callbacks
history_finetune = model.fit(
    train_generator,
    epochs=10, # O EarlyStopping provavelmente vai parar antes
    validation_data=validation_generator,
    callbacks=callbacks_list,
    class_weight=class_weights
)

# --- 8. Avaliação e Salvamento Final ---
print("\n--- Avaliando o modelo final no conjunto de dados de VALIDAÇÃO ---")
test_loss, test_accuracy = model.evaluate(validation_generator)
print(f"Loss de Validação Final: {test_loss:.4f}")
print(f"Acurácia de Validação Final: {test_accuracy:.4f}")

model.save(caminho_modelo_salvo)
print(f"\n✅ Modelo treinado e salvo em: {caminho_modelo_salvo}")