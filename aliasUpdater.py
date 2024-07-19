import os
import re
import argparse

def collect_aliases(directory):
    aliases = {}
    folder_stack = [(directory, "")]

    while folder_stack:
        current_folder, parent_number = folder_stack.pop()
        if not os.path.isdir(current_folder):
            continue

        for folder_name in os.listdir(current_folder):
            folder_path = os.path.join(current_folder, folder_name)
            if os.path.isdir(folder_path):
                match = re.match(r"(\d+)_", folder_name)
                if match:
                    extracted_number = match.group(1)
                    if extracted_number.isdigit():
                        aliases[extracted_number] = folder_path
                        folder_stack.append((folder_path, extracted_number))
                        print(f"Collected alias for folder {extracted_number} at {folder_path}")

    return aliases

def create_aliases(aliases):
    alias_commands = []
    for number, path in aliases.items():
        alias_commands.append(f"alias {number}='cd \"{path}\"'")

    return alias_commands

def main(directory):
    print("Starting alias collection...")
    aliases = collect_aliases(directory)

    print("\nCreating aliases...")
    alias_commands = create_aliases(aliases)

    with open("aliases.sh", "w") as alias_file:
        alias_file.write("\n".join(alias_commands))

    print("\nAliases created:")
    for command in alias_commands:
        print(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate aliases for numbered folders")
    parser.add_argument("directory", help="The directory to scan for numbered folders")
    args = parser.parse_args()
    main(args.directory)
