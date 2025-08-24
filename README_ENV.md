# Versi .env Auto-Load + Diagnostik

File ini (`bot_video_link_env.py`) otomatis membaca `.env` di folder yang sama dan menampilkan log diagnostik:
- CWD (folder kerja saat ini)
- Apakah `.env` ada di folder itu
- BOT_TOKEN ada/tidak, panjang, dan prefix

## Cara pakai
1) Install:
```
pip install -r requirements.txt
pip install python-dotenv
```
2) Buat file `.env` di folder yang sama:
```
BOT_TOKEN=123456:ABCDEF-your-token
LOG_LEVEL=INFO
```
3) Run:
```
python bot_video_link_env.py
```

Jika tetap error, lihat log yang tampil: pastikan kamu menjalankan perintah dari folder yang sama dengan `.env`, atau pindahkan `.env` ke sana.
