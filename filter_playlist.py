import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar urutan prioritas channel yang Anda inginkan (dalam huruf kecil)
CHANNEL_PRIORITY = [
    "tvone", "rcti", "mnctv", "gtv", "antv", "transtv", "trans7", 
    "indosiar", "sctv", "metro", "kompastv", "cnn", "inews", "rtv", 
    "mdtv", "jowo", "hanacaraka", "cnbc", "sindonews", "moji", "idx", 
    "tvri", "jak tv", "btv", "daai", "indonesiana", "caruban", "banten", 
    "sportstars", "sportstars 2", "sportstars 3", "sportstars 4", 
    "soccer", "spotv", "spotv2", "cartoon", "dunia anak", "space toon", "nickelodeon"
]

def get_channel_priority(block_text):
    # Menentukan posisi urutan channel berdasarkan daftar di atas
    for index, name in enumerate(CHANNEL_PRIORITY):
        # Cek kecocokan nama channel di dalam blok teks m3u
        if name in block_text:
            return index
    return 999  # Jika tidak ada dalam daftar, ditaruh di paling belakang

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
    
    valid_channels = []
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
            
            # Cek apakah blok ini termasuk dalam daftar prioritas kita
            priority = get_channel_priority(block_text)
            if priority != 999:
                valid_channels.append((priority, block))
        else:
            i += 1

    # Urutkan channel sesuai dengan urutan angka 1 sampai 39 di CHANNEL_PRIORITY
    valid_channels.sort(key=lambda x: x[0])

    # Susun kembali isi file playlist
    new_lines = [header]
    for _, block in valid_channels:
        new_lines.extend(block)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memperbarui {OUTPUT_FILE} sesuai urutan prioritas.")

if __name__ == "__main__":
    filter_m3u()
