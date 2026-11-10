import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar target id atau nama unik yang persis ingin diambil
EXACT_TARGETS = ['tvg-id="tvone.id@sd"', 'tvg-id="gtv.id@sd"']

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
            
            # Hanya ambil jika baris EXTINF persis memiliki tvg-id target utama
            if any(target in block_text for target in EXACT_TARGETS):
                new_lines.extend(block)
        else:
            i += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memperbarui {OUTPUT_FILE} dengan filter presisi.")

if __name__ == "__main__":
    filter_m3u()
