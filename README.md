# Kindle clippings to Notion uploader

This python script syncs your Kindle clippings with Notion.
Each book gets its own page in Notion, and each clipping is a block in that page.

When started with `./main.py watch`, the script will wait for your Kindle to be connected via USB.
It will then parse all clippings and upload new ones to Notion.
The script also makes a copy of the `my clippings.txt` file to iCloud.

In order to remember which clippings were already uploaded, a page called `LastImportStatus` is created in Notion.

# Requirements
Works only on MacOS.

# Installation
`pip install -r requirements.txt`  
Make sure to fill `.env` with your Notion integration token and the ID of the page containing your books.
The integration needs to be invited in the Notion UI to be allowed to make edits.

 # Motivation
After many years of not doing any backups, I finally realised that my Kindle clippings are very valuable to me.
I want to have the clippings always with me, on my phone and be able to add additional notes to them.
Also I wanted to take the opportunity to learn more about Python and using Copilot and ChatGPT for development.
