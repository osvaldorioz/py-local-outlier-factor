from setuptools import setup
from torch.utils.cpp_extension import CppExtension, BuildExtension
import pybind11

setup(
    name="lof",
    ext_modules=[
        CppExtension(
            "lof",
            ["lof.cpp"],
            include_dirs=[pybind11.get_include()],
            extra_compile_args=["-std=c++20", "-O3"],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
)