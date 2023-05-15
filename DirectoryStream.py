import glob
import os
from Stream import Stream


class DirectoryStream(Stream):
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        return glob.glob(os.path.join("weatherfiles/", self.filepath))


