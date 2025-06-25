import os
import shutil


def on_startup(*args, **kwargs):
    shutil.copy("README.md", "docs/index.md")
    # Copy logo
    os.makedirs("docs/assets", exist_ok=True)
    shutil.copy("assets/logo_256.png", "docs/assets/logo_256.png")
