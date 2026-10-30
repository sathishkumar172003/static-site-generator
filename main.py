from src.file_helpers import cleanDir, copyDir
from src.markdown_helpers import generate_page, generate_pages_recursive
import os 
import sys


OUTPUT_DIR = os.path.join(os.getcwd(), "docs")
MD_PATH = os.path.join(os.getcwd(), "content")
TEMPLATE_PATH = os.path.join(os.getcwd(),  "template.html")

def run(basepath=None):
    if basepath is None:
        basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Clean the output directory
    if os.path.exists(OUTPUT_DIR):
        print("Cleaning output directory...")
        cleanDir(OUTPUT_DIR)
    else:
        os.makedirs(OUTPUT_DIR) 
    # copy static files to output directory
    print("Copying static files to output directory...")
    static_dir = os.path.join(os.getcwd(), "static")
    if os.path.exists(static_dir):
        copyDir(static_dir, OUTPUT_DIR)
    generate_pages_recursive(MD_PATH, TEMPLATE_PATH, OUTPUT_DIR, basepath)


if __name__ == "__main__":
    run()