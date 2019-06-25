import os
import attr

from constants import SALTSIZE, DEFAULT_COCODIR, PK_HEADER, PK_FOOTER, HASHSIZE


class SecretNotLoadedException(Exception):
    pass


@attr.s
class CocoEncryptedContent:
    path = attr.ib(default="{}/{}".format(DEFAULT_COCODIR, "encrypted.cj"))
    secret = attr.ib(default=None)

    def write_to_filesystem(self, content):
        file_content = PK_HEADER + content + PK_FOOTER
        with open(self.path, 'wb') as outfile:
            outfile.write(file_content)

    def has_secret_at_path(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as instance_path:
                return b'COCOJUMBO LOCAL SECRET' in instance_path.read()
        else:
            return False

    def load_secret_from_filesystem(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as local_secret_file:
                self.secret = local_secret_file.read()
        else:
            raise FileNotFoundError("Cannot find local secret at {}".format(
                self.path
            ))

    def has_secret_loaded(self):
        return (self.secret is not None
                and b'COCOJUMBO LOCAL SECRET' in self.secret)

    def get_key(self):
        if self.has_secret_loaded():
            return self.secret[len(PK_HEADER)+SALTSIZE:
                               -(len(PK_FOOTER)+HASHSIZE)]
        else:
            raise SecretNotLoadedException(
                "No secret loaded to obtain key from."
            )

    def get_salt(self):
        if self.has_secret_loaded():
            return self.secret[len(PK_HEADER):len(PK_HEADER)+SALTSIZE]
        else:
            raise SecretNotLoadedException(
                "No secret loaded to obtain salt from."
            )

    def get_hash(self):
        if self.has_secret_loaded():
            return self.secret[-(len(PK_FOOTER)+HASHSIZE):-len(PK_FOOTER)]
        else:
            raise SecretNotLoadedException(
                "No secret loaded to obtain hash from."
            )
