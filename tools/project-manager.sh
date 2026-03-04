#!/bin/bash
# Project Manager Tool
# Creates and manages structured project folders

set -e

PROJECTS_DIR="$HOME/.openclaw/workspace/projects"
TOOLS_DIR="$HOME/.openclaw/workspace/tools"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ensure projects directory exists
mkdir -p "$PROJECTS_DIR"

# Default templates
declare -A TEMPLATES=(
    ["python"]="python"
    ["research"]="research" 
    ["web"]="web"
    ["data"]="data"
    ["minimal"]="minimal"
)

# Template definitions
create_python_template() {
    local project_dir="$1"
    
    # Create Python project structure
    mkdir -p "$project_dir/src"
    mkdir -p "$project_dir/tests"
    mkdir -p "$project_dir/docs"
    mkdir -p "$project_dir/data/raw"
    mkdir -p "$project_dir/data/processed"
    mkdir -p "$project_dir/data/results"
    mkdir -p "$project_dir/notebooks"
    mkdir -p "$project_dir/scripts"
    mkdir -p "$project_dir/config"
    
    # Create basic Python files
    cat > "$project_dir/src/main.py" << 'EOF'
#!/usr/bin/env python3
"""
Main entry point for the project.
"""

def main():
    """Main function."""
    print("Hello from the project!")

if __name__ == "__main__":
    main()
EOF

    cat > "$project_dir/src/utils.py" << 'EOF'
"""
Utility functions for the project.
"""

def hello_world():
    """Return a greeting."""
    return "Hello, World!"
EOF

    cat > "$project_dir/tests/test_main.py" << 'EOF'
"""
Tests for the main module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import main

def test_main():
    """Test the main function."""
    # This is a simple test
    assert True
EOF

    # Create requirements.txt
    cat > "$project_dir/requirements.txt" << 'EOF'
# Project dependencies
# numpy==1.24.0
# pandas==2.0.0
# matplotlib==3.7.0
EOF

    # Create .gitignore for Python
    cat > "$project_dir/.gitignore" << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data
data/processed/
data/results/

# Notebooks
*.ipynb_checkpoints

# OS
.DS_Store
Thumbs.db
EOF
}

create_research_template() {
    local project_dir="$1"
    
    # Create research project structure
    mkdir -p "$project_dir/paper"
    mkdir -p "$project_dir/experiments"
    mkdir -p "$project_dir/data/raw"
    mkdir -p "$project_dir/data/processed"
    mkdir -p "$project_dir/data/results"
    mkdir -p "$project_dir/analysis"
    mkdir -p "$project_dir/references"
    mkdir -p "$project_dir/figures"
    mkdir -p "$project_dir/code"
    
    # Create LaTeX paper template
    cat > "$project_dir/paper/main.tex" << 'EOF'
\documentclass{article}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}

\title{Project Title}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
Abstract goes here.
\end{abstract}

\section{Introduction}
Introduction text.

\section{Methods}
Methods description.

\section{Results}
Results presentation.

\section{Discussion}
Discussion of results.

\section{Conclusion}
Conclusion.

\bibliographystyle{plain}
\bibliography{references}

\end{document}
EOF

    # Create references file
    cat > "$project_dir/paper/references.bib" << 'EOF'
@article{example2023,
  title={Example Article},
  author={Author, A. and Author, B.},
  journal={Journal of Examples},
  volume={1},
  pages={1--10},
  year={2023}
}
EOF

    # Create experiment log
    cat > "$project_dir/experiments/experiment-log.md" << 'EOF'
# Experiment Log

## 2023-01-01: First Experiment
- Goal: Test hypothesis
- Procedure: Describe steps
- Results: Initial findings
- Notes: Observations and issues
EOF
}

create_web_template() {
    local project_dir="$1"
    
    # Create web project structure
    mkdir -p "$project_dir/src"
    mkdir -p "$project_dir/public"
    mkdir -p "$project_dir/assets"
    mkdir -p "$project_dir/tests"
    mkdir -p "$project_dir/docs"
    
    # Create basic HTML file
    cat > "$project_dir/src/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Title</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Hello, World!</h1>
    <p>Welcome to the project.</p>
    <script src="main.js"></script>
</body>
</html>
EOF

    # Create CSS file
    cat > "$project_dir/src/styles.css" << 'EOF'
/* Main stylesheet */

body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}

h1 {
    color: #333;
}
EOF

    # Create JavaScript file
    cat > "$project_dir/src/main.js" << 'EOF'
// Main JavaScript file

console.log('Project loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready');
});
EOF

    # Create package.json for Node.js projects
    cat > "$project_dir/package.json" << 'EOF'
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Web project",
  "main": "src/main.js",
  "scripts": {
    "start": "node src/main.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "Your Name",
  "license": "MIT"
}
EOF
}

create_data_template() {
    local project_dir="$1"
    
    # Create data science project structure
    mkdir -p "$project_dir/notebooks"
    mkdir -p "$project_dir/src"
    mkdir -p "$project_dir/data/raw"
    mkdir -p "$project_dir/data/processed"
    mkdir -p "$project_dir/data/results"
    mkdir -p "$project_dir/models"
    mkdir -p "$project_dir/reports"
    mkdir -p "$project_dir/figures"
    
    # Create Jupyter notebook
    cat > "$project_dir/notebooks/01-exploration.ipynb" << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data Exploration\n",
    "\n",
    "First exploration of the dataset."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Set style\n",
    "sns.set_style('whitegrid')\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load data\n",
    "# df = pd.read_csv('../data/raw/data.csv')\n",
    "# print(df.head())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

    # Create requirements.txt for data science
    cat > "$project_dir/requirements.txt" << 'EOF'
# Data Science Stack
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.2.0
jupyter>=1.0.0
notebook>=6.5.0
EOF
}

create_minimal_template() {
    local project_dir="$1"
    
    # Create minimal structure
    mkdir -p "$project_dir/src"
    mkdir -p "$project_dir/docs"
    
    # Create basic README
    cat > "$project_dir/README.md" << 'EOF'
# Project Name

Brief description of the project.

## Getting Started

Instructions for setting up and running the project.

## Usage

How to use the project.

## License

Specify license here.
EOF
}

create_default_template() {
    local project_dir="$1"
    
    # Create default structure (similar to minimal but with data folder)
    mkdir -p "$project_dir/src"
    mkdir -p "$project_dir/docs"
    mkdir -p "$project_dir/data"
    mkdir -p "$project_dir/tests"
    
    # Create basic README
    cat > "$project_dir/README.md" << 'EOF'
# Project Name

Brief description of the project.

## Project Structure

- `src/` - Source code
- `docs/` - Documentation
- `data/` - Data files
- `tests/` - Test files

## Getting Started

Instructions for setting up and running the project.

## Usage

How to use the project.

## License

Specify license here.
EOF
}

create_readme() {
    local project_dir="$1"
    local project_name="$2"
    local description="$3"
    local template="$4"
    
    cat > "$project_dir/README.md" << EOF
# $project_name

$description

## Project Details

- **Created**: $(date '+%Y-%m-%d %H:%M:%S')
- **Template**: $template
- **Location**: \`$project_dir\`

## Project Structure

\`\`\`
$(find "$project_dir" -type f | sort | sed 's|'"$project_dir"'/||' | head -20)
\`\`\`

## Getting Started

1. Navigate to the project directory:
   \`\`\`bash
   cd $project_dir
   \`\`\`

2. Review the structure and add your files.

3. Update this README with project-specific information.

## Notes

- Keep source code in \`src/\`
- Store data in \`data/\`
- Write documentation in \`docs/\`
- Add tests in \`tests/\`

## Next Steps

1. Initialize git repository: \`git init\`
2. Add project-specific dependencies
3. Start coding in \`src/\`
4. Update this README as the project evolves
EOF
}

print_help() {
    echo -e "${BLUE}Project Manager Tool${NC}"
    echo "Creates and manages structured project folders in workspace/projects/"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  create <name> [description] [--template <template>]  Create new project"
    echo "  list [--details]                                    List all projects"
    echo "  open <name>                                         Navigate to project"
    echo "  archive <name> [--reason <reason>]                  Archive project"
    echo "  help                                                Show this help"
    echo ""
    echo "Templates:"
    echo "  python    - Python project with virtualenv setup"
    echo "  research  - Research project with LaTeX support"
    echo "  web       - Web development project"
    echo "  data      - Data science project"
    echo "  minimal   - Minimal structure (default)"
    echo ""
    echo "Examples:"
    echo "  $0 create my-project \"A data analysis project\""
    echo "  $0 create my-web-project --template web"
    echo "  $0 list --details"
    echo "  $0 open my-project"
}

create_project() {
    local project_name="$1"
    local description="$2"
    local template="minimal"
    
    # Parse optional template argument
    if [[ "$3" == "--template" && -n "$4" ]]; then
        template="$4"
    fi
    
    # Validate project name
    if [[ -z "$project_name" ]]; then
        echo -e "${RED}Error: Project name is required${NC}"
        print_help
        exit 1
    fi
    
    # Convert to kebab-case if needed
    local clean_name=$(echo "$project_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
    
    local project_dir="$PROJECTS_DIR/$clean_name"
    
    # Check if project already exists
    if [[ -d "$project_dir" ]]; then
        echo -e "${YELLOW}Warning: Project '$clean_name' already exists${NC}"
        echo -n "Do you want to overwrite? (y/N): "
        read -r response
        if [[ "$response" != "y" && "$response" != "Y" ]]; then
            echo "Aborted."
            exit 0
        fi
        rm -rf "$project_dir"
    fi
    
    # Create project directory
    echo -e "${GREEN}Creating project: $clean_name${NC}"
    echo -e "  Template: $template"
    echo -e "  Location: $project_dir"
    
    mkdir -p "$project_dir"
    
    # Create project structure based on template
    case "$template" in
        "python")
            create_python_template "$project_dir"
            ;;
        "research")
            create_research_template "$project_dir"
            ;;
        "web")
            create_web_template "$project_dir"
            ;;
        "data")
            create_data_template "$project_dir"
            ;;
        "minimal")
            create_minimal_template "$project_dir"
            ;;
        *)
            create_default_template "$project_dir"
            ;;
    esac
    
    # Create README
    create_readme "$project_dir" "$clean_name" "$description" "$template"
    
    echo -e "${GREEN}✓ Project created successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cd $project_dir"
    echo "  2. Review the README.md file"
    echo "  3. Start adding your code to src/"
    echo "  4. Initialize git: git init"
}

list_projects() {
    local show_details=false
    
    if [[ "$1" == "--details" ]]; then
        show_details=true
    fi
    
    echo -e "${BLUE}Projects in $PROJECTS_DIR:${NC}"
    echo ""
    
    if [[ ! -d "$PROJECTS_DIR" ]] || [[ -z "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]]; then
        echo "No projects found."
        echo ""
        echo "Create your first project:"
        echo "  $0 create my-first-project \"My first project\""
        return
    fi
    
    for project in "$PROJECTS_DIR"/*; do
        if [[ -d "$project" ]]; then
            local project_name=$(basename "$project")
            local created=$(stat -c %y "$project" 2>/dev/null | cut -d' ' -f1)
            
            echo -e "${GREEN}• $project_name${NC}"
            
            if [[ "$show_details" == true ]]; then
                echo "  Created: $created"
                echo "  Path: $project"
                
                # Count files
                local file_count=$(find "$project" -type f | wc -l)
                local dir_count=$(find "$project" -type d | wc -l)
                echo "  Files: $file_count, Directories: $((dir_count - 1))"
                
                # Show README first line if exists
                if [[ -f "$project/README.md" ]]; then
                    local first_line=$(head -1 "$project/README.md" | sed 's/# //')
                    echo "  Description: $first_line"
                fi
                
                echo ""
            fi
        fi
    done
    
    if [[ "$show_details" != true ]]; then
        echo ""
        echo "For more details: $0 list --details"
    fi
}

open_project() {
    local project_name="$1"
    
    if [[ -z "$project_name" ]]; then
        echo -e "${RED}Error: Project name is required${NC}"
        echo "Usage: $0 open <project-name>"
        exit 1
    fi
    
    local project_dir="$PROJECTS_DIR/$project_name"
    
    if [[ ! -d "$project_dir" ]]; then
        echo -e "${RED}Error: Project '$project_name' not found${NC}"
        echo ""
        echo "Available projects:"
        for project in "$PROJECTS_DIR"/*; do
            if [[ -d "$project" ]]; then
                echo "  • $(basename "$project")"
            fi
        done
        exit 1
    fi
    
    echo -e "${GREEN}Opening project: $project_name${NC}"
    echo "Location: $project_dir"
    echo ""
    echo "You can now:"
    echo "  1. Navigate: cd $project_dir"
    echo "  2. List files: ls -la"
    echo "  3. Edit README: cat README.md"
    
    # If we're in an interactive shell, offer to change directory
    if [[ -t 0 ]]; then
        echo ""
        echo -n "Change to project directory? (y/N): "
        read -r response
        if [[ "$response" == "y" || "$response" == "Y" ]]; then
            cd "$project_dir"
            echo "Changed to: $(pwd)"
        fi
    fi
}

archive_project() {
    local project_name="$1"
    local reason="Archived on $(date '+%Y-%m-%d')"
    
    # Parse optional reason argument
    if [[ "$2" == "--reason" && -n "$3" ]]; then
        reason="$3"
    fi
    
    if [[ -z "$project_name" ]]; then
        echo -e "${RED}Error: Project name is required${NC}"
        echo "Usage: $0 archive <project-name> [--reason \"reason text\"]"
        exit 1
    fi
    
    local project_dir="$PROJECTS_DIR/$project_name"
    local archive_dir="$PROJECTS_DIR/_archived"
    
    if [[ ! -d "$project_dir" ]]; then
        echo -e "${RED}Error: Project '$project_name' not found${NC}"
        exit 1
    fi
    
    mkdir -p "$archive_dir"
    
    # Create archive with timestamp
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local archive_name="${project_name}_${timestamp}"
    local archive_path="$archive_dir/$archive_name"
    
    echo -e "${YELLOW}Archiving project: $project_name${NC}"
    echo "  Reason: $reason"
    echo "  Archive: $archive_path"
    
    # Move project to archive
    mv "$project_dir" "$archive_path"
    
    # Add archive note
    cat > "$archive_path/ARCHIVE.md" << EOF
# Archived Project: $project_name

- **Original Name**: $project_name
- **Archived Date**: $(date '+%Y-%m-%d %H:%M:%S')
- **Reason**: $reason
- **Original Location**: $project_dir

## Contents

This directory contains the archived project files.

## Restoration

To restore this project:
\`\`\`bash
mv "$archive_path" "$project_dir"
\`\`\`
EOF
    
    echo -e "${GREEN}✓ Project archived successfully!${NC}"
    echo "Archived to: $archive_path"
}

# Main command handling
main() {
    local command="$1"
    
    case "$command" in
        "create")
            shift
            create_project "$@"
            ;;
        "list")
            shift
            list_projects "$@"
            ;;
        "open")
            shift
            open_project "$@"
            ;;
        "archive")
            shift
            archive_project "$@"
            ;;
        "help"|"--help"|"-h"|"")
            print_help
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}"
            print_help
            exit 1
            ;;
    esac
}

# Make script executable
if [[ "$0" == "$BASH_SOURCE" ]]; then
    # Check if script is executable, if not make it executable
    if [[ ! -x "$0" ]]; then
        chmod +x "$0"
    fi
    
    main "$@"
fi