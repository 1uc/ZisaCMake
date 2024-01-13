# ZisaCMake: Utilities for CMake

## Listing Source Files
This repository contains a Python package list of source files for CMake
projects. Since `GLOB` doesn't play nice with Git, e.g. switching branches that
add or remove files, and writing down the list of files is too tedious for my
taste, a third option in needed. Namely automatically generate the list of
files.

The assumption about the CMake project are:

 * that it concentrates all actual CMake code in the top-level `CMakeLists.txt`.
 * that it's easy to programmatically assign source files to their CMake target
   based on their path alone.

The Python package will then generate a `CMakeLists.txt` in each subfolder
containing source files. This `CMakeLists.txt` lists all files in that
subfolder and includes any subfolders of that folder.

Please check `example`.

### Installation
Either clone and then install or just directly point `pip` at the repository:

    pip install git+https://github.com/1uc/ZisaCMake.git
