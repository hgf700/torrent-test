import json
import sys
import bencodepy
import hashlib

def parse_file(file):
    try:
        with open(file, "rb") as f:
            decoded_data = bencodepy.decode(f.read())

        tracker_url = decoded_data.get(b'announce', b'').decode()
        length = decoded_data.get(b'info', {}).get(b'length', 0)
        to_code = decoded_data.get(b'info', {})
        coded = bencodepy.encode(to_code)
        info_hash = hashlib.sha1(coded).hexdigest()
        piece_length = decoded_data.get(b'info', {}).get(b'piece length', 0)
        pieces = decoded_data.get(b'info', {}).get(b'pieces', b'')
        # show pieces in 20 long parts
        piece_hashes = [pieces[i:i+20].hex() for i in range(0, len(pieces), 20)]

        return {
            "Tracker URL": tracker_url,
            "Length": length,
            "Info Hash": info_hash,
            "Piece Length": piece_length,
            "Piece Hashes": piece_hashes
        }

    except Exception as e:
        print(f"Błąd: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "info":
        print("Użycie: python main.py info <ścieżka_do_pliku.torrent>")
        sys.exit(1)

    file_path = sys.argv[2]
    result = parse_file(file_path)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
