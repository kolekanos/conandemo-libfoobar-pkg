import os
from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class MyLibConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "virtualenv"

    def generate(self):
        # TODO: Why does Conan not pick up the environment variable by itself?
        tc = CMakeToolchain(self, generator=os.getenv("CONAN_CMAKE_GENERATOR", None))
        tc.preprocessor_definitions["CMAKE_TRY_COMPILE_TARGET_TYPE"] = "STATIC_LIBRARY"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run("echo Created the following test file:")
        self.run("file example")
        if not tools.cross_building(self.settings):
            self.run("echo Running the example:")
            self.run("example")

