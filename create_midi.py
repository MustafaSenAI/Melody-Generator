import pretty_midi

# Üretilen notalar
generated_notes = [55, 68, 51, 68, 51, 68, 51, 68, 51, 68, 51, 68, 51, 68, 51, 68, 51, 68, 51, 68]

# PrettyMIDI nesnesi oluştur
midi = pretty_midi.PrettyMIDI()
piano = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program("Acoustic Grand Piano"))

# Zamanlayıcı
start = 0
duration = 0.5  # Her notanın süresi (yarım saniye)

# Notaları sırayla ekle
for note_number in generated_notes:
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=start, end=start + duration)
    piano.notes.append(note)
    start += duration

midi.instruments.append(piano)

# MIDI dosyasını kaydet
midi.write("uretilen_melodi.mid")
print("🎵 Melodi başarıyla 'uretilen_melodi.mid' olarak kaydedildi.")
