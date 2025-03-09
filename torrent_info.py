import json
import sys
import bencodepy
import hashlib

def parse_file(file):
    try:
        with open(file, "rb") as f:
            decoded_data=bencodepy.decode(f.read())

        tracker_url = decoded_data.get(b'announce', b'').decode() 
        length = decoded_data.get(b'info', {}).get(b'length', 0) 
        to_code = decoded_data.get(b'info',{})
        coded = bencodepy.encode(to_code)
        hash = hashlib.sha1(coded).hexdigest()

        return {
            "Tracker URL": tracker_url,
            "Length": length,
            "Coded SHA1" : hash
        }

    except Exception as e:
        print(e)
        sys.exit(1)

def main():
    command = sys.argv[1]

    if command == "info":
        file_path = sys.argv[2]
    result = parse_file(file_path)

    print(json.dumps(result, indent=4))
    

if __name__ == "__main__":
    main()
