import json
import sys
import bencodepy

def decode_bencode(bencoded_value):
    def extract_string(data): 
        length, rest = data.split(b":", 1)
        length = int(length)
        return rest[:length], rest[length:]
    
    def decode(data):
        if data[0:1].isdigit(): #5:hello
            decoded_str, rest = extract_string(data)
            return decoded_str, rest
        
        elif data.startswith(b'i'): # i52e
            end = data.index(b'e')
            return int(data[1:end]), data[end+1:]
        
        elif data.startswith(b'l'): #l5:helloi52ee
            data = data[1:]
            result = []
            while not data.startswith(b'e'):
                item, data = decode(data)
                result.append(item)
            return result, data[1:] 
         
        elif data.startswith(b'd'): #d3:foo3:bar5:helloi52ee
            data = data[1:]
            result = []
            while not data.startswith(b'e'):
                item, data = decode(data)
                result.append(item)
            return result, data[1:] 

        else:
            raise NotImplementedError("Unsupported Bencode format")

    decoded_result, _ = decode(bencoded_value)
    return decoded_result 

def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()
            raise TypeError(f"Type not serializable: {type(data)}")

        decoded_result = decode_bencode(bencoded_value) 
        print(json.dumps(decoded_result, default=bytes_to_str))
    
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
