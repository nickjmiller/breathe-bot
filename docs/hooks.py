import shutil


def copy_readme(*args, **kwargs):
    shutil.copy("README.md", "docs/index.md")
    # Copy logo
    shutil.copy("assets/logo_256.png", "docs/assets/logo_256.png")
