import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_SHIEGIET = "shiegiet"
OUTPUT_ZAFRAN = "zafran"

# 39 Channel Paket Ekonomi (Shiegiet)
ECONOMY_CHANNELS = [
    ("TVONE", ["tvone", "tv one"]),
    ("RCTI", ["rcti"]),
    ("MNCTV", ["mnctv", "mnc tv"]),
    ("GTV", ["gtv", "global tv"]),
    ("ANTV", ["antv"]),
    ("TRANSTV", ["transtv", "trans tv"]),
    ("TRANS7", ["trans7", "trans 7"]),
    ("INDOSIAR", ["indosiar"]),
    ("SCTV", ["sctv"]),
    ("METRO", ["metrotv", "metro tv"]),
    ("KOMPASTV", ["kompastv", "kompas tv"]),
    ("CNN", ["cnn indonesia", "cnn j"]),
    ("INEWS", ["inews"]),
    ("RTV", ["rtv", "rajawalitv"]),
    ("MDTV", ["mdtv"]),
    ("JOWO", ["jowo", "channel jowo"]),
    ("HANACARAKA", ["hanacaraka"]),
    ("CNBC", ["cnbc indonesia", "cnbc"]),
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
    ("SPORTSTARS", ["sportstars 1", "sportstars ("]),
    ("SPORTSTARS 2", ["sportstars 2", "sportstars2"]),
    ("SPORTSTARS 3", ["sportstars 3", "sportstars3"]),
    ("SPORTSTARS 4", ["sportstars 4", "sportstars4"]),
    ("SOCCER", ["soccer"]),
    ("SPOTV", ["spotv 1", "spotv hd", "spotv("]),
    ("SPOTV2", ["spotv 2", "spotv2"]),
    ("CARTOON", ["cartoon network"]),
    ("DUNIA ANAK", ["dunia anak"]),
    ("SPACE TOON", ["spacetoon", "space toon"]),
    ("NICKELODEON", ["nickelodeon"])
]

# Kata kunci tambahan untuk mendeteksi semua channel Sport/Olahraga di Zafran (Premium)
SPORT_KEYWORDS = [
    "sport", "soccer", "bein", "match", "arena", "bola", "futsal", 
    "nba", "nfl", "golf", "tennis", "badminton", "race", "f1", 
    "motogp", "fight", "wwe", "ufc", "espn", "champions"
]

def process_playlists():
    print("Mengambil playlist dari file BASED...")
    try:
        req = urllib.request.urlopen(BASE_URL)
        content = req.read().decode('utf-8')
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        return

    lines = content.splitlines()
    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U"
    
    # Parsing semua blok channel yang ada di file BASED
    all_parsed_channels = []
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            extinf_line = block[0]
            channel_title = extinf_line.split(",")[-1].strip().lower() if "," in extinf_line else extinf_line.lower()
            all_parsed_channels.append((channel_title, block))
        else:
            i += 1

    # 1. Membentuk file SHIEGIET (Paket Ekonomi - Urut 1 s.d 39)
    shiegiet_sorted = []
    seen_indices = set()
    
    for target_idx, (ch_name, keywords) in enumerate(ECONOMY_CHANNELS):
        found_block = None
        for title, block in all_parsed_channels:
            matched = False
            for kw in keywords:
                if kw in title:
                    if ch_name == "GTV" and 'gaming' in title: continue
                    if ch_name == "SPORTSTARS" and any(x in title for x in ["2", "3", "4"]): continue
                    if ch_name == "SPOTV" and "2" in title: continue
                    matched = True
                    break
            if matched:
                found_block = block
                break
        if found_block and target_idx not in seen_indices:
            seen_indices.add(target_idx)
            shiegiet_sorted.append(found_block)

    # Simpan file shiegiet
    shiegiet_lines = [header]
    for b in shiegiet_sorted:
        shiegiet_lines.extend(b)
    with open(OUTPUT_SHIEGIET, "w", encoding="utf-8") as f:
        f.write("\n".join(shiegiet_lines) + "\n")

    # 2. Membentuk file ZAFRAN (Paket Premium = Shiegiet + Semua Channel Sport Lainnya)
    zafran_blocks = list(shiegiet_sorted) # Masukkan semua isi shiegiet dulu
    zafran_added_titles = {t for t, _ in all_parsed_channels if any(any(kw in t for kw in kw_list) for _, kw_list in ECONOMY_CHANNELS)}

    for title, block in all_parsed_channels:
        # Jika judul mengandung kata kunci sport dan belum masuk ke zafran
        if any(sport_kw in title for sport_kw in SPORT_KEYWORDS):
            if title not in zafran_added_titles:
                zafran_added_titles.add(title)
                zafran_blocks.append(block)

    # Simpan file zafran
    zafran_lines = [header]
    for b in zafran_blocks:
        zafran_lines.extend(b)
    with open(OUTPUT_ZAFRAN, "w", encoding="utf-8") as f:
        f.write("\n".join(zafran_lines) + "\n")

    print("Berhasil memperbarui file 'shiegiet' dan 'zafran' secara otomatis!")

if __name__ == "__main__":
    process_playlists()
