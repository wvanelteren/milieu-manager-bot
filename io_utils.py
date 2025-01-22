from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def load_system_prompt_from_j2_template(path: str) -> str:
    """Load and render a system prompt from a Jinja2 template file.
    
    Args:
        path: Path to the system prompt template file
        
    Returns:
        str: The rendered system prompt content
        
    Raises:
        Exception: If template loading or rendering fails
    """
    path = Path(path)
    env = Environment(
        loader=FileSystemLoader(path.parent),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(path.name)
    return template.render()
