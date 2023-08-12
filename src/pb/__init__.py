from pb.parser import Content


def fmt_bite(content: Content) -> str:
    """Format a content bite."""
    return info(content)  # TODO


def info(content: Content) -> str:
    return content.info()
