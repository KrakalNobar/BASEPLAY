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

    # Pisahkan entry berdasarkan tag #EXTINF
    entries = content.split("#EXTINF:")
    header = entries[0].strip() if entries else "#EXTM3U"
    
    shiegiet_channels = [header]
    zafran_channels = [header]

    # Keyword Ekonomi untuk Shiegiet (Sama persis seperti semula)
    economy_keywords = [
        "tvone", "rcti", "mnctv", "gtv", "antv", "transtv", "trans7",
        "indosiar", "sctv", "metrotv", "kompastv", "cnn", "inews",
        "rtv", "mdtv", "jowo", "hanacaraka", "cnbc", "sindonews"
    ]

    # Keyword tambahan untuk Zafran (Sport & Film)
    sport_keywords = ["sport", "bein", "champions", "soccer", "football", "wwe", "ufc", "nba", "formula", "espn", "bola"]
    film_keywords = ["film", "cinema", "movie", "boxoffice", "hbo", "fox", "axn", "celestial", "bioskop", "movies", "cinemax", "paramount", "tlc", "zee"]

    for entry in entries[1:]:
        block = "#EXTINF:" + entry
        block_lower = block.lower()

        # Cek kategori
        is_economy = any(k in block_lower for k in economy_keywords)
        is_sport = any(k in block_lower for k in sport_keywords)
        is_film = any(k in block_lower for k in film_keywords)

        # Shiegiet MURNI hanya ekonomi
        if is_economy:
            shiegiet_channels.append(block.strip())

        # Zafran adalah Ekonomi + Sport + Film
        if is_economy or is_sport or is_film:
            zafran_channels.append(block.strip())

    # Simpan hasil ke file
    with open(OUTPUT_SHIEGIET, "w", encoding="utf-8") as f:
        f.write("\n".join(shiegiet_channels) + "\n")
        
    with open(OUTPUT_ZAFRAN, "w", encoding="utf-8") as f:
        f.write("\n".join(zafran_channels) + "\n")

    print(f"Selesai! Shiegiet: {len(shiegiet_channels)-1} channel, Zafran: {len(zafran_channels)-1} channel.")

if __name__ == "__main__":
    process_playlists()
