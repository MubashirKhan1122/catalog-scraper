"""
Simple utility functions for web scraping.
Easy to understand for university students.
"""

import requests
from urllib.parse import urljoin


def get_page(url):
    """
    Get a webpage (simple version).

    Args:
        url: The website address

    Returns:
        The webpage content, or None if error
    """
    try:
        response = requests.get(url)
        return response.text
    except:
        print(f"Error getting page: {url}")
        return None


def join_url(base, path):
    """
    Join two URLs together.
    Example: join_url('https://example.com', '/page')
             -> 'https://example.com/page'

    Args:
        base: The main website URL
        path: The page path

    Returns:
        Complete URL
    """
    return urljoin(base, path)


def clean_text(text):
    """
    Clean up text (remove extra spaces).

    Args:
        text: The text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra spaces and newlines
    text = text.strip()
    text = " ".join(text.split())
    return text


def get_price(price_text):
    """
    Convert price text to number.
    Example: "$123.45" -> 123.45

    Args:
        price_text: Price as text (like "$123.45")

    Returns:
        Price as number (like 123.45)
    """
    if not price_text:
        return 0

    # Remove $ and commas
    price_text = price_text.replace('$', '').replace(',', '').strip()

    try:
        return float(price_text)
    except:
        return 0


def get_number(text):
    """
    Get a number from text.
    Example: "12 reviews" -> 12

    Args:
        text: Text containing a number

    Returns:
        The number found
    """
    if not text:
        return 0

    # Find all digits
    numbers = ''.join(c for c in text if c.isdigit())

    if numbers:
        return int(numbers)
    return 0


def remove_duplicates(products):
    """
    Remove duplicate products from list.

    Args:
        products: List of products

    Returns:
        List without duplicates, count of duplicates removed
    """
    seen_urls = set()
    unique = []
    duplicates = 0

    for product in products:
        url = product.get('product_url', '')

        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(product)
        else:
            duplicates += 1

    return unique, duplicates
