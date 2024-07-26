from globals import LOGGER

def log_interaction(log_file: str, prompt: str, response: str):
    """Log the interaction between the system and the LLM."""
    if not LOGGER:
        return
    if not log_file.parent.exists():
        log_file.parent.mkdir(parents=True)
    with open(log_file, 'a') as f:
        f.write(f"Prompt: {prompt}\n\n")
        f.write(f"Response: {response}\n\n")
        f.write("-" * 80 + "\n\n")