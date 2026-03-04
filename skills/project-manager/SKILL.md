---
name: project-manager
description: "Create and manage structured project folders in workspace/projects directory. Use when starting new coding projects, research projects, or any work that requires organized file structure."
homepage: ""
metadata: { "openclaw": { "emoji": "📁", "requires": { "dirs": ["workspace/projects"] } } }
---

# Project Manager Skill

Create structured project folders for organized coding and research work.

## When to Use

✅ **USE this skill when:**

- Starting a new coding project
- Beginning research work that needs organized files
- Creating a new data analysis project
- Setting up documentation or writing projects
- Any work that benefits from structured file organization

## Project Structure

Each project gets a dedicated folder with this structure:

```
workspace/projects/
├── project-name/
│   ├── README.md          # Project overview and documentation
│   ├── src/               # Source code
│   │   ├── main.py        # Main entry point
│   │   ├── utils.py       # Utility functions
│   │   └── ...
│   ├── data/              # Data files (input/output)
│   │   ├── raw/           # Raw data (never modify)
│   │   ├── processed/     # Processed data
│   │   └── results/       # Final results and outputs
│   ├── docs/              # Documentation
│   │   ├── design.md      # Design decisions
│   │   ├── notes.md       # Research notes
│   │   └── references.md  # References and citations
│   ├── tests/             # Test files
│   │   ├── test_main.py
│   │   └── ...
│   ├── config/            # Configuration files
│   │   ├── settings.yaml
│   │   └── ...
│   ├── notebooks/         # Jupyter notebooks
│   │   ├── exploration.ipynb
│   │   └── analysis.ipynb
│   ├── scripts/           # Utility scripts
│   │   ├── setup.sh
│   │   └── deploy.sh
│   └── .gitignore         # Git ignore file
```

## Commands

### Create New Project

```bash
# Create a new project with default structure
./tools/project-manager.sh create my-project

# Create with description
./tools/project-manager.sh create my-project "A data analysis project for weather data"

# Create with specific template
./tools/project-manager.sh create my-project --template python
```

### List Projects

```bash
# List all projects
./tools/project-manager.sh list

# List with details
./tools/project-manager.sh list --details
```

### Open Project

```bash
# Navigate to project directory
./tools/project-manager.sh open my-project

# Open in editor (if configured)
./tools/project-manager.sh edit my-project
```

### Archive Project

```bash
# Archive completed project
./tools/project-manager.sh archive my-project

# Archive with reason
./tools/project-manager.sh archive my-project --reason "Completed analysis"
```

## Templates

Available project templates:

- **python** - Python project with virtualenv setup
- **research** - Research project with LaTeX support
- **web** - Web development project
- **data** - Data science project
- **minimal** - Minimal structure (just README and src)

## Quick Start

1. **Create projects directory** (if not exists):
   ```bash
   mkdir -p ~/.openclaw/workspace/projects
   ```

2. **Create your first project**:
   ```bash
   cd ~/.openclaw/workspace
   ./tools/project-manager.sh create my-first-project "My first organized project"
   ```

3. **Start working**:
   ```bash
   cd projects/my-first-project
   # Add your code to src/
   # Add data to data/
   # Write documentation in docs/
   ```

## Integration with Other Skills

- **Obsidian Tech Notes**: Link project documentation to Obsidian vault
- **Git**: Initialize git repository in project folder
- **Research**: Organize research papers and notes in docs/references.md
- **Data Analysis**: Keep raw data in data/raw/, processed in data/processed/

## Best Practices

1. **One project, one folder** - Keep everything related to a project in its folder
2. **Document early** - Write README.md first, update as you go
3. **Separate concerns** - Keep source code, data, and documentation separate
4. **Version control** - Initialize git repository for each project
5. **Backup regularly** - Important projects should be backed up or pushed to remote

## Notes

- Projects are stored in `workspace/projects/`
- Each project is self-contained
- Use descriptive project names (kebab-case recommended)
- Update README.md as project evolves
- Archive completed projects to keep workspace clean