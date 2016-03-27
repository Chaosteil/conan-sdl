from conans import ConanFile, CMake
from conans.tools import download, unzip, check_sha256
import os, shutil


class SDLConanFile(ConanFile):
    name = "sdl"
    version = "2.0.4"
    branch = "stable"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "gles": [True, False]}
    default_options = ("shared=True", "gles=False")
    generators = "cmake"
    license = "zlib/png"
    url = "http://github.com/chaosteil/conan-sdl"
    exports = ["CMakeLists.txt"]
    mercurial_archive = "330f500d5815"
    full_version = 'SDL2-2.0.4'


    def config(self):
        del self.settings.compiler.libcxx


    def source(self):
        zip_name = "%s.zip" % self.full_version
        # download("https://www.libsdl.org/release/%s" % zip_name, zip_name)
        # We use this mercurial package because it fixes a critical build error
        # on the latest Arch linux. Remove once SDL 2.0.5 is released.
        download("https://hg.libsdl.org/SDL/archive/%s.zip" % self.mercurial_archive, zip_name)
        check_sha256(zip_name, 'dd2816bd7551ed206a8687dad224d3651522551dd3669a97ed820ba641f89a51')
        unzip(zip_name)
        os.unlink(zip_name)

        folder_name = 'SDL-%s' % (self.mercurial_archive)
        self.run("chmod +x ./%s/configure" % folder_name)


    def build(self):
        folder_name = 'SDL-%s' % (self.mercurial_archive)
        cmake = CMake(self.settings)
        self.run("mkdir -p _build")
        cd_build = "cd _build"

        # This is a super hacky way to inject conan settings into the SDL CMake. :(
        command = cmake.command_line.replace('CONAN_', 'CMAKE_').replace('COMPILER', 'C_COMPILER')
        if self.settings.os == "Macos":
            command = command.replace('apple-clang', 'clang')

        options = " ".join([
            "-DVIDEO_OPENGLES=ON -DVIDEO_OPENGL=OFF" if self.options.gles else "-DVIDEO_OPENGLES=OFF -DVIDEO_OPENGL=ON"
        ])

        self.output.warn('%s && cmake ../%s %s %s' % (cd_build, folder_name, command, options))
        self.run('%s && cmake ../%s %s %s' % (cd_build, folder_name, command, options))
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
                self.copy(pattern="*.so*", dst="lib", src="_build", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="_build", keep_path=False)


    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ['SDL2-2.0']
        else:
            self.cpp_info.libs = ['SDL2']

        self.cpp_info.libs.extend(["m", "dl", "pthread"])

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("rt")
