import csv
import logging

from cryptography.fernet import Fernet

log = logging.getLogger(__name__)


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    # @TODO: Make this dynamic - i.e. from config, or ENVVAR
    return open("./secure/key.key", "rb").read()


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def decrypted_csv_data(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file
    and returns the decrypted data in CSV lines
    """
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            # read the encrypted data
            encrypted_data = file.read()
        # decrypt data
        return f.decrypt(encrypted_data).decode('utf-8').splitlines()
    except Exception as e:
        log.error(str(e))


def search_encrypted_file(keyword, filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)

    print(keyword)

    keyword = keyword.lower()

    lines = decrypted_data.decode('utf-8').splitlines()

    results = []

    for line in csv.reader(lines):
        print(line)
        # [0] = label
        # [2] = definition
        if keyword in line[0].lower():
            results.append({'label': '{0} - {1}'.format(line[0], line[2]), 'uri': line[1]})
        elif keyword in line[2].lower():
            results.append({'label': '{0} - {1}'.format(line[0], line[2]), 'uri': line[1]})

    print(results)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Encryptor Script")
    parser.add_argument("file", help="File to encrypt/decrypt")
    parser.add_argument("-g", "--generate-key", dest="generate_key", action="store_true",
                        help="Whether to generate a new key or use existing")
    parser.add_argument("-e", "--encrypt", action="store_true",
                        help="Whether to encrypt the file, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Whether to decrypt the file, only -e or -d can be specified.")
    parser.add_argument("-s", "--search", action="store_true",
                        help="Search an encrypted file. Must include the -k argument too.")
    parser.add_argument("-k", "--keyword", action="store_true",
                        help="Keyword to be searched. Must include the -s argument too.")

    args = parser.parse_args()
    file = args.file
    generate_key = args.generate_key

    if generate_key:
        write_key()
    # load the key
    key = load_key()

    encrypt_ = args.encrypt
    decrypt_ = args.decrypt
    search = args.search
    keyword = args.keyword

    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        encrypt(file, key)
    elif decrypt_:
        decrypt(file, key)
    elif search:
        search_encrypted_file('ng', file, key)
    else:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
