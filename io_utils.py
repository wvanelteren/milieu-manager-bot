from jinja2 import Environment, FileSystemLoader, select_autoescape

def load_system_prompt_from_j2_template(path: str) -> str:
    """Load and render a system prompt from a Jinja2 template file.
    
    Args:
        path: Path to the system prompt template file
        
    Returns:
        str: The rendered system prompt content
        
    Raises:
        Exception: If template loading or rendering fails
    """
    env = Environment(
        loader=FileSystemLoader(path.parent),
        autoescape=select_autoescape()
    )
    template = env.get_template(path.name)
    return template.render()
