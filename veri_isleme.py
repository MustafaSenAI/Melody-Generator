import os
import glob
import pandas as pd
import pretty_midi
import json

# MIDI kök klasörü
midi_root = "maestro-v3.0.0"
csv_path = os.path.join(midi_root, "maestro-v3.0.0.csv")

# CSV oku
df = pd.read_csv(csv_path)
df["midi_filename_clean"] = df["midi_filename"].apply(os.path.basename)

# MIDI dosyalarını topla
midi_paths = glob.glob(os.path.join(midi_root, "**/*.midi"), recursive=True)
midi_paths = midi_paths[:50]  # İlk 50 dosya

# Dosya adlarını al
selected_names = [os.path.basename(p) for p in midi_paths]
df = df[df["midi_filename_clean"].isin(selected_names)]

# Besteciye göre duygu atama
def get_emotion(composer):
    if "Chopin" in composer or "Rachmaninoff" in composer:
        return "hüzünlü"
    elif "Mozart" in composer or "Beethoven" in composer:
        return "neşeli"
    else:
        return "nötr"

df["emotion"] = df["canonical_composer"].apply(get_emotion)

melodies = []

# Notaları çıkar
for path in midi_paths:
    try:
        midi = pretty_midi.PrettyMIDI(path)
        notes = []
        for instrument in midi.instruments:
            if instrument.is_drum:
                continue
            for note in instrument.notes:
                notes.append(note.pitch)

        if notes:
            file_name = os.path.basename(path)
            emotion = df.loc[df["midi_filename_clean"] == file_name, "emotion"].values[0]
            melodies.append({
                "filename": file_name,
                "emotion": emotion,
                "notes": notes
            })

    except Exception as e:
        print(f"Hata: {path} - {e}")

# JSON olarak kaydet
with open("melodiler.json", "w", encoding="utf-8") as f:
    json.dump(melodies, f, indent=2, ensure_ascii=False)

print(f"✅ melodiler.json başarıyla kaydedildi.")
print(f"🎵 Toplam melodi sayısı: {len(melodies)}")
