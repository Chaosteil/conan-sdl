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

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake . %s' % cmake.command_line)
        self.run('cmake --build . %s' % cmake.build_config)

    def test(self):
        self.run(os.path.join(".", "bin", "test"))
