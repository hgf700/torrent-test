import sys
import re
import urllib.parse
import hashlib

def parse_magnet(magnet_link):
    match = re.search(r"xt=urn:btih:([a-fA-F0-9]+)", magnet_link)
    if match:
        info_hash = match.group(1)
    else:
        info_hash = "Nie znaleziono"
    
    sha1_hash = hashlib.sha1(bytes(info_hash, 'utf-8')).hexdigest()

    match_dn = re.search(r"dn=([^&]+)", magnet_link)
    file_name = match_dn.group(1) if match_dn else "Nie znaleziono"

    match_tr = re.search(r"tr=([^&]+)", magnet_link)
    tracker_url = urllib.parse.unquote(match_tr.group(1)) if match_tr else "Nie znaleziono"
    
    print(f"Info Hash: {sha1_hash}")
    print(f"Nazwa pliku: {file_name}")
    print(f"Tracker URL: {tracker_url}")

    
def main():
    if  sys.argv[1] == "magnet_parse":

        magnet_link = sys.argv[2]
        parse_magnet(magnet_link)

if __name__ == "__main__":
    main()
