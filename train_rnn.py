import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Veriyi yükle
with open("melodiler.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Tüm notaları bir listeye aktar
all_notes = []
for sample in data:
    all_notes.extend(sample["notes"])

# Tekrar edenleri kaldır, sıralı nota ID listesi yap
unique_notes = sorted(list(set(all_notes)))
note_to_int = {note: i for i, note in enumerate(unique_notes)}
int_to_note = {i: note for note, i in note_to_int.items()}

# Giriş-çıkış dizilerini oluştur
sequence_length = 20
inputs = []
targets = []

for sample in data:
    notes = sample["notes"]
    if len(notes) < sequence_length + 1:
        continue
    for i in range(len(notes) - sequence_length):
        seq_in = notes[i:i + sequence_length]
        seq_out = notes[i + sequence_length]
        inputs.append([note_to_int[n] for n in seq_in])
        targets.append(note_to_int[seq_out])

# Numpy dizilerine çevir
X = np.array(inputs)
y = to_categorical(targets, num_classes=len(unique_notes))

# Eğitim ve test verisi ayır
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1)

# Modeli oluştur
model = Sequential([
    LSTM(128, input_shape=(sequence_length, 1)),
    Dense(len(unique_notes), activation="softmax")
])

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Girişleri 3D'ye reshape et
X_train = X_train.reshape(X_train.shape[0], sequence_length, 1)
X_val = X_val.reshape(X_val.shape[0], sequence_length, 1)

# Eğit
model.fit(X_train, y_train, epochs=15, batch_size=64, validation_data=(X_val, y_val))

# Kaydet
model.save("melodi_rnn_model.h5")
print("✅ Model başarıyla kaydedildi.")

import os
print("📁 Kayıt yeri:", os.getcwd())
