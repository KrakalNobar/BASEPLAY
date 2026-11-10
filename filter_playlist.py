import urllib.request
import re

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_FILE = "shiegiet"

# Daftar target channel yang diinginkan secara persis (urutan 1 sampai 39)
# Kita buat kamus/pola yang spesifik agar tidak menangkap channel lain yang namanya mirip
TARGET_CHANNELS = [
    "tvone", "rcti", "mnctv", "gtv", "antv", "transtv", "trans7", 
    "indosiar", "sctv", "metro", "kompastv", "cnn", "inews", "rtv", 
    "mdtv", "jowo", "hanacaraka", "cnbc", "sindonews", "moji", "idx", 
    "tvri", "jak tv", "btv", "daai", "indonesiana", "caruban", "banten", 
    "sportstars", "sportstars 2", "sportstars 3", "sportstars 4", 
    "soccer", "spotv", "spotv2", "cartoon", "dunia anak", "space toon", "nickelodeon"
]

def get_exact_matched_index(block_text):
    # Membersihkan teks untuk pengecekan
    block_lower = block_text.lower()
    
    # Ekstrak judul channel atau tvg-name/tvg-id untuk dicocokkan dengan ketat
    for index, target in enumerate(TARGET_CHANNELS):
        # Gunakan regex boundary \b agar pencocokan kata benar-benar pas 
        # (contoh: 'mnc' tidak akan nyasar ke 'mongolian' atau 'mnc tv' ditangkap dengan tepat)
        
        # Penanganan khusus untuk nama pendek agar tidak keliru
        if target == "mnc":
            if 'mnc tv' in block_lower or 'mnctv' in block_lower or 'tvg-id="mnc' in block_lower:
                if 'sindonews' not in block_lower: # Hindari sindonews terseret
                    return index
        elif target == "gtv":
            if 'gtv' in block_lower and 'gaming' not in block_lower:
                return index
        elif target == "cnn":
            if 'cnn indonesia' in block_lower or 'cnn j' in block_lower or block_lower.strip().endswith(',cnn') or 'cnn' in block_lower:
                # Pastikan bukan cnn international yang tidak diinginkan jika ada, atau sesuaikan
                if 'international' not in block_lower:
                    return index
        else:
            # Pencocokan standar dengan batas kata yang jelas
            pattern = r'\b' + re.escape(target) + r'\b'
            if re.search(pattern, block_lower):
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
    
    # Simpan berdasarkan urutan index target agar susunannya dijamin rapi sesuai daftar
    ordered_buckets = {i: [] for i in range(len(TARGET_CHANNELS))}
    
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            # Gabungkan baris EXTINF dan URL di bawahnya untuk dianalisis
            block_text = " ".join(block)
            matched_index = get_exact_matched_index(block_text)
            
            if matched_index != 999:
                # Masukkan ke dalam bucket urutan yang tepat (hanya ambil 1 atau yang paling akurat jika mau, atau masukkan semua yang cocok di posisi itu)
                # Untuk menghindari duplikat ganda, kita bisa batasi atau masukkan
                if not ordered_buckets[matched_index]: # Ambil kemunculan pertama yang valid untuk tiap channel
                    ordered_buckets[matched_index].append(block)
        else:
            i += 1

    # Susun kembali sesuai urutan prioritas 0 sampai 38
    new_lines = [header]
    for idx in range(len(TARGET_CHANNELS)):
        if ordered_buckets[idx]:
            # Ambil item pertama yang cocok untuk channel tersebut
            new_lines.extend(ordered_buckets[idx][0])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Berhasil memperbarui {OUTPUT_FILE} dengan filter presisi tinggi.")

if __name__ == "__main__":
    filter_m3u()
