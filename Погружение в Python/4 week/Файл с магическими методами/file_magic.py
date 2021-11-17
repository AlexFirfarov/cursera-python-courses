import tempfile


class File:

    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.current = 0

        with open(storage_path, 'a'):
            pass

    def __add__(self, other):
        file, filename = tempfile.mkstemp()
        file_obj = File(filename)
        file_obj.write(self.read() + other.read())
        return file_obj

    def __str__(self):
        return self.storage_path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.storage_path, 'r') as f:
            for _ in range(0, self.current):
                f.readline()
            self.current += 1
            line = f.readline()

            if not line:
                self.current = 0
                raise StopIteration
            return line

    def read(self):
        with open(self.storage_path, 'r') as f:
            return f.read()

    def write(self, text):
        with open(self.storage_path, 'w') as f:
            f.write(text)
