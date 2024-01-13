#! /usr/bin/env python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2021 ETH Zurich, Luc Grosheintz-Laval
# Copyright (c) 2023 Luc Grosheintz-Laval

import glob
import os
import errno
import os.path


def find_files(folder, suffixes):
    files = sum((glob.glob("{}*{}".format(folder, s)) for s in suffixes), [])
    return list(sorted(files))


def find_source_files(folder):
    suffixes = [".c", ".C", ".cpp", ".c++", ".cu", ".h", ".hpp", ".cuh"]
    return find_files(folder, suffixes)


def find_subdirectories(folder):
    dirs = sorted(glob.glob(folder + "*/"))
    return [d for d in dirs if "CMake" not in d]


def format_sources(target, sources) -> str:
    ret = ""

    line_pattern = "  {:s} ${{CMAKE_CURRENT_LIST_DIR}}/{:s}"

    if sources:
        ret += "\n".join(
            [
                "target_sources(" + target.cmake_target,
                *[
                    line_pattern.format(target.cmake_visibility, os.path.basename(s))
                    for s in sources
                ],
                ")\n",
            ]
        )

    return ret


def add_subdirectory(folder) -> str:
    line_pattern = "add_subdirectory({:s})\n"
    return line_pattern.format(os.path.basename(folder[:-1]))


def remove_file(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def append_to_file(filename, text):
    with open(filename, "a") as f:
        f.write(text)


def recurse(base_directory, targets) -> bool:
    cmake_file = base_directory + "CMakeLists.txt"
    remove_file(cmake_file)

    source_files = find_source_files(base_directory)
    non_empty = False

    for target in targets:
        filtered_sources = list(
            filter(lambda path: target.requires(path), source_files)
        )

        if filtered_sources:
            wrapped_sources = target.wrap_sources(
                format_sources(target, filtered_sources)
            )

            append_to_file(cmake_file, wrapped_sources)
            non_empty = True

    for d in find_subdirectories(base_directory):
        if recurse(d, targets):
            append_to_file(cmake_file, add_subdirectory(base_directory + d))
            non_empty = True

    return non_empty


class Target:
    """Interface for adding sources to CMake targets.

    When `requires(path)` is true then it adds:
        target_sources({cmake_target} {cmake_visibility} {path})

    It will call `wrap_sources` which enables adding code before and after
    the `target_sources`. The default implementation adds:
        if({cmake_guard})
        ...
        endif()

    if `cmake_guard` is not `None`; and does nothing otherwise.
    """

    def wrap_sources(self, formatted_sources: str) -> str:
        if self.cmake_guard is None:
            return formatted_sources

        else:
            return "\n".join(
                [
                    f"if({self.cmake_guard})",
                    formatted_sources,
                    f"endif()\n\n",
                ]
            )

    def requires(self, path) -> bool:
        raise NotImplementedError("Missing implementation of `requires`.")

    @property
    def cmake_visibility(self):
        return "PRIVATE"

    @property
    def cmake_guard(self):
        raise NotImplementedError("Missing implementation of `cmake_guard`.")

    @property
    def cmake_target(self):
        raise NotImplementedError("Missing implementation of `cmake_target`.")


class NotMainTarget(Target):
    def __init__(self, cmake_target):
        self._cmake_target = cmake_target

    def requires(self, path) -> bool:
        return not "_main." in os.path.basename(path)

    @property
    def cmake_guard(self):
        return None

    @property
    def cmake_target(self):
        return self._cmake_target
