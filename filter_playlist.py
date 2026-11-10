import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar target channel yang Anda inginkan (Urutan 1 sampai 39 secara pasti)
# Kita pasangkan nama channel dengan kata kunci unik yang ada di judulnya
TARGET_CHANNELS = [
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
    ("SPORTSTARS", ["sportstars 1", "sportstars ("]), # Pastikan spesifik agar tidak nyeret sportstars 2/3/4
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
    
    # Menyiapkan wadah penyimpanan berurutan dari indeks 0 sampai 38
    sorted_channels = []
    
    # Parsing file M3U per blok channel
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            # Ambil bagian judul channel saja (biasanya setelah tanda koma terakhir di baris EXTINF)
            extinf_line = block[0]
            if "," in extinf_line:
                channel_title = extinf_line.split(",")[-1].strip().lower()
            else:
                channel_title = extinf_line.lower()
            
            # Cek kecocokan ketat hanya berdasarkan urutan TARGET_CHANNELS
            matched_priority = 999
            for idx, (ch_name, keywords) in enumerate(TARGET_CHANNELS):
                found = False
                for kw in keywords:
                    # Cek apakah keyword ada di judul channel
                    if kw in channel_title:
                        # Aturan pengecualian ketat agar tidak salah tangkap
                        if ch_name == "GTV" and 'gaming' in channel_title:
                            continue
                        if ch_name == "SPORTSTARS" and ("2" in channel_title or "3" in channel_title or "4" in channel_title):
                            continue
                        if ch_name == "SPOTV" and "2" in channel_title:
                            continue
                        found = True
                        break
                if found:
                    matched_priority = idx
                    break
            
            # Jika channel ini terdaftar di target kita, masukkan ke list sementara bersama nomor prioritasnya
            if matched_priority != 999:
                sorted_channels.append((matched_priority, block))
        else:
            i += 1

    # Urutkan list berdasarkan nomor prioritas secara mutlak (dari 0 sampai 38)
    sorted_channels.sort(key=lambda x: x[0])

    # Hilangkan duplikat jika di file BASED ada channel kembar, ambil yang pertama saja per jenis
    final_blocks = []
    seen_indices = set()
    for priority, block in sorted_channels:
        if priority not in seen_indices:
            seen_indices.add(priority)
            final_blocks.append((priority, block))

    # Susun ulang isi file output
    new_lines = [header]
    # Agar benar-benar urut dari 0 sampai 38 meskipun ada yang kosong/tidak ada di BASED
    for target_idx in range(len(TARGET_CHANNELS)):
        for priority, block in final_blocks:
            if priority == target_idx:
                new_lines.extend(block)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print("Filter dan pengurutan selesai.")

if __name__ == "__main__":
    filter_m3u()
