# Spotify-Controller-with-hand-gesture
Oke, gue buatin **README.md full versi final** yang udah rapi, lengkap, dan tinggal lo taruh di root repo GitHub lo.

````markdown
# 🎵 Spotify Controller with Hand Gesture

Kontrol Spotify cukup pakai **gerakan tangan**.  
Nggak perlu klik mouse atau tekan tombol keyboard lagi — tinggal angkat tangan, musik nurut.

---

## ✨ Fitur Utama
- 🎚 **Play / Pause** lagu
- ⏭ **Next / Previous track**
- 🔊 **Volume up / down**
- 📷 Deteksi gesture real-time via kamera
- 🚀 Cepat, responsif, dan gampang dijalankan

---

## 🛠 Teknologi
- **Python**
- **OpenCV** – untuk capture video & deteksi gerakan
- **MediaPipe** – untuk tracking posisi tangan & jari
- **Spotipy** – integrasi dengan Spotify API

---

## ⚙ Instalasi & Setup

1. **Clone repo**
   ```bash
   git clone https://github.com/arizzira/Spotify-Controller-with-hand-gesture.git
   cd Spotify-Controller-with-hand-gesture
````

2. **Buat virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   .\venv\Scripts\activate    # Windows
   pip install -r requirements.txt
   ```

3. **Daftar & ambil API key dari Spotify**

   * Masuk ke [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   * Buat aplikasi baru
   * Simpan **Client ID** & **Client Secret**
   * Set `redirect_uri` → contoh: `http://localhost:8888/callback`

4. **Buat file `.env`**

   ```
   CLIENT_ID=your_spotify_client_id
   CLIENT_SECRET=your_spotify_client_secret
   REDIRECT_URI=http://localhost:8888/callback
   ```

5. **Jalankan program**

   ```bash
   python gesture_spotify.py
   ```

---

## ✋ Gestur Default

| Gesture                    | Fungsi         |
| -------------------------- | -------------- |
| ✊ Kepal                    | Play / Pause   |
| 👉 Jari telunjuk           | Next Track     |
| ✌ Dua jari                 | Previous Track |
| 🖐 Telapak terbuka         | Volume Up      |
| 🤚 Telapak menghadap bawah | Volume Down    |

*(Gesture bisa diubah di `gesture_spotify.py` sesuai selera lo)*

---

## 📷 Demo

*(Tambahkan GIF atau screenshot di sini)*
Contoh:

```markdown
![Demo](assets/demo.gif)
```

---

## 📌 Catatan

* Gunakan pencahayaan yang cukup agar kamera mendeteksi gesture dengan akurat.
* Dibutuhkan **Spotify Premium** untuk kontrol playback via API.
* Pastikan kamera tidak terhalang.

---

## 📜 Lisensi

[MIT License](LICENSE)

---

## 📬 Kontak

Made with ❤️ by **arizzira**
GitHub: [@arizzira](https://github.com/arizzira)

```

Kalau lo mau, gue bisa sekalian bikinin **GIF demo** pake template looping kamera + Spotify supaya README ini langsung *eye-catching* pas orang buka repo lo.  
Mau gue buatkan juga?
```
