"""
Simple exporter to save data to CSV and JSON files.
Easy to understand for students.
"""

import csv
import json


class SimpleExporter:
    """
    Simple exporter that saves products to files.
    Can save as: CSV (Excel) or JSON
    """

    def __init__(self, folder_name="data"):
        """
        Start the exporter.

        Args:
            folder_name: Folder where files will be saved
        """
        self.folder = folder_name

    def save_to_csv(self, products, filename="products.csv"):
        """
        Save products to a CSV file (can open in Excel).

        Args:
            products: List of products
            filename: Name of the CSV file
        """
        if not products:
            print("No products to save")
            return

        # Full file path
        filepath = f"{self.folder}/{filename}"

        # Define column names
        columns = [
            'category',
            'subcategory',
            'title',
            'price',
            'product_url',
            'image_url',
            'description',
            'review_count',
            'details',
            'source_page'
        ]

        # Write to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columns)

            # Write header row
            writer.writeheader()

            # Write each product
            for product in products:
                writer.writerow(product)

        print(f"✓ Saved {len(products)} products to {filepath}")

    def save_to_json(self, products, filename="products.json"):
        """
        Save products to a JSON file (for web/API use).

        Args:
            products: List of products
            filename: Name of the JSON file
        """
        if not products:
            print("No products to save")
            return

        # Full file path
        filepath = f"{self.folder}/{filename}"

        # Write to JSON
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(products, file, indent=2, ensure_ascii=False)

        print(f"✓ Saved {len(products)} products to {filepath}")

    def save_summary_csv(self, products, filename="category_summary.csv"):
        """
        Create a summary report and save to CSV.
        Shows: total products, average price, min/max price per category.

        Args:
            products: List of products
            filename: Name of the summary CSV file
        """
        if not products:
            print("No products to summarize")
            return

        # Group products by subcategory
        groups = {}
        for product in products:
            category = product.get('category', 'Unknown')
            subcategory = product.get('subcategory', 'Unknown')
            key = f"{category} > {subcategory}"

            if key not in groups:
                groups[key] = []
            groups[key].append(product)

        # Calculate statistics for each group
        summary = []
        for group_name, group_products in groups.items():
            # Get all prices
            prices = [p['price'] for p in group_products if p.get('price')]

            # Calculate stats
            total = len(group_products)
            avg_price = sum(prices) / len(prices) if prices else 0
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0

            # Count missing descriptions
            missing_desc = sum(1 for p in group_products if not p.get('description', '').strip())

            summary.append({
                'subcategory': group_name,
                'total_products': total,
                'average_price': round(avg_price, 2),
                'min_price': min_price,
                'max_price': max_price,
                'missing_descriptions': missing_desc,
                'duplicates_removed': 0
            })

        # Save to CSV
        filepath = f"{self.folder}/{filename}"
        columns = ['subcategory', 'total_products', 'average_price',
                   'min_price', 'max_price', 'missing_descriptions', 'duplicates_removed']

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(summary)

        print(f"✓ Saved summary to {filepath}")

    def save_summary_json(self, products, filename="category_summary.json"):
        """
        Create a summary report and save to JSON.

        Args:
            products: List of products
            filename: Name of the summary JSON file
        """
        if not products:
            print("No products to summarize")
            return

        # Group products by subcategory
        groups = {}
        for product in products:
            category = product.get('category', 'Unknown')
            subcategory = product.get('subcategory', 'Unknown')
            key = f"{category} > {subcategory}"

            if key not in groups:
                groups[key] = []
            groups[key].append(product)

        # Calculate statistics for each group
        summary = []
        for group_name, group_products in groups.items():
            # Get all prices
            prices = [p['price'] for p in group_products if p.get('price')]

            # Calculate stats
            total = len(group_products)
            avg_price = sum(prices) / len(prices) if prices else 0
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0

            # Count missing descriptions
            missing_desc = sum(1 for p in group_products if not p.get('description', '').strip())

            summary.append({
                'subcategory': group_name,
                'total_products': total,
                'average_price': round(avg_price, 2),
                'min_price': min_price,
                'max_price': max_price,
                'missing_descriptions': missing_desc,
                'duplicates_removed': 0
            })

        # Save to JSON
        filepath = f"{self.folder}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(summary, file, indent=2, ensure_ascii=False)

        print(f"✓ Saved summary to {filepath}")
