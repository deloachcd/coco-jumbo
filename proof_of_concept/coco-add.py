import sys

from CocoEncrypter import CocoEncrypter
from CocoLocalSecret import CocoLocalSecret
from CocoPasswordFunctions import generate_password
from CocoValidators import identifier_is_valid

from constants import DEFAULT_COCODIR, DEFAULT_SECRET_FILENAME

if __name__ == "__main__":
    if not sys.argv[1:]:
        identifier = input("Enter identifier for new encrypted login "
                           "(or press 'q' to quit): ")
        if "q" in identifier.lower():
            exit()
    else:
        identifier = sys.argv[1]

    if not identifier_is_valid(identifier):
        print("Error: requested identifier is invalid.")
        exit(-1)

    local_secret_path = "{}/{}".format(DEFAULT_COCODIR, DEFAULT_SECRET_FILENAME)
    local_secret = CocoLocalSecret(path=local_secret_path)

    if local_secret.has_secret_at_path():
        local_secret.load_secret_from_filesystem()
    else:
        print("Error: cannot find local secret at {}".format(local_secret_path))
        exit(-1)

    key = local_secret.get_key()
    encrypter = CocoEncrypter.from_key(key)
    encrypted_password = encrypter.encrypt(generate_password(16).encode("utf-8"))

    file_content = (
        local_secret.get_salt() + encrypted_password + local_secret.get_hash()
    )
    output_path = "{}/{}.cj".format(DEFAULT_COCODIR, identifier)
    with open(output_path, "wb") as outfile:
        outfile.write(file_content)
