import os


class PathClass:

    def rootpath(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def workpath(self):
        return os.getcwd()

    def join(self, *args):
        return os.path.join(*args)

    def abspath(self, path):
        return os.path.abspath(path)

    def normpath(self, path):
        return os.path.normpath(path)

    def rootpathcomplete(self, path):
        return self.normpath(self.join(self.rootpath(), path))

    def workpathcomplete(self, path):
        return self.normpath(self.join(self.workpath(), path))


if __name__ == "__main__":
    print(PathClass().rootpath())
    print(PathClass().rootpathcomplete('static/css.css'))
