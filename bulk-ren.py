import argparse
from pathlib import Path
from rich import print as rprint

parser = argparse.ArgumentParser(
  prog="bulk-rename",
  description=(
    "Rename part or all of filenames in one command. "
    "By default, files in the current directory are used."
  ),
  epilog=(
    "Be careful when using this tool so you don't "
    "rename files incorrectly."
  ),
)

parser.add_argument(
  "input_name",
  help="Filename or part of the filename you want to change",
)

parser.add_argument(
  "output_name",
  help="Replacement text",
)

parser.add_argument(
  "-sf",
  "--showfirst",
  action="store_true",
  help="Preview the results without renaming anything",
)

parser.add_argument(
  "-f",
  "--onefile",
  help="Rename only one specific file",
)

parser.add_argument(
  "-e",
  "--extension",
  help="Only rename files with this extension, e.g. .jpg",
)


def get_files(
  directory: Path,
  input_name: str,
  onefile: str | None,
  extension: str | None,
) -> list[Path]:
  files = [
    file
    for file in directory.iterdir()
    if file.is_file()
  ]

  if onefile:
    files = [
      file
      for file in files
      if file.name == onefile
    ]

  if extension:
    if not extension.startswith("."):
      extension = f".{extension}"

    files = [
      file
      for file in files
      if file.suffix.lower() == extension.lower()
    ]

  files = [
    file
    for file in files
    if input_name in file.name
  ]

  return files


def get_output_name(
  file: Path,
  input_name: str,
  output_name: str,
) -> str:
  return file.name.replace(
    input_name,
    output_name,
  )


def preview(
  files: list[Path],
  input_name: str,
  output_name: str,
):
  for file in files:
    new_name = get_output_name(
      file,
      input_name,
      output_name,
    )

    rprint(
      f"[yellow]{file.name}[/yellow]"
      f"[cyan] --> [/cyan]"
      f"[purple]{new_name}[/purple]"
    )


def rename_files(
  files: list[Path],
  input_name: str,
  output_name: str,
):
  for file in files:
    new_name = get_output_name(
      file,
      input_name,
      output_name,
    )

    destination = file.with_name(new_name)

    try:
      file.rename(destination)
      rprint(
        f"[green]Renamed "
        f"[yellow]{file.name}[/yellow]"
        f" --> "
        f"[purple]{new_name}[/purple]"
        f"[/green]"
      )

    except OSError as err:
      rprint(
        f"[bold red]Couldn't rename:[/bold red] "
        f"[purple]{file.name}[/purple]"
      )
      rprint(
        f"[bold red]Error: {err}[/bold red]"
      )


def main():
  args = parser.parse_args()

  directory = Path.cwd()

  rprint()
  rprint(
    "[bold red]######[/bold red]"
    "[bold cyan] bulk-rename made by [/bold cyan]"
    "[bold magenta]T3CHN0_17[/bold magenta]"
    "[bold red] ######[/bold red]"
  )
  rprint()

  files = get_files(
    directory,
    args.input_name,
    args.onefile,
    args.extension,
  )

  if not files:
    rprint(
      "[bold yellow]"
      "No matching files found."
      "[/bold yellow]"
    )
    return

  if args.showfirst:
    preview(
      files,
      args.input_name,
      args.output_name,
    )
    return

  rename_files(
    files,
    args.input_name,
    args.output_name,
  )

if __name__ == "__main__":
  main()