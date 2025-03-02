"""Defines several custom matplotlib colormaps.

Copyright (c) 2024 The INVRS-IO authors.
"""

import base64
import pathlib
import zlib
from typing import Any, Sequence

import numpy as onp
from matplotlib import colors

_DATA_PATH = f"{pathlib.Path(__file__).resolve().parent}/data"


# Code is from https://github.com/rsmith-nl/wavelength_to_rgb.
_CTBL = (
    b"eNrV0ltr0AUAxuHn1rqoiAqSiA6EEJ3ogBUJeeFFRUdJOjOyWau1bLZpGztnM1oyy"
    b"2yYmcmMETPNlixNVpmssobKMJuYDVnNGksz0zTe5C9BXyF4v8Dz4y1RMlPpLGVlKs"
    b"pVVqh+Vu0cDVVa5mqdp61Ge63FdTrqLWuwolFno64m3U3WNutp1ttsY7O+Jpub9Df"
    b"a2migwY56O+sM1dpTY3iekblGq4zNcWC2QxWOlDtWJqVSIg/JfTJd7pRbZZpMlZtk"
    b"slwtl8skuUjOk3PkDDlFnNipcWZMjAtjUlwR18aNcXNMi9virpgRD0ZJlMZTMTuqo"
    b"ibqoyUWxCuxKJbEm/F2dEZXrI4PYn1siL7YHP3xTWyLwfg+9sRwjMT+GI/f4884Fj"
    b"mxP2S/7JVB+Vr6pEe65C1ZJC9KjTxduKcX1smF74TMhDgtzopz4/y4uGBdFlfFdXF"
    b"DTImpBe6WuD3ujnvj/ni4ID4WTxTKZ6IyqgtoXTTGC9EaL8fCgvt6dPwrXhmrCnR3"
    b"rIl18VH0xicF/fPYEl/G1hiI7UWA72KoaPBj7Iufigxj8VtR4nAcjeMnYxyXo3JYD"
    b"sq4/CqjMiLD8oPsll1Fp+0yUNTqly/kU9kkG2S9fChrpLtIuErekeWyVN6Q16Rd2m"
    b"SBzJcmqSvqVkulVMiTMkselUfkAZkh98gd/znZFLlerpEr5VK5RC6QiXK2nC4TTv7"
    b"sf7C/OcZfHOEwhzjIAcYZ4xdG+ZkR9jHMXvawmyF2sZNBdrCNAb5lK1/RzxY28xl9"
    b"bGIjH9PLenpYx1rep5v36OJdOlnJCpazjKV0sITFvEo7C2njJVqZTwtNNFBHLc9Tz"
    b"XNUMpsKyinjcUqZSQn/AJ7p9HY="
)


_CTBL = zlib.decompress(base64.b64decode(_CTBL))


def rgb_for_wavelength(wavelength_nm: float) -> onp.ndarray[Any, Any]:
    """Converts a wavelength between 380 and 780 nm to an RGB color tuple.

    Args:
        wavelength_nm: Wavelength in nanometers. It is rounded to the nearest integer.

    Returns:
        A 3-tuple (red, green, blue) of integers in the range 0-255.
    """
    wavelength_nm = int(round(wavelength_nm))
    if wavelength_nm < 380 or wavelength_nm > 780:
        raise ValueError("wavelength out of range")
    idx = (wavelength_nm - 380) * 3
    color_str = _CTBL[idx : idx + 3]
    return onp.asarray([int(i) for i in color_str]) / 255


def cmap_for_wavelength(
    wavelength_nm: float,
    background_color: str | Sequence[float] = "k",
) -> colors.LinearSegmentedColormap:
    """Generate a colormap for the specified wavelength.

    The colormap varies between the background color, and the color associated with the
    specified wavelength.

    Args:
        wavelength_nm: The wavelength, with values between 380 and 780 nanometers.
        background_color: A color that can be understood by matplotlib, e.g. `"w"`,
            `"k"`, or `(0.1, 0.1, 0.1)`.

    Returns:
        The generated colormap.
    """
    color = rgb_for_wavelength(wavelength_nm=wavelength_nm)
    return colors.LinearSegmentedColormap.from_list(
        name=f"{int(wavelength_nm)}_{background_color}",
        colors=[background_color, color],  # type: ignore[arg-type]
        N=256,
    )


def wbgyr() -> colors.ListedColormap:
    """Returns the white-blue-yellow-green-red colormap."""
    cmap_colors = onp.loadtxt(f"{_DATA_PATH}/wbgyr.txt", delimiter=",")
    return colors.ListedColormap(cmap_colors)
