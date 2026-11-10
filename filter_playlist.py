import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_SHIEGIET = "shiegiet"
OUTPUT_ZAFRAN = "zafran"

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
            
            # Kriteria Shiegiet (Khusus Ekonomi/Lokal)
            is_economy = any(k in block_text for k in ["tvone", "rcti", "mnctv", "gtv", "antv", "transtv", "trans7", "indosiar", "sctv", "metrotv", "kompastv", "inews", "rtv"])
            
            # Kriteria Zafran: Mencakup Ekonomi + Sport + Film (Kata kunci diperluas agar mudah tertangkap)
            is_sport = any(k in block_text for k in ["sport", "bein", "champions", "soccer", "football", "ufc", "nba", "espn", "bola", "sport"])
            is_film = any(k in block_text for k in ["film", "cinema", "movie", "boxoffice", "hbo", "fox", "axn", "celestial", "bioskop", "movies", "cinemax", "paramount", "tlc", "zee"])

            if is_economy:
                shiegiet_blocks.extend(block)
                count_shiegiet += 1
                
            # Masukkan ke zafran jika termasuk ekonomi, sport, ATAU film
            if is_economy or is_sport or is_film:
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
