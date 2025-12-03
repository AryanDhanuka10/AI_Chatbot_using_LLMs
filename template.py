"""Generate folder structure for the Multi-Domain LLM Assistant project.

Run this script once using: `python template.py`
"""

import os

PROJECT_STRUCTURE = {
    "src": [
        "__init__.py",
        "main.py",
    ],
    "src/models": [
        "__init__.py",
        "llm.py",
    ],
    "src/agents": [
        "__init__.py",
        "education_agent.py",
        "medical_agent.py",
        "legal_agent.py",
        "coding_agent.py",
    ],
    "src/router": [
        "__init__.py",
        "domain_router.py",
    ],
    "tests": [
        "__init__.py",
        "test_llm.py",
        "test_education_agent.py",
        "test_router.py",
    ],
    "config": [
        "__init__.py",
        "settings.py",
    ],
    "data": [],
    "notebooks": [],
}


def create_file(path: str) -> None:
    """Create a Python file containing a valid module-level docstring.

    The generated docstring complies with Ruff docstring rules
    (D400, D415, D205) and provides a placeholder module description.
    """
    module_name = os.path.basename(path).replace(".py", "")

    content = f'''"""Module: {module_name}.

Auto-generated template file.
"""

'''

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_structure() -> None:
    """Generate the full folder + file structure for the project.

    Folders are created recursively, and each file is initialized with
    a valid docstring to ensure linting and pre-commit checks pass.
    """
    print("Generating project structure...\n")

    for folder, files in PROJECT_STRUCTURE.items():
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

        for filename in files:
            file_path = os.path.join(folder, filename)
            create_file(file_path)
            print(f"  - File created: {file_path}")

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    generate_structure()
