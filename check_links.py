import requests

# Konfigurasi file input dan file hasil akhir
INPUT_FILE = "BASED"
OUTPUT_FILE = "hasil"

# Header penyamaran agar permintaan dapat diproses oleh server
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.dens.tv/"
}

def is_link_active(url):
    try:
        # Menggunakan stream=True agar pengecekan koneksi awal lebih cepat
        response = requests.get(url, headers=HEADERS, timeout=3, stream=True)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    return False

def clean_and_check():
    print(f"Membaca file {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {INPUT_FILE} tidak ditemukan di folder ini.")
        return

    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U\n"
    active_blocks = [header]
    
    total = 0
    passed = 0

    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            url = block[-1].strip()
            if url.startswith("http"):
                total += 1
                print(f"[{total}] Mengecek channel...", end=" ")
                
                if is_link_active(url):
                    print("--> AKTIF")
                    active_blocks.extend(block)
                    passed += 1
                else:
                    print("--> MATI (Dibuang)")
        else:
            i += 1

    # Langsung simpan hanya yang aktif ke dalam file tujuan (misal: file 'hasil')
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(active_blocks)

    print("\n" + "="*30)
    print("PROSES SELESAI!")
    print(f"Total channel dicek : {total}")
    print(f"Channel aktif lolos : {passed}")
    print(f"Hasil bersih disimpan di file: '{OUTPUT_FILE}'")

if __name__ == "__main__":
    clean_and_check()
