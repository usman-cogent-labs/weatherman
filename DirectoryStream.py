import glob
import os
from Stream import Stream


class DirectoryStream(Stream):
    def read(self, file_path):
        return glob.glob(os.path.join("weatherfiles/", file_path))
