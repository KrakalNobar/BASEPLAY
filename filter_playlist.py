import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_SHIEGIET = "shiegiet"
OUTPUT_ZAFRAN = "zafran"

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

SPORT_CHANNELS = [
    ("SPORT", ["sport", "bein", "champions", "soccer", "football", "wwe", "ufc", "nba", "formula", "espn", "bola"])
]

FILM_CHANNELS = [
    ("FILM", ["film", "cinema", "movie", "boxoffice", "hbo", "fox movies", "axn", "celestial", "bioskop", "movies", "cinemax", "paramount", "tlc"])
]

ZAFRAN_CHANNELS = ECONOMY_CHANNELS + SPORT_CHANNELS + FILM_CHANNELS

def process_playlists():
    print("Mengunduh file BASED...")
    req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode("utf-8").splitlines()
    except Exception as e:
        print(f"Gagal mengunduh: {e}")
        return

    print(f"Total baris dalam BASED: {len(lines)}")
    
    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U\n"
    
    shiegiet_blocks = [header]
    zafran_blocks = [header]

    count_shiegiet = 0
    count_zafran = 0
    sample_printed = 0

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
            
            # Debug cetak 5 channel pertama untuk melihat format teksnya di log
            if sample_printed < 5:
                print(f"[DEBUG SAMPLE] {block_text.strip()}")
                sample_printed += 1
            
            if any(any(kw in block_text for kw in kws) for _, kws in ECONOMY_CHANNELS):
                shiegiet_blocks.extend(block)
                count_shiegiet += 1
                
            if any(any(kw in block_text for kw in kws) for _, kws in ZAFRAN_CHANNELS):
                zafran_blocks.extend(block)
                count_zafran += 1
        else:
            i += 1

    with open(OUTPUT_SHIEGIET, "w", encoding="utf-8") as f:
        f.writelines(shiegiet_blocks)
        
    with open(OUTPUT_ZAFRAN, "w", encoding="utf-8") as f:
        f.writelines(zafran_blocks)

    print(f"Selesai! Shiegiet: {count_shiegiet}, Zafran: {count_zafran}")

if __name__ == "__main__":
    process_playlists()
