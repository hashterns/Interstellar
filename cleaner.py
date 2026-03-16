import os
import re

# The complete list of keywords, hosting platforms, and obfuscated variations
WORDS_TO_REMOVE = [
    "proxy", "webproxy", "proxy-server", "proxy-site", "proxy-list", "cgi-proxy",
    "php-proxy", "vpn", "tunnel", "ssh-tunnel", "shadowsocks", "v2ray", "wireguard",
    "openvpn", "bypass", "circumvention", "relay", "mirror", "mirror-site",
    "stealth-proxy", "masked-url", "encrypted-tunnel", "proxy-browser", "anonymizer",
    "unblock", "unblocked", "unblocking", "unblocked-games", "unblocked-at-school",
    "unblocked-at-work", "unblocked-at-uni", "filter-bypass", "whitelist-bypass",
    "site-unblocker", "unblock-link", "working-link", "latest-mirror",
    "premium-unblocked", "restricted-access-bypass", "games", "browser-games",
    "flash-games", "html5-games", "io-games", "emulator", "roms", "online-games",
    "retro-games", "web-games", "roblox", "minecraft", "slope-game", "run-3",
    "tetris-unblocked", "cookie-clicker", "bitlife", "krunker", "surviv.io",
    "agar.io", "slither.io", "1v1.lol", "friday-night-funkin", "github.io",
    "vercel.app", "netlify.app", "herokuapp", "glitch.me", "replit.com",
    "pages.dev", "workers.dev", "g4mes", "unbl0cked", "pr0xy", "p-r-o-x-y",
    "p.r.o.x.y", "g.a.m.e.s", "un-blocked", "prxy"
]

def clean_html_files(directory_path):
    # Sort words by length in descending order. 
    # This ensures compound words (e.g., 'proxy-server') are removed 
    # BEFORE shorter standalone words (e.g., 'proxy') trigger a partial match.
    sorted_words = sorted(WORDS_TO_REMOVE, key=len, reverse=True)
    
    # Escape special characters (like dots in agar.io) to ensure literal regex matches
    escaped_words = [re.escape(word) for word in sorted_words]
    
    # Create a case-insensitive regex pattern matching any of the words
    # (?i) makes it case-insensitive so it catches "Proxy", "GAMES", etc.
    pattern = re.compile(r'(?i)(' + '|'.join(escaped_words) + r')')

    files_modified = 0

    # Walk through the directory and process every HTML file
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replace matches with an empty string
                new_content = pattern.sub('', content)

                # If the content changed, write it back to the file
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Cleaned keywords from: {filepath}")
                    files_modified += 1

    print(f"\nCleanup complete. Modified {files_modified} file(s).")

if __name__ == "__main__":
    # Define the directory where your HTML files are stored. 
    # '.' represents the current directory.
    target_directory = "." 
    
    print(f"Scanning directory: {os.path.abspath(target_directory)}")
    clean_html_files(target_directory)
