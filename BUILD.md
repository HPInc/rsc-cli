# Build Instructions

This document provides comprehensive instructions for building and packaging the HP Remote System Controller CLI tool.

## Prerequisites

- **Python 3.12 or later**
- **Poetry** for dependency management and building
- **Git** for version control

## Initial Setup

### 1. Install Poetry

If you don't have Poetry installed, install it using pip:

```powershell
pip install poetry poetry-plugin-export
```

### 2. Clone the Repository

```powershell
git clone https://github.com/HPInc/rsc-cli
cd rsc-cli
```

### 3. Install Dependencies

Install all dependencies including development and test dependencies:

```powershell
poetry install
```

## Building the Package

### Standard Build

To build the package (creates both wheel and source distribution):

```powershell
poetry build
```

This will create:

- `dist/*.whl` - Wheel distribution
- `dist/*.tar.gz` - Source distribution

## Version Management

The project version is managed in `pyproject.toml` and can be updated using Poetry's version command.

### Viewing Current Version

```powershell
poetry version
```

### Bumping Version

Poetry provides several version bump strategies:

```powershell
poetry version {major,minor,patch,1.0.1}
```

- `major` - For breaking changes (1.0.0 → 2.0.0)
- `minor` - For new features that maintain backward compatibility (1.0.0 → 1.1.0)
- `patch` - For bug fixes and minor changes (1.0.0 → 1.0.1)
- `1.0.1` - To set a specific version (replace with desired version number)

## Creating Windows Bundle

The project includes a special script for creating a Windows bundle with all dependencies.

### 1. Build the Project

First, ensure the project is built:

```powershell
poetry build
```

### 2. Run Bundle Creation Script

Execute the PowerShell script to create a zip file with install script and dependencies:

```powershell
# From the project root directory
.\createbundle\createbundle.ps1
```

This script will:

- Package the built wheel and all dependencies
- Include an install script (`install.bat`)
- Create a zip file ready for distribution

## Development Workflow

### Running Tests

```powershell
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=hprsctool --cov-report=html
```

### Code Quality Checks

```powershell
# Run pylint
poetry run pylint hprsctool

# Run pylint on specific files
poetry run pylint hprsctool/hprsctool.py
```

### Installing in Development Mode

To install the package in development mode (editable install):

```powershell
poetry install
```

After this, you can run the tool directly:

```powershell
poetry run hprsctool --help
```
