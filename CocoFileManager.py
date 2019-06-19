import os

import attr

from constants import DEFAULT_COCODIR


@attr.s
class CocoFileManager:
    cocodir = attr.ib(default=os.path.expanduser(DEFAULT_COCODIR))

    def ensure_cocodir_exists(self):
        if not os.path.exists(self.cocodir):
            os.makedirs(self.cocodir)

    def write_bytes_to_file(self, content, filename):
        with open("{}/{}".format(self.cocodir, filename), 'wb') as outfile:
            outfile.write(content)
