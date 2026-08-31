# Downloads dir file organizer

import asyncio
from time import time
from os import getlogin
from shutil import move
from pathlib import Path

pc_uname = getlogin()
downloads_dir = Path(f"C:/Users/{pc_uname}/Downloads")
done_files = []
stable_files = []
default_categories = {
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
  "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
  "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
  "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
  "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
  "Web Files": [".html", ".css", ".js", ".json", ".xml"],
  "Executables": [".exe", ".msi", ".dmg", ".pkg", ".sh", ".bat"],
  "Temp Files": [".tmp"],
}

images_dir = Path(f"{downloads_dir.resolve()}/Images")
documents_dir = Path(f"{downloads_dir.resolve()}/Documents")
audio_dir = Path(f"{downloads_dir.resolve()}/Audio")
videos_dir = Path(f"{downloads_dir.resolve()}/Videos")
archives_dir = Path(f"{downloads_dir.resolve()}/Archives")
web_files_dir = Path(f"{downloads_dir.resolve()}/Web Files")
executables_dir = Path(f"{downloads_dir.resolve()}/Executables")
temp_files_dir = Path(f"{downloads_dir.resolve()}/Temp Files")
another_dir = Path(f"{downloads_dir.resolve()}/Another Files")

created_dirs = [
  images_dir, documents_dir, audio_dir,
  videos_dir, archives_dir, web_files_dir,
  executables_dir, temp_files_dir, another_dir
]

def recently_modified(
  file_path: Path,
  seconds: float = 5,
) -> bool:

  try:
    modified = file_path.stat().st_mtime
  except FileNotFoundError:
    return False

  return time() - modified < seconds

async def is_file_stable(
  file_path: Path,
  checks: int = 3,
  interval: float = 2,
) -> bool:

  try:
    previous_size = file_path.stat().st_size
  except FileNotFoundError:
    return False

  for x in range(checks):

    await asyncio.sleep(interval)

    try:
      current_size = file_path.stat().st_size
    except FileNotFoundError:
      return False

    if current_size != previous_size:
      return False

    if recently_modified(file_path):
      return False

    previous_size = current_size

  return True

def check_file_type(file_path: Path) -> str:
  for x_category in default_categories:
    if file_path.suffix.lower() in default_categories[x_category]:
      return x_category

  return "Unknown file type!"


async def file_handler():
  while True:
    for x_dir in created_dirs:
      x_dir.mkdir(parents=True, exist_ok=True)

    await asyncio.sleep(3)

    stable_files.clear()
    results = await asyncio.gather(
      *(is_file_stable(file_path) for file_path in downloads_dir.iterdir())
    )

    downloads_dir_files = [f for f in downloads_dir.iterdir() if f.is_file()]
    if not downloads_dir_files:
      continue

    for file_to_copy, stable in zip(downloads_dir_files, results):
      if not stable:
        continue

      file_type = check_file_type(file_to_copy)
      if file_type == "File not found!":
        print(f"File not found: {file_to_copy.name}")
      elif file_type == "Unknown file type!":
        destination = another_dir / file_to_copy.name
        
      else:
        destination = downloads_dir / file_type / file_to_copy.name

      if destination.exists():
        print(f"Already exists: {destination.name}")
        done_files.append(file_to_copy.resolve())
        continue

      try:
        move(file_to_copy, destination)

      except PermissionError:
        print(f"File is currently in use: {file_to_copy.name}")
        continue

      except FileNotFoundError:
        print(f"File disappeared before it could be moved: {file_to_copy.name}")
        continue
      
      done_files.append(file_to_copy.resolve())
      print(f"Added {file_to_copy.name} to {file_type}")


try:
  asyncio.run(file_handler())
except KeyboardInterrupt:
  print("\nProgram stopped.")
finally:
  for x_dir in created_dirs:
    print()
    print(f"{x_dir.name} Files:")
    dir_files = x_dir.iterdir()
    for x_file in dir_files:
      print(x_file)

  print()
  print()
  print("Cleanup completed.")