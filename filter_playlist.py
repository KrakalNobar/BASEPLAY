import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_SHIEGIET = "shiegiet"
OUTPUT_ZAFRAN = "zafran"

# 1. Daftar Channel Paket Ekonomi (Shiegiet)
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
]

# 2. Tambahan Kategori Sport (Olahraga)
SPORT_CHANNELS = [
    ("SPORT", ["sport", "bein", "champions", "soccer", "football", "wwe", "ufc", "nba", "formula", "espn", "bola"])
]

# 3. Tambahan Kategori Film yang Lebih Luas
FILM_CHANNELS = [
    ("FILM", ["film", "cinema", "movie", "boxoffice", "hbo", "fox movies", "axn", "celestial", "bioskop", "movies", "cinemax", "paramount", "tlc"])
]

ZAFRAN_CHANNELS = ECONOMY_CHANNELS + SPORT_CHANNELS + FILM_CHANNELS

def download_playlist():
    req = urllib.request.Request(
        BASE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8").splitlines()

def process_playlists():
    lines = download_playlist()
    if not lines:
        print("File BASED kosong atau gagal diunduh.")
        return

    header = lines[0] if lines[0].startswith("#EXTM3U") else "#EXTM3U\n"
    
    shiegiet_blocks = [header]
    zafran_blocks = [header]

    count_shiegiet = 0
    count_zafran = 0

    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            block_text = "".join(block).lower()
            
            # Cek Shiegiet
            if any(any(kw in block_text for kw in kws) for _, kws in ECONOMY_CHANNELS):
                shiegiet_blocks.extend(block)
                count_shiegiet += 1
                
            # Cek Zafran (Ekonomi + Sport + Film)
            if any(any(kw in block_text for kw in kws) for _, kws in ZAFRAN_CHANNELS):
                zafran_blocks.extend(block)
                count_zafran += 1
        else:
            i += 1

    with open(OUTPUT_SHIEGIET, "w", encoding="utf-8") as f:
        f.writelines(shiegiet_blocks)
        
    with open(OUTPUT_ZAFRAN, "w", encoding="utf-8") as f:
        f.writelines(zafran_blocks)

    print(f"Berhasil! Shiegiet: {count_shiegiet} channel, Zafran: {count_zafran} channel.")

if __name__ == "__main__":
    process_playlists()
