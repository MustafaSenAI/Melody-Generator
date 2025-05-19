import json
import numpy as np
from tensorflow.keras.models import load_model
import random


def apply_temperature(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds + 1e-9) / temperature
    exp_preds = np.exp(preds)
    return exp_preds / np.sum(exp_preds)

def top_k_sampling(probabilities, k=5):
    sorted_indices = np.argsort(probabilities)[-k:]
    top_probs = probabilities[sorted_indices]
    top_probs = top_probs / np.sum(top_probs)  # Normalize
    return np.random.choice(sorted_indices, p=top_probs)

# Eğittiğimiz modeli yükle
model = load_model("melodi_rnn_model.h5")





# Eğitim sırasında kaydedilen dizileri yeniden oluştur
with open("melodiler.json", "r", encoding="utf-8") as f:
    melodiler = json.load(f)

all_notes = [note for sample in melodiler for note in sample["notes"]]
unique_notes = sorted(list(set(all_notes)))
note_to_int = {note: i for i, note in enumerate(unique_notes)}
int_to_note = {i: note for i, note in enumerate(unique_notes)}

# Rastgele bir giriş seç ve üretim yap
sequence_length = 20
seed = [60, 62, 64, 65, 67, 69, 71, 72, 71, 69, 67, 65, 64, 62, 60, 62, 64, 65, 67, 69]
generated = []

for _ in range(50):
    input_seq = np.array([note_to_int[n] for n in seed]).reshape(1, sequence_length, 1)
    prediction = model.predict(input_seq, verbose=0)
    
    # Apply temperature
    temp_scaled = apply_temperature(prediction[0], temperature=0.8)
    
    # Apply top-k sampling
    predicted_index = top_k_sampling(temp_scaled, k=5)

    predicted_note = int_to_note[predicted_index]
    generated.append(predicted_note)
    seed = seed[1:] + [predicted_note]


print("🎶 Üretilen melodi:")
print(generated)
