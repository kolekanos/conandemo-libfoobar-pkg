import os
from conans import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps

class FooBarConan(ConanFile):
    name = "FooBar"
    version = "0.1.0"
    settings = "os", "compiler", "arch", "build_type"
    no_copy_source = True
    generators = "CMakeDeps", "virtualenv"

    def configure(self):
        # We're building a pure C library that does not depend on any C++ standard library.
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def requirements(self):
        self.requires("Foo/0.1.0@kolekanos/testing")
        self.requires("Bar/0.1.0@kolekanos/testing")

    def generate(self):
        # TODO: Why does Conan not pick up the environment variable by itself?
        tc = CMakeToolchain(self, generator=os.getenv("CONAN_CMAKE_GENERATOR", None))
        tc.preprocessor_definitions["CMAKE_TRY_COMPILE_TARGET_TYPE"] = "STATIC_LIBRARY"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def source(self):
        git = tools.Git(verify_ssl=False)
        git.clone(
            url="https://github.com/kolekanos/conandemo-libfoobar",
            branch="master",
            shallow=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = ["FooBar"]

