import urllib.request

# URL mentah (raw) dari file BASED di repository Anda
BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar keyword kanal yang ingin diambil (TVONE dan GLOBAL/GTV)
ALLOWED_CHANNELS = ["tvone", "gtv"] 

def filter_m3u():
    print("Mengambil playlist dari file BASED...")
    try:
        req = urllib.request.urlopen(BASE_URL)
        content = req.read().decode('utf-8')
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return

    lines = content.splitlines()
    new_lines = []
    
    if lines and lines[0].startswith("#EXTM3U"):
        new_lines.append(lines[0])

    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            # Mengumpulkan baris atribut pendukung dan URL stream di bawahnya
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            # Cek apakah kanal ini mengandung kata kunci tvone atau gtv (GLOBAL)
            block_text = " ".join(block).lower()
            if any(allowed in block_text for allowed in ALLOWED_CHANNELS):
                new_lines.extend(block)
        else:
            i += 1

    # Simpan hasil filter ke dalam file/folder shiegiet
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memfilter dan memperbarui {OUTPUT_FILE}")

if __name__ == "__main__":
    filter_m3u()
