import os
import shutil


def copy_readme(*args, **kwargs):
    shutil.copy("README.md", "docs/index.md")
    # Copy logo
    os.makedirs("docs/assets", exist_ok=True)
    shutil.copy("assets/logo_256.png", "docs/assets/logo_256.png")
