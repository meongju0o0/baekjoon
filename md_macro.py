import os
import re

if __name__ == '__main__':
    filename = "README.md"
    repo_dir = "./"

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_content = file.readlines()
    else:
        existing_content = []

    existing_paths = set()
    pattern = re.compile(r"\[(.*?)\]\((.*?)\)")

    for line in existing_content:
        match = pattern.search(line)
        if match:
            existing_paths.add(match.group(2))

    new_entries = []
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".cpp") or file.endswith(".py"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, repo_dir)
                github_url = f"https://github.com/meongju0o0/baekjoon/blob/master/{relative_path.replace(os.sep, '/')}"
                if github_url not in existing_paths:
                    problem_numbers = re.findall(r'\d+', file)
                    if problem_numbers:
                        problem_number = problem_numbers[0]
                        new_entries.append((problem_number, github_url))

    new_entries.sort(key=lambda x: int(x[0]))

    with open(filename, 'w', encoding='utf-8') as file:
        for line in existing_content:
            file.write(line)
        if new_entries:
            for problem_number, url in new_entries:
                file.write(f"- [no_{problem_number}]({url})\n")
