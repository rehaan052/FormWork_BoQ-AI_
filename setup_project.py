import os

# Root directories
folders = [
    "data",
    "data/raw",
    "data/processed",
    "src"
]

# Files to create
files = [
    "app.py",
    "requirements.txt",
    "README.md",
    "src/boq_calculation.py",
    "src/optimization.py",
    "src/inventory_logic.py",
    "src/utils.py"
]

def create_structure():
    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Create files
    for file in files:
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("")

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_structure()