import os
import openai
from tqdm import tqdm
from git import Repo

# Set up OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Define file extensions to check
VALID_EXTENSIONS = {".py", ".java", ".js", ".cpp", ".c", ".cs", ".ts"}

# Function to check if a file is valid for refactoring
def is_valid_file(file_path):
    return os.path.isfile(file_path) and file_path.endswith(tuple(VALID_EXTENSIONS))

# Function to read file content
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Function to refactor code using GPT-4o
def refactor_code(code, file_path):
    prompt = f"""
    Refactor the following {file_path.split('.')[-1]} code while maintaining its functionality and improving design quality:
    
    ```{file_path.split('.')[-1]}
    {code}
    ```
    
    Return only the improved code.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error refactoring {file_path}: {e}")
        return code  # Return original code if refactoring fails

# Function to write refactored code back to file
def write_file(file_path, refactored_code):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(refactored_code)

# Function to scan all files and refactor them
def process_repository(repo_path):
    files_modified = []
    
    for root, _, files in os.walk(repo_path):
        for file in tqdm(files, desc="Processing files"):
            file_path = os.path.join(root, file)

            if is_valid_file(file_path):
                print(f"Refactoring: {file_path}")
                
                original_code = read_file(file_path)
                refactored_code = refactor_code(original_code, file_path)
                
                if refactored_code and refactored_code != original_code:
                    write_file(file_path, refactored_code)
                    files_modified.append(file_path)

    return files_modified

# Function to commit and push changes to GitHub
def commit_and_push_changes(repo_path, modified_files):
    if not modified_files:
        print("No files were modified. Skipping commit.")
        return
    
    repo = Repo(repo_path)
    repo.git.add("--all")
    repo.index.commit("Automated refactoring of design smells")
    repo.git.push("origin", "refactored-branch")

    print("Changes pushed to GitHub.")

# Main execution
if __name__ == "__main__":
    repo_path = os.getcwd()  # Assume script is run in repo root
    modified_files = process_repository(repo_path)
    commit_and_push_changes(repo_path, modified_files)
