import os
import shutil


def cleanup_intermediate():
    inter_dir = "intermediate"
    if not os.path.exists(inter_dir):
        print(f"{inter_dir} does not exist, skip cleanup.")
        return

    removed_files = 0
    removed_dirs = 0

    for name in os.listdir(inter_dir):
        path = os.path.join(inter_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
            removed_files += 1
        elif os.path.isdir(path):
            shutil.rmtree(path)
            removed_dirs += 1

    print(
        f"Intermediate cleanup complete. "
        f"Removed files: {removed_files}, removed dirs: {removed_dirs}."
    )


if __name__ == "__main__":
    cleanup_intermediate()
