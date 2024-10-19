from pathlib import Path


class PathClass:

    def rootpath(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def workpath(self) -> Path:
        return Path.cwd()

    def rootpathcomplete(self, path: str) -> Path:
        return self.rootpath() / path

    def workpathcomplete(self, path: str) -> Path:
        return self.workpath() / path

class InputCheck:

    def check_type_empty(self, value, types) -> bool:
        """
        检查值的类型是否符合要求，且不为空。

        Args:
            value: 要检查的值。
            types: 要求的类型，可以是单个类型或类型元组。

        Returns:
            bool: 如果值的类型符合要求且不为空，则返回 True；否则返回 False。
        """
        if self.is_empty(value):
            return False
        if not self.check_type(value, types):
            return False
        return True

    def is_empty(self, value) -> bool:
        """
        检查各种类型的值是否为空。

        Args:
            value: 要检查的值，可以是字符串、列表、字典、集合、元组等。

        Returns:
            bool: 如果值为空，则返回 True；否则返回 False。
        """
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, (list, dict, set, tuple)) and len(value) == 0:
            return True
        return False

    def check_type(self, value, types) -> bool:
        """
        检查值的类型是否符合要求。

        Args:
            value: 要检查的值。
            types: 要求的类型，可以是单个类型或类型元组。

        Returns:
            bool: 如果值的类型符合要求，则返回 True；否则返回 False。
        """
        if isinstance(types, type):
            types = (types,)
        return isinstance(value, types)


if __name__ == "__main__":
    print(PathClass().rootpath())
    print(type(PathClass().rootpath()))
    print(PathClass().workpath())
    print(type(PathClass().workpath()))