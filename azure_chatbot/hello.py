import azure.functions as func

def main(name: str) -> str:
    return f"Hello {name}!"
