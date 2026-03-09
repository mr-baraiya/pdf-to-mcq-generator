#!/usr/bin/env bash
set -e

# Install system packages required for OCR (needs sudo on Render)
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-eng poppler-utils

# Install Python dependencies
pip install -r requirements.txt