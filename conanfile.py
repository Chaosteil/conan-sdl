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

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir build")
        self.run('cd build && cmake ../%s -DBUILD_SHARED_LIBS=%s '
                 '-DCMAKE_INSTALL_PREFIX=../install %s' %
            ('SDL-' + self.mercurial_archive, "ON" if self.options.shared else "OFF",
             cmake.command_line))
        self.run('cd build && cmake --build . %s -- -j2 install' %
                 cmake.build_config)

    def package(self):
        self.copy('*.*', 'include', 'install/include', keep_path=True)
        self.copy(pattern="*.a", dst="lib", src="install/lib", keep_path=False)
        self.copy(pattern="*.so." + self.so_version, dst="lib", src="install/lib", keep_path=False)

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs.append(':libSDL2-2.0.so.' + self.so_version)
        else:
            self.cpp_info.libs.extend(['SDL2', 'SDL2main'])

        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["m", "dl", "pthread", "rt"])
