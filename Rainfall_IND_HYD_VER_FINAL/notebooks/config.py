import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA = os.path.join(ROOT_DIR)

if __name__ == "__main__":
    print(ROOT_DIR)