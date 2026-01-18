#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

# =========================================
# Build LuaBridge Linux .so using Docker
# Cross-platform Python version
# =========================================

IMAGE_NAME = "luabridge-builder"
CONTAINER_NAME = "luabridge-temp"
OUTPUT_FILE = "LuaBridge.so"

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
        # Destination path: ../WebHeroes/LuaBridge.so
        destination = (script_dir / ".." / "WebHeroes" / OUTPUT_FILE).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)

        print(f"Copying {OUTPUT_FILE} to {destination}...")
        run(
            ["docker", "cp", f"{CONTAINER_NAME}:/build/{OUTPUT_FILE}", str(destination)],
            "Failed to copy output file!"
        )

    finally:
        # Cleanup container even if copy fails
        print("Cleaning up...")
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stdout=subprocess.DEVNULL)

    print("========================================")
    print(f"Build complete: {OUTPUT_FILE}")
    print("========================================")

if __name__ == "__main__":
    main()
