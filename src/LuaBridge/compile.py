import os
import sys
import subprocess
from pathlib import Path
import shutil

IMAGE_NAME = "luabridge-builder"
CONTAINER_NAME = "luabridge-temp"
OUTPUT_FILE = "LuaBridge.so"
PYI_FILE = "LuaBridge.pyi"

def run(cmd, error_message):
    print(f"> {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(error_message)
        sys.exit(1)

def main():
    # Get directory of this script
    script_dir = Path(__file__).resolve().parent
    print(f"Changing to script directory: {script_dir}")
    os.chdir(script_dir)

    # Build Docker image
    print("Building Docker image...")
    run(
        ["docker", "build", "-t", IMAGE_NAME, "."],
        "Docker build failed!"
    )

    # Create temporary container
    print("Creating temporary container...")
    run(
        ["docker", "create", "--name", CONTAINER_NAME, IMAGE_NAME],
        "Container creation failed!"
    )

    try:
        # Destination path: ../WebHeroes/
        output_dir = (script_dir / ".." / "WebHeroes").resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Copy the shared library
        so_destination = output_dir / OUTPUT_FILE
        print(f"Copying {OUTPUT_FILE} to {so_destination}...")
        run(
            ["docker", "cp", f"{CONTAINER_NAME}:/build/{OUTPUT_FILE}", str(so_destination)],
            "Failed to copy output file!"
        )

        # Copy the .pyi file
        pyi_source = script_dir / PYI_FILE
        pyi_destination = output_dir / PYI_FILE
        if pyi_source.exists():
            print(f"Copying {PYI_FILE} to {pyi_destination}...")
            shutil.copy(pyi_source, pyi_destination)
        else:
            print(f"Warning: {PYI_FILE} not found in {script_dir}")

    finally:
        # Cleanup container even if copy fails
        print("Cleaning up...")
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL)

    print("========================================")
    print(f"Build complete: {OUTPUT_FILE} + {PYI_FILE}")
    print("========================================")

if __name__ == "__main__":
    main()
