from conans import ConanFile, CMake
from conans.tools import download, unzip, check_sha256
import os, shutil

class SDLConanFile(ConanFile):
    name = "sdl"
    version = "2.0.4"
    branch = "stable"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    license = "zlib/png"
    url = "http://github.com/chaosteil/conan-sdl"
    exports = ["CMakeLists.txt"]
    so_version = "0.4.0"
    mercurial_archive = "330f500d5815"

    full_version = 'SDL2-2.0.4'

    def source(self):
        zip_name = "%s.zip" % self.full_version
        # download("https://www.libsdl.org/release/%s" % zip_name, zip_name)
        # We use this mercurial package because it fixes a critical build error
        # on the latest Arch linux. Remove once SDL 2.0.5 is released.
        download("https://hg.libsdl.org/SDL/archive/%s.zip" % self.mercurial_archive, zip_name)
        check_sha256(zip_name, 'dd2816bd7551ed206a8687dad224d3651522551dd3669a97ed820ba641f89a51')
        unzip(zip_name)
        os.unlink(zip_name)

    def config(self):
        del self.settings.compiler.libcxx

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir build")
        self.run('cd build && cmake ../%s -DBUILD_SHARED_LIBS=%s '
                 '-DCMAKE_INSTALL_PREFIX=../install %s' %
            ('SDL-' + self.mercurial_archive, "ON" if self.options.shared else "OFF",
             cmake.command_line))
        self.run('cd build && cmake --build . %s -- -j2 install' %

                 cmake.build_config)
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        folder_name = 'SDL-%s' % (self.mercurial_archive)
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.run("cd %s &&  mkdir _build" % folder_name)
            cd_build = "cd %s && cd _build" % folder_name
            arch = "-m32 " if self.settings.arch == "x86" else ""
            self.run("cd %s && CFLAGS='%s -fPIC -O3' ./configure" % (folder_name, arch))
            if self.settings.os == "Macos":
                old_str = 'LDSHARED=gcc -dynamiclib -install_name ${exec_prefix}/lib/libz.1.dylib'
                new_str = 'LDSHARED=gcc -dynamiclib -install_name libz.1.dylib'
                replace_in_file("./%s/Makefile" % folder_name, old_str, new_str)
            self.run("cd %s && make" % folder_name)
        else:
            cmake = CMake(self.settings)
            self.run("mkdir _build")
            cd_build = "cd _build"
            self.output.warn('%s && cmake .. %s' % (cd_build, cmake.command_line))
            self.run('%s && cmake .. %s' % (cd_build, cmake.command_line))
            self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
            self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        folder_name = 'SDL-%s' % (self.mercurial_archive)
        self.copy("*.h", "include", "%s" % (folder_name), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", src=folder_name, keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="%s/_build" % folder_name, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=folder_name, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['SDL2', 'SDL2main']
