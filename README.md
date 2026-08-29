# File Downloader

Grabs document links off a web page and downloads them for you instead of clicking through a website one PDF at a time.

## What it does

- Loads a page and finds the document links in it
- Downloads each one
- Names the files properly based on the link text (with an optional prefix for context) instead of leaving you with a folder full of "document.pdf", "document(1).pdf", etc.

## Context
I got tired of manually downloading files off a site one by one. 

## Setup
pip install -r requirements.txt

## Usage
Open `automate.py` and fill in the config values at the of the `main` func (page URL, div/tag classes to target, site domain, save folder), then run:
python automate.py
