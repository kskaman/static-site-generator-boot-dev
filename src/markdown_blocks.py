def markdown_to_blocks(markdown):
    """
    Convert a markdown string into a list of block elements.

    Args:
        markdown (str): The markdown content to be converted.

    Returns:
        list: A list of block elements representing the markdown content.
    """
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    
    return blocks
