from conans import CMake, ConanFile
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "chaosteil")

class SDLTestConanFile(ConanFile):
    name = "sdltest"
    version = "1.0"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "sdl/2.0.4@%s/%s" % (username, channel)

    def config(self):
        del self.settings.compiler.libcxx

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir -p _build")
        self.output.warn('cd _build && cmake .. %s' % cmake.command_line)
        self.run('cd _build && cmake .. %s' % cmake.command_line)
        self.output.warn('cd _build && cmake --build . %s' % cmake.build_config)
        self.run('cd _build && cmake --build . %s' % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run(os.path.join(".", "_build", "bin", "test"))
