"""
Simple web crawler to find categories and products.
Easy to understand for students.
"""

from bs4 import BeautifulSoup
from .utils import get_page, join_url, clean_text


class SimpleCrawler:
    """
    A simple crawler that navigates the website.
    Finds: categories -> subcategories -> products
    """

    def __init__(self, website_url):
        """
        Start the crawler.

        Args:
            website_url: The main website address
        """
        self.website_url = website_url
        self.visited = []  # Keep track of visited URLs

    def find_categories(self):
        """
        Step 1: Find all categories on the main page.

        Returns:
            List of categories (each is a dict with 'name' and 'url')
        """
        print("Finding categories...")

        # Get the main page
        html = get_page(self.website_url)
        if not html:
            return []

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find all category links
        category_links = soup.find_all('a', class_='category-link')

        categories = []
        for link in category_links:
            name = clean_text(link.get_text())
            url = join_url(self.website_url, link.get('href', ''))

            if name and url:
                categories.append({'name': name, 'url': url})
                print(f"  Found: {name}")

        return categories

    def find_subcategories(self, category_url):
        """
        Step 2: Find subcategories within a category.

        Args:
            category_url: The category page URL

        Returns:
            List of subcategories
        """
        print("  Finding subcategories...")

        # Get the category page
        html = get_page(category_url)
        if not html:
            return []

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find subcategory links
        subcat_links = soup.find_all('a', class_='subcategory-link')

        subcategories = []
        for link in subcat_links:
            name = clean_text(link.get_text())
            url = join_url(self.website_url, link.get('href', ''))

            if name and url:
                subcategories.append({'name': name, 'url': url})
                print(f"    Found: {name}")

        return subcategories

    def find_products_on_page(self, page_url, category, subcategory):
        """
        Step 3: Find all products on a page.

        Args:
            page_url: The page URL
            category: Category name
            subcategory: Subcategory name

        Returns:
            List of product URLs
        """
        # Get the page
        html = get_page(page_url)
        if not html:
            return []

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find product cards
        product_cards = soup.find_all(class_='thumbnail')

        products = []
        for card in product_cards:
            # Find the title link
            title_link = card.find('a', class_='title')

            if title_link:
                title = clean_text(title_link.get('title', ''))
                url = join_url(self.website_url, title_link.get('href', ''))

                # Check if we already visited this product
                if url and url not in self.visited:
                    products.append({
                        'title': title,
                        'url': url,
                        'category': category,
                        'subcategory': subcategory,
                        'source_page': page_url
                    })
                    self.visited.append(url)

        return products

    def find_page_numbers(self, page_url):
        """
        Step 4: Find pagination links (page 2, 3, 4, etc.)

        Args:
            page_url: The current page URL

        Returns:
            List of page URLs
        """
        # Get the page
        html = get_page(page_url)
        if not html:
            return []

        # Parse HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find pagination links
        pagination = soup.find_all(class_='pagination')
        page_urls = []

        for pag in pagination:
            links = pag.find_all('a')
            for link in links:
                href = link.get('href', '')
                if href:
                    url = join_url(self.website_url, href)
                    if url not in page_urls:
                        page_urls.append(url)

        return page_urls

    def get_all_products_in_category(self, category_name, category_url):
        """
        Get ALL products in a category (including all pages and subcategories).

        Args:
            category_name: Name of the category
            category_url: URL of the category

        Returns:
            List of all products
        """
        print(f"\nGetting products from: {category_name}")
        all_products = []

        # Find subcategories
        subcategories = self.find_subcategories(category_url)

        # If no subcategories, treat as direct listing
        if not subcategories:
            subcategories = [{'name': category_name, 'url': category_url}]

        # For each subcategory
        for subcat in subcategories:
            subcat_name = subcat['name']
            subcat_url = subcat['url']

            print(f"  Checking: {subcat_name}")

            # Get products from first page
            products = self.find_products_on_page(subcat_url, category_name, subcat_name)
            all_products.extend(products)
            print(f"    Found {len(products)} products on first page")

            # Find other pages (pagination)
            page_urls = self.find_page_numbers(subcat_url)

            # Visit other pages
            for page_url in page_urls:
                if page_url != subcat_url:  # Don't repeat first page
                    more_products = self.find_products_on_page(page_url, category_name, subcat_name)
                    all_products.extend(more_products)
                    if more_products:
                        print(f"    Found {len(more_products)} more products")

        print(f"  Total in {category_name}: {len(all_products)} products")
        return all_products
