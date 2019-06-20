import os
from time import sleep
import sys

import pyperclip

from CocoLocalSecret import CocoLocalSecret
from CocoEncrypter import CocoEncrypter
from CocoValidators import identifier_is_valid
from constants import DEFAULT_COCODIR, DEFAULT_SECRET_FILENAME, SALTSIZE, HASHSIZE


if __name__ == "__main__":
    if not sys.argv[1:]:
        identifier = input("Enter identifier to load password on clipboard "
                           "(or press 'q' to quit): ")
        if "q" in identifier.lower():
            exit()
    else:
        identifier = sys.argv[1]

    if not identifier_is_valid(identifier):
        print("Error: requested identifier is invalid.")
        exit(-1)
    derived_file_location = "{}/{}.cj".format(DEFAULT_COCODIR,
                                              identifier)
    if not os.path.exists(derived_file_location):
        print("Error: login associated with requested identifier not found.")
        exit(-1)

    old_clipboard_content = pyperclip.paste()
    secret_path = "{}/{}".format(
        DEFAULT_COCODIR, DEFAULT_SECRET_FILENAME
    )
    local_secret = CocoLocalSecret(path=secret_path)
    local_secret.load_secret_from_filesystem()
    encrypter = CocoEncrypter.from_key(local_secret.get_key())
    with open(derived_file_location, 'rb') as encrypted_data:
        password_bytes = encrypter.decrypt(encrypted_data.read()[SALTSIZE:-HASHSIZE])
    print("Copying password to clipboard for 10 seconds...")
    pyperclip.copy(password_bytes.decode('utf-8'))
    sleep(10)
    pyperclip.copy(old_clipboard_content)
    print("Done!")
