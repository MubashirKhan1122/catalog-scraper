"""Parsers for extracting data from product pages."""

from typing import Dict, Optional
from bs4 import BeautifulSoup
from .utils import safe_request, clean_text, parse_price, parse_rating, join_url


class ProductParser:
    """Parser for extracting product details from product pages."""

    def __init__(self, base_url: str):
        """
        Initialize the parser.

        Args:
            base_url: The base URL of the website
        """
        self.base_url = base_url

    def parse_product_page(self, product_url: str, category: str, subcategory: str, source_page: str) -> Optional[Dict]:
        """
        Parse a product detail page and extract all required information.

        Args:
            product_url: URL of the product page
            category: Category name
            subcategory: Subcategory name
            source_page: URL of the source listing page

        Returns:
            Dictionary containing product details or None if parsing fails
        """
        response = safe_request(product_url)

        if not response:
            print(f"Failed to fetch product page: {product_url}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            # Extract product title
            title_elem = soup.select_one('.title, h1.product-title, .product-name')
            title = clean_text(title_elem.get_text()) if title_elem else ""

            # Extract price
            price_elem = soup.select_one('.price, .product-price, .pull-right.price')
            price_str = clean_text(price_elem.get_text()) if price_elem else None
            price = parse_price(price_str)

            # Extract description
            description_elem = soup.select_one('.description, .product-description')
            description = clean_text(description_elem.get_text()) if description_elem else ""

            # Extract image URL
            image_elem = soup.select_one('.img-responsive, .product-image img, img.img-responsive')
            image_url = ""
            if image_elem:
                img_src = image_elem.get('src', '')
                if img_src:
                    image_url = join_url(self.base_url, img_src)

            # Extract review count or rating
            review_elem = soup.select_one('.ratings, .review-count, [data-rating]')
            review_count = 0
            if review_elem:
                review_text = clean_text(review_elem.get_text())
                review_count = parse_rating(review_text) or 0

            # Extract additional details/specs
            details = {}
            detail_elems = soup.select('.product-details li, .specifications li')
            for detail in detail_elems:
                detail_text = clean_text(detail.get_text())
                if detail_text:
                    details[detail_text] = True

            # Combine details into a single string
            details_str = "; ".join(details.keys()) if details else ""

            product_data = {
                'category': category,
                'subcategory': subcategory,
                'title': title,
                'price': price,
                'product_url': product_url,
                'image_url': image_url,
                'description': description,
                'review_count': review_count,
                'details': details_str,
                'source_page': source_page
            }

            return product_data

        except Exception as e:
            print(f"Error parsing product {product_url}: {e}")
            return None

    def parse_listing_page_products(self, page_url: str, category: str, subcategory: str) -> list:
        """
        Parse products from a listing page (lightweight extraction).

        Args:
            page_url: URL of the listing page
            category: Category name
            subcategory: Subcategory name

        Returns:
            List of product dictionaries with basic info
        """
        response = safe_request(page_url)

        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        # Find all product cards
        product_cards = soup.select('.thumbnail')

        for card in product_cards:
            try:
                # Extract title
                title_elem = card.select_one('a.title')
                title = clean_text(title_elem.get('title', '')) if title_elem else ""

                # Extract price
                price_elem = card.select_one('.price, .pull-right.price')
                price_str = clean_text(price_elem.get_text()) if price_elem else None
                price = parse_price(price_str)

                # Extract description preview
                desc_elem = card.select_one('.description')
                description = clean_text(desc_elem.get_text()) if desc_elem else ""

                # Extract product URL
                product_url = ""
                if title_elem:
                    href = title_elem.get('href', '')
                    if href:
                        product_url = join_url(self.base_url, href)

                products.append({
                    'category': category,
                    'subcategory': subcategory,
                    'title': title,
                    'price': price,
                    'product_url': product_url,
                    'description': description,
                    'source_page': page_url
                })

            except Exception as e:
                print(f"Error parsing product card: {e}")
                continue

        return products
