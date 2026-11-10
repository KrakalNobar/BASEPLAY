import requests

INPUT_FILE = "BASED"
OUTPUT_FILE = "hasil"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.dens.tv/"
}

def is_link_active(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=3, stream=True)
        if response.status_code == 200:
            return True
    except Exception:
        pass
    return False

def clean_and_check():
    print(f"Membaca file {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File {INPUT_FILE} tidak ditemukan.")
        return

    header = lines[0] if lines and lines[0].startswith("#EXTM3U") else "#EXTM3U\n"
    active_blocks = [header]
    
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("#EXTINF"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].startswith("#EXTINF") and not lines[i].startswith("#EXTM3U"):
                block.append(lines[i])
                i += 1
            
            url = block[-1].strip()
            if url.startswith("http"):
                if is_link_active(url):
                    active_blocks.extend(block)
        else:
            i += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(active_blocks)
    print("Pengecekan selesai, file 'hasil' diperbarui.")

if __name__ == "__main__":
    clean_and_check()
