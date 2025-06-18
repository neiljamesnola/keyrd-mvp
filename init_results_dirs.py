import os

def create_results_structure(base_dir="results"):
    subdirs = ["resilient", "stress_eater", "fatigue_sensitive"]

    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created base directory: {base_dir}")
    else:
        print(f"Base directory already exists: {base_dir}")

    # Create subdirectories
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created subdirectory: {path}")
        else:
            print(f"Subdirectory already exists: {path}")

if __name__ == "__main__":
    create_results_structure()
