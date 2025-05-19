# 🎵 AI Melodi Üretici (LSTM RNN Tabanlı Müzik Üretimi)

Bu proje, LSTM (Long Short-Term Memory) mimarisi kullanan bir RNN (Recurrent Neural Network) ile müzik üretmeyi amaçlayan bir yapay zeka projesidir. Yapay sinir ağı, MIDI formatındaki melodileri analiz ederek yeni müzikal örüntüler oluşturmayı öğrenir.

---

## 📁 Kullanılan Veri Seti

Projede kullanılan veri seti: **[Maestro v3.0.0](https://magenta.tensorflow.org/datasets/maestro)**  
Bu set, yüksek kaliteli klasik müzik performanslarını içeren kapsamlı bir MIDI koleksiyonudur.

---

## 🧠 Model Eğitimi

- `train_rnn.py` dosyası ile melodilerden elde edilen notalar modele verilerek LSTM tabanlı bir RNN ağı eğitilmiştir.
- 20 notalık giriş dizileri kullanılarak bir sonraki nota tahmin edilmiştir.
- Eğitim sonucu model `melodi_rnn_model.h5` olarak kaydedilmiştir.

---

## 🎼 Melodi Üretimi

- `generate_melody.py` dosyası ile eğitilen model rastgele bir başlangıç sekansı üzerinden 50 notalık yeni bir melodi üretmektedir.
- Üretilen notalar `create_midi.py` ile `uretilen_melodi.mid` dosyasına dönüştürülür.

---

## 🔊 Ses Formatına Dönüştürme

- `.mid` dosyasını `.wav` formatına çevirmek için [FluidSynth](https://www.fluidsynth.org/) kullanılır.
- Ek olarak, `FluidR3_GM.sf2` gibi bir SoundFont (.sf2) dosyasına ihtiyaç vardır.
- Örnek kullanım:
  ```bash
  fluidsynth -ni FluidR3_GM.sf2 uretilen_melodi.mid -F uretilen_melodi.wav -r 44100
