import urllib.request

BASE_URL = "https://raw.githubusercontent.com/KrakalNobar/BASEPLAY/main/BASED"
OUTPUT_SHIEGIET = "shiegiet"
OUTPUT_ZAFRAN = "zafran"

def process_playlists():
    print("Mengunduh file BASED...")
    req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf-8")
    except Exception as e:
        print(f"Gagal mengunduh: {e}")
        return

    lines = content.splitlines()
    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U"
    
    shiegiet_blocks = [header]
    zafran_blocks = [header]

    # Daftar keyword ekonomi
    economy_keywords = [
        "tvone", "tv one", "rcti", "mnctv", "mnc tv", "gtv", "global tv",
        "antv", "transtv", "trans tv", "trans7", "trans 7", "indosiar", 
        "sctv", "metrotv", "metro tv", "kompastv", "kompas tv", "cnn indonesia", 
        "cnn j", "inews", "rtv", "rajawalitv", "mdtv", "jowo", "channel jowo", 
        "hanacaraka", "cnbc indonesia", "cnbc", "sindonews"
    ]

    # Keyword pemisah untuk Sport & Film
    sport_keywords = ["sport", "bein", "champions", "soccer", "football", "wwe", "ufc", "nba", "formula", "espn", "bola"]
    film_keywords = ["film", "cinema", "movie", "boxoffice", "hbo", "fox", "axn", "celestial", "bioskop", "movies", "cinemax", "paramount", "tlc", "zee"]

    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            block_text = "\n".join(block).lower()
            
            is_economy = any(k in block_text for k in economy_keywords)
            is_sport = any(k in block_text for k in sport_keywords)
            is_film = any(k in block_text for k in film_keywords)

            # SYARAT SHIEGIET: Harus ekonomi, TAPI HARUS BERSIH dari Sport dan Film
            # (Sehingga SCTV Sport / SCTV Movie tidak akan masuk ke Shiegiet)
            if is_economy and not is_sport and not is_film:
                shiegiet_blocks.extend(block)
                
            # SYARAT ZAFRAN: Gabungan Ekonomi + Sport + Film
            if is_economy or is_sport or is_film:
                zafran_blocks.extend(block)
        else:
            i += 1

    with open(OUTPUT_SHIEGIET, "w", encoding="utf-8") as f:
        f.write("\n".join(shiegiet_blocks) + "\n")
        
    with open(OUTPUT_ZAFRAN, "w", encoding="utf-8") as f:
        f.write("\n".join(zafran_blocks) + "\n")

    print("Filter selesai dengan akurat!")

if __name__ == "__main__":
    process_playlists()
