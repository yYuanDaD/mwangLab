import os
import shutil


def reset_project():
    folders = ["./data", "./output"]

    print("Cleaning project environment...")

    for folder in folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"[FAIL] Could not delete {file_path}. Reason: {e}")
            print(f"[OK] Cleared directory: {folder}")
        else:
            os.makedirs(folder)
            print(f"Directory missing, created: {folder}")


if __name__ == "__main__":
    reset_project()
    print("\nProject environment reset. Ready for a new run.")
