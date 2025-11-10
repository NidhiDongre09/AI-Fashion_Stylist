from urllib.parse import quote

def generate_shopping_links(item_name: str):
    """Generate store search links for an outfit item."""
    encoded = quote(item_name)

    links = {
        "Myntra": f"https://www.myntra.com/{encoded}",
        "Ajio": f"https://www.ajio.com/search/?text={encoded}",
        "Amazon": f"https://www.amazon.in/s?k={encoded}"
    }
    return links
