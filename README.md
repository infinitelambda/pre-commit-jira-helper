# pre-commit Jira Helper

A [pre-commit](https://pre-commit.com/) hook that automatically prepends Jira issue numbers to your commit messages. Because who doesn't love a little automation magic sprinkled on their Git workflow? ✨

- [pre-commit Jira Helper](#pre-commit-jira-helper)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Basic Examples](#basic-examples)
  - [Configuration](#configuration)
  - [Developer Guide](#developer-guide)
    - [Modular Architecture](#modular-architecture)
      - [Step 1: Create Your Hook](#step-1-create-your-hook)
      - [Step 2: Create CLI Wrapper](#step-2-create-cli-wrapper)
      - [Step 3: Register in pyproject.toml](#step-3-register-in-pyprojecttoml)
      - [Step 4: Add to .pre-commit-hooks.yaml](#step-4-add-to-pre-commit-hooksyaml)
  - [Contributing](#contributing)
  - [License](#license)
  - [About Infinite Lambda](#about-infinite-lambda)

## Features

- **Multiple Issue Support**: Extracts ALL Jira issues from branch names by default
- **Intelligent Deduplication**: Skips issues already present in commit messages
- **Flexible Patterns**: Customizable regex patterns for different Jira formats

## Installation

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/infinitelambda/pre-commit-jira-helper
    rev: v0.1.0  # Use the latest version
    hooks:
      - id: prepend-jira-issue
        stages: [commit-msg]
```

Then install the hook:

```bash
pre-commit install --hook-type commit-msg
```

## Usage

### Basic Examples

**Single Issue:**
```bash
# Branch: feature/ABC-123-add-auth
git commit -m "Add user authentication"
# Actual commit message: 
"ABC-123: Add user authentication"
```

**Multiple Issues:**
```bash
# Branch: feature/ABC-123-DEF-456-new-feature  
git commit -m "Implement new feature"
# Actual commit message: 
"ABC-123, DEF-456: Implement new feature"
```

**With Prefix Filtering:**
```bash
# Branch: feature/ABC-123-XYZ-999-DEF-456-test
# With --prefixes ABC,DEF
git commit -m "Add tests"
# Actual commit message: 
"ABC-123, DEF-456: Add tests" # (XYZ-999 filtered out)
```

## Configuration

Add this to your `.pre-commit-config.yaml`:

```yaml
fail_fast: true
repos:
  - repo: https://github.com/infinitelambda/pre-commit-jira-helper
    rev: v0.1.0  # Use the latest version
    hooks:
      - id: prepend-jira-issue
        stages: [commit-msg]
        # Uncomment and customize these args as needed:
        
        # Basic usage - extracts ALL Jira issues matching the pattern:
        # On branch 'feature/ABC-123-DEF-456-new-feature' -> 'ABC-123, DEF-456: commit message'
        # (no args needed for default behavior)
        
        # Restrict to specific Jira project prefixes only:
        # On branch 'feature/ABC-123-XYZ-999-DEF-456-test' -> 'ABC-123, DEF-456: commit message' 
        args:
          - "--prefixes=ABC,DEF"
        
        # Custom pattern and separator:
        args:
          - "--pattern=[A-Z]{3,}-\\d+"
          - "--separator= - "
        
        # Combine all options:
        args:
          - "--prefixes=PROJ,TASK"
          - "--pattern=[A-Z]{3,}-\\d+"
          - "--separator= | "

      # !CAUTION: This is only for example purposes
      - id: example-prefix-hook
        stages: [commit-msg]
        args: ["--prefix", "[COMMIT]"]
```

See `.pre-commit-config.example.yaml` for more configuration examples.

## Developer Guide

### Modular Architecture

The codebase is organized for easy extensibility. Want to add your own hook? It's as simple as extending our base classes!

#### Step 1: Create Your Hook

```python
# pre_commit_jira_helper/hooks/my_hook.py
from pre_commit_jira_helper.base import CommitMessageHook
from pre_commit_jira_helper.logger import get_logger

logger = get_logger("hooks.my_hook")

class MyCustomHook(CommitMessageHook):
    def should_run(self, commit_msg_filepath):
        # Your logic here
        return True
    
    def process(self, commit_msg_filepath):
        # Your processing logic
        return True
```

#### Step 2: Create CLI Wrapper

```python
# pre_commit_jira_helper/cli/my_hook.py
from pre_commit_jira_helper.cli.base import create_parser
from pre_commit_jira_helper.hooks.my_hook import MyCustomHook

def main(argv=None):
    parser = create_parser(
        prog="my-custom-hook",
        description="Description of my hook",
        epilog="Examples and notes here"
    )
    # Add any custom arguments here
    args = parser.parse_args(argv)
    
    hook = MyCustomHook(debug=args.debug)
    return hook.run(commit_msg_filepath=args.commit_msg_filepath)
```

#### Step 3: Register in pyproject.toml

```toml
[project.scripts]
my-custom-hook = "pre_commit_jira_helper.cli.my_hook:main"
```

#### Step 4: Add to .pre-commit-hooks.yaml

```yaml
- id: my-custom-hook
  name: My Custom Hook
  entry: my-custom-hook
  language: python
  description: Description of what your hook does
  stages: [commit-msg]
```

That's it! Your hook is ready to use. We've included an example hook (`example-prefix-hook`) that demonstrates this pattern.

## Contributing

Contributions are welcome! Feel free to:

- Report bugs or request features via [Issues](https://github.com/infinitelambda/pre-commit-jira-helper/issues)
- Submit pull requests with improvements
- Share your creative branch naming conventions (we've seen some wild ones!)

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

---

## About Infinite Lambda

Infinite Lambda is a cloud and data consultancy. We build strategies, help organisations implement them and pass on the expertise to look after the infrastructure.

We are an Elite Snowflake Partner, a Platinum dbt Partner and two-times Fivetran Innovation Partner of the Year for EMEA.

Naturally, we love exploring innovative solutions and sharing knowledge, so go ahead and:

🔧 Take a look around our [Git](https://github.com/infinitelambda)  
✏️ Browse our [tech blog](https://infinitelambda.com/category/tech-blog/)

We are also chatty, so:  
#️⃣ Follow us on [LinkedIn](https://www.linkedin.com/company/infinite-lambda/)  
👋🏼 Or just [get in touch](https://infinitelambda.com/contacts/)

[<img src="https://raw.githubusercontent.com/infinitelambda/cdn/1.0.0/general/images/GitHub-About-Section-1080x1080.png" alt="About IL" width="500">](https://infinitelambda.com/)