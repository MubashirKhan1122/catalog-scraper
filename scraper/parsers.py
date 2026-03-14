"""
Simple parser to extract product data from pages.
Easy to understand for students.
"""

from bs4 import BeautifulSoup
from .utils import get_page, clean_text, get_price, get_number, join_url


class SimpleParser:
    """
    Simple parser that extracts product information.
    Gets: title, price, description, image, reviews
    """

    def __init__(self, website_url):
        """
        Start the parser.

        Args:
            website_url: The main website URL
        """
        self.website_url = website_url

    def get_product_details(self, product_url, category, subcategory, source_page):
        """
        Extract all details from a product page.

        Args:
            product_url: URL of the product page
            category: Category name
            subcategory: Subcategory name
            source_page: Where we found this product

        Returns:
            Dictionary with all product info
        """
        # Get the product page
        html = get_page(product_url)
        if not html:
            return None

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find each piece of information
        title = self._get_title(soup)
        price = self._get_price(soup)
        description = self._get_description(soup)
        image_url = self._get_image(soup)
        review_count = self._get_reviews(soup)

        # Put everything in a dictionary
        product = {
            'category': category,
            'subcategory': subcategory,
            'title': title,
            'price': price,
            'product_url': product_url,
            'image_url': image_url,
            'description': description,
            'review_count': review_count,
            'details': '',  # Extra details (if any)
            'source_page': source_page
        }

        return product

    def _get_title(self, soup):
        """Get product title."""
        title_tag = soup.find(class_='title')
        if title_tag:
            return clean_text(title_tag.get_text())
        return ""

    def _get_price(self, soup):
        """Get product price."""
        price_tag = soup.find(class_='price')
        if price_tag:
            price_text = price_tag.get_text()
            return get_price(price_text)
        return 0

    def _get_description(self, soup):
        """Get product description."""
        desc_tag = soup.find(class_='description')
        if desc_tag:
            return clean_text(desc_tag.get_text())
        return ""

    def _get_image(self, soup):
        """Get product image URL."""
        img_tag = soup.find('img', class_='img-responsive')
        if img_tag and img_tag.get('src'):
            return join_url(self.website_url, img_tag.get('src'))
        return ""

    def _get_reviews(self, soup):
        """Get number of reviews."""
        review_tag = soup.find(class_='ratings')
        if review_tag:
            review_text = review_tag.get_text()
            return get_number(review_text)
        return 0
