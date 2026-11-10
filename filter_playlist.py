import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar nama kanal yang dicocokkan secara spesifik (menggunakan tvg-id atau nama pasti di baris EXTINF)
# Kita pastikan mencocokkan id atau nama yang spesifik untuk TVOne dan GTV/Global
EXACT_MATCHES = ["tvone", "gtv.id", "gtv"]

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
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            block_text = " ".join(block).lower()
            
            # Filter ketat: Cek apakah baris EXTINF mengandung kata kunci secara spesifik
            # Contoh untuk tvone: pastikan ada 'tvone'
            # Contoh untuk global/gtv: pastikan ada 'gtv' tapi bukan bagian dari kata lain yang tidak relevan
            is_valid = False
            for match in EXACT_MATCHES:
                if match == "tvone" and 'tvone' in block_text:
                    is_valid = True
                elif match in ["gtv", "gtv.id"] and ('gtv' in block_text or 'global' in block_text):
                    # Pastikan tidak meloloskan 'gaming tv' atau yang mengandung kata 'tv' sembarangan
                    if 'gaming' not in block_text:
                        is_valid = True

            if is_valid:
                new_lines.extend(block)
        else:
            i += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memperbarui {OUTPUT_FILE} dengan filter ketat.")

if __name__ == "__main__":
    filter_m3u()
