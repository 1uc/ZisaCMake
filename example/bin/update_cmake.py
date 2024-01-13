#! /usr/bin/env python3

from zisa_cmake import recurse, NotMainTarget, Target

class AnythingTarget(Target):
    def __init__(self, cmake_target):
        self._cmake_target = cmake_target

    def requires(self, path) -> bool:
        return True

    @property
    def cmake_guard(self):
        return "BUILD_TESTS"

    @property
    def cmake_target(self):
        return self._cmake_target


if __name__ == "__main__":
    recurse("src/", [NotMainTarget("utils")])
    recurse("tests/", [AnythingTarget("unit_tests")])
