import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar target channel dengan nama resmi yang biasa muncul di judul
# Format: (Nomor Urut, Nama Channel Utama, [Daftar kata kunci judul yang valid])
EXACT_CHANNELS = [
    ("1. TVONE", ["tvone", "tv one"]),
    ("2. RCTI", ["rcti"]),
    ("3. MNCTV", ["mnctv", "mnc tv"]),
    ("4. GTV", ["gtv", "global tv"]),
    ("5. ANTV", ["antv"]),
    ("6. TRANSTV", ["transtv", "trans tv"]),
    ("7. TRANS7", ["trans7", "trans 7"]),
    ("8. INDOSIAR", ["indosiar"]),
    ("9. SCTV", ["sctv"]),
    ("10. METRO", ["metrotv", "metro tv"]),
    ("11. KOMPASTV", ["kompastv", "kompas tv"]),
    ("12. CNN", ["cnn indonesia", "cnn j"]),
    ("13. INEWS", ["inews", "i-news"]),
    ("14. RTV", ["rtv"]),
    ("15. MDTV", ["mdtv"]),
    ("16. JOWO", ["jowo"]),
    ("17. HANACARAKA", ["hanacaraka"]),
    ("18. CNBC", ["cnbc indonesia", "cnbc"]),
    ("19. SINDONEWS", ["sindonews"]),
    ("20. MOJI", ["moji"]),
    ("21. IDX", ["idx channel", "idx"]),
    ("22. TVRI", ["tvri nasional", "tvri"]),
    ("23. JAK TV", ["jaktv", "jak tv"]),
    ("24. BTV", ["btv"]),
    ("25. DAAI", ["daai tv", "daai"]),
    ("26. INDONESIANA", ["indonesiana"]),
    ("27. CARUBAN", ["caruban"]),
    ("28. BANTEN", ["banten tv", "banten"]),
    ("29. SPORTSTARS", ["sportstars 1", "sportstars"]),
    ("30. SPORTSTARS 2", ["sportstars 2", "sportstars2"]),
    ("31. SPORTSTARS 3", ["sportstars 3", "sportstars3"]),
    ("32. SPORTSTARS 4", ["sportstars 4", "sportstars4"]),
    ("33. SOCCER", ["soccer channel", "soccer"]),
    ("34. SPOTV", ["spotv hd", "spotv"]),
    ("35. SPOTV2", ["spotv 2", "spotv2"]),
    ("36. CARTOON", ["cartoon network", "cartoon"]),
    ("37. DUNIA ANAK", ["dunia anak"]),
    ("38. SPACE TOON", ["spacetoon", "space toon"]),
    ("39. NICKELODEON", ["nickelodeon"])
]

def find_exact_match(block_text):
    block_lower = block_text.lower()
    
    # Cek satu per satu berdasarkan urutan prioritas 1 sampai 39
    for index, (ch_name, keywords) in enumerate(EXACT_CHANNELS):
        for kw in keywords:
            # Pastikan pencocokan ada di baris judul/EXTINF atau atribut nama
            if kw in block_lower:
                # Filter pengecualian khusus untuk menghindari channel nyasar
                if ch_name == "4. GTV" and 'gaming' in block_lower:
                    continue
                if ch_name == "12. CNN" and 'international' in block_lower:
                    continue
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
    
    # Menyimpan channel yang ditemukan sesuai slot urutannya
    ordered_buckets = {i: [] for i in range(len(EXACT_CHANNELS))}
    
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
            matched_index = find_exact_match(block_text)
            
            if matched_index != 999:
                # Ambil yang pertama kali cocok untuk slot tersebut
                if not ordered_buckets[matched_index]:
                    ordered_buckets[matched_index].append(block)
        else:
            i += 1

    # Susun ulang secara berurutan dari 1 sampai 39
    new_lines = [header]
    for idx in range(len(EXACT_CHANNELS)):
        if ordered_buckets[idx]:
            new_lines.extend(ordered_buckets[idx][0])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memperbarui {OUTPUT_FILE} dengan filter ketat.")

if __name__ == "__main__":
    filter_m3u()
