import bencodepy
import hashlib
import urllib.request
import urllib.parse
import random
import struct
import json
import sys

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

def httpget(file):
    try:
        with open(file, "rb") as f:
            bencoded_value = f.read()

        decoded_data = bencodepy.decode(bencoded_value)
        tracker_url = decoded_data.get(b'announce', b'').decode()

        info_dict = decoded_data.get(b'info', {})
        bencoded_info = bencodepy.encode(info_dict)
        info_hash = hashlib.sha1(bencoded_info).digest()

        params = {
            "info_hash": info_hash,
            "peer_id": "-PC0001-001122334455",
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": decoded_data.get(b'info', {}).get(b'length', 0),
            "compact": 1,
        }

        url = f"{tracker_url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:
            response_data = response.read()

        decoded_response = bencodepy.decode(response_data)

        peers = decoded_response.get(b"peers", b"")
        peer_list = []

        # Decode peer list
        for i in range(0, len(peers), 6):
            ip = ".".join(str(b) for b in peers[i:i+4])
            port = struct.unpack("!H", peers[i+4:i+6])[0]
            peer_list.append(f"{ip}:{port}")

        return {"peers": peer_list}

    except Exception as e:
        print(f"Błąd: {e}")
        sys.exit(1)



def main():
    if  sys.argv[1] == "info":
        file_path = sys.argv[2]
        result = parse_file(file_path)

        print(json.dumps(result, indent=4))

    if sys.argv[1] == "peers":
        file_path = sys.argv[2]
        result = httpget(file_path)

        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
