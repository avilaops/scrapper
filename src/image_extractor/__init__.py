# Image Extractor Module
"""
Extrator de imagens com OCR utilizando Tesseract e armazenamento em SQLite.
"""

from .image_extractor import ImageExtractor
from .tesseract_config import *

__all__ = ['ImageExtractor']
