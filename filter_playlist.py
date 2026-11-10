import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar target channel dan kata kunci pencarian alternatifnya (tanpa spasi/fleksibel)
# Format: ("Nama Urutan", [daftar kata kunci yang mungkin muncul di file BASED])
CHANNEL_RULES = [
    ("TVONE", ["tvone", "tv one"]),
    ("RCTI", ["rcti"]),
    ("MNCTV", ["mnctv", "mnc tv"]),
    ("GTV", ["gtv"]),
    ("ANTV", ["antv"]),
    ("TRANSTV", ["transtv", "trans tv"]),
    ("TRANS7", ["trans7", "trans 7"]),
    ("INDOSIAR", ["indosiar"]),
    ("SCTV", ["sctv"]),
    ("METRO", ["metrotv", "metro tv", "metro"]),
    ("KOMPASTV", ["kompastv", "kompas tv"]),
    ("CNN", ["cnn indonesia", "cnn j", "cnn"]),
    ("INEWS", ["inews", "i-news"]),
    ("RTV", ["rtv"]),
    ("MDTV", ["mdtv"]),
    ("JOWO", ["jowo"]),
    ("HANACARAKA", ["hanacaraka"]),
    ("CNBC", ["cnbc"]),
    ("SINDONEWS", ["sindonews"]),
    ("MOJI", ["moji"]),
    ("IDX", ["idx"]),
    ("TVRI", ["tvri"]),
    ("JAK TV", ["jaktv", "jak tv"]),
    ("BTV", ["btv"]),
    ("DAAI", ["daai"]),
    ("INDONESIANA", ["indonesiana"]),
    ("CARUBAN", ["caruban"]),
    ("BANTEN", ["banten"]),
    ("SPORTSTARS", ["sportstars"]),
    ("SPORTSTARS 2", ["sportstars 2", "sportstars2"]),
    ("SPORTSTARS 3", ["sportstars 3", "sportstars3"]),
    ("SPORTSTARS 4", ["sportstars 4", "sportstars4"]),
    ("SOCCER", ["soccer"]),
    ("SPOTV", ["spotv"]),
    ("SPOTV2", ["spotv2", "spotv 2"]),
    ("CARTOON", ["cartoon"]),
    ("DUNIA ANAK", ["dunia anak"]),
    ("SPACE TOON", ["spacestoon", "space toon", "spacetoon"]),
    ("NICKELODEON", ["nickelodeon"])
]

def find_channel_index(block_text):
    block_lower = block_text.lower()
    
    # Cek setiap aturan channel sesuai urutan prioritas
    for index, (channel_name, keywords) in enumerate(CHANNEL_RULES):
        for kw in keywords:
            # Khusus GTV, pastikan bukan gaming tv
            if channel_name == "GTV" and ('gtv' in block_lower and 'gaming' not in block_lower):
                return index
            # Khusus METRO, pastikan bukan metro channel yang tidak diinginkan jika mau spesifik, tapi biarkan fleksibel dulu
            elif channel_name != "GTV" and kw in block_lower:
                return index
                
    return 999

def filter_m3u():
    print("Mengambil playlist dari file BASED...")
    try:
        req = urllib.request.urlopen(BASE_URL)
        content = req.read().decode('utf-8')
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return

    lines = content.splitlines()
    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U"
    
    ordered_buckets = {i: [] for i in range(len(CHANNEL_RULES))}
    
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            block_text = " ".join(block)
            matched_index = find_channel_index(block_text)
            
            if matched_index != 999:
                # Simpan item pertama yang cocok untuk masing-masing slot urutan
                if not ordered_buckets[matched_index]:
                    ordered_buckets[matched_index].append(block)
        else:
            i += 1

    # Susun kembali sesuai urutan 1 sampai 39 secara presisi
    new_lines = [header]
    for idx in range(len(CHANNEL_RULES)):
        if ordered_buckets[idx]:
            new_lines.extend(ordered_buckets[idx][0])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memperbarui {OUTPUT_FILE} dengan urutan & keyword fleksibel.")

if __name__ == "__main__":
    filter_m3u()
