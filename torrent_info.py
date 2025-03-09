import json
import sys
import bencodepy

def parse_file(file):
    try:
        with open(file, "rb") as f:
            decoded_data=bencodepy.decode(f.read())

        tracker_url = decoded_data.get(b'announce', b'').decode() 
        length = decoded_data.get(b'info', {}).get(b'length', 0) 
        return {
            "Tracker URL": tracker_url,
            "Length": length
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
