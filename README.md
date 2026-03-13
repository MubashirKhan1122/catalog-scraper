# E-Commerce Catalog Scraper

A comprehensive web scraping project that extracts product data from an e-commerce website using Python, Beautiful Soup, and the uv package manager.

## Project Overview

This project scrapes product information from [https://webscraper.io/test-sites/e-commerce/static](https://webscraper.io/test-sites/e-commerce/static), navigating through categories, subcategories, paginated listing pages, and individual product detail pages to extract comprehensive product data.

### Target Website

- **URL**: https://webscraper.io/test-sites/e-commerce/static
- **Structure**: Categories → Subcategories → Paginated Listings → Product Details

## Features

- ✅ **Category & Subcategory Discovery**: Automatically discovers all categories and subcategories
- ✅ **Pagination Handling**: Crawls all pages within each subcategory
- ✅ **Product Detail Extraction**: Visits each product page for complete information
- ✅ **URL Resolution**: Properly handles relative and absolute URLs
- ✅ **Deduplication**: Removes duplicate products based on normalized URLs
- ✅ **Data Cleaning**: Normalizes prices, handles missing fields, cleans text
- ✅ **Error Handling**: Graceful error handling for failed requests and missing data
- ✅ **CSV Export**: Generates products.csv and category_summary.csv

## Project Structure

```
.
├── README.md                 # This file
├── pyproject.toml           # uv project configuration and dependencies
├── uv.lock                  # uv lock file for reproducible builds
├── main.py                  # Main entry point
├── data/                    # Output directory for CSV files
│   ├── products.csv         # Complete product dataset
│   └── category_summary.csv # Category statistics summary
├── scraper/                 # Scraper package
│   ├── __init__.py          # Package initializer
│   ├── crawler.py           # Category/subcategory/pagination crawler
│   ├── parsers.py           # Product detail page parser
│   ├── exporters.py         # CSV export functionality
│   └── utils.py             # Utility functions (URL handling, text cleaning, etc.)
└── tests/                   # Test directory
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Internet connection

### Installation

1. **Install uv package manager** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone or navigate to the project directory**:
   ```bash
   cd "AQSA ASSIGNMENT"
   ```

3. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

   This will:
   - Create a virtual environment
   - Install all required dependencies (requests, beautifulsoup4)
   - Set up the project for execution

## Running the Scraper

Execute the scraper using uv:

```bash
uv run python main.py
```

The scraper will:
1. Discover all categories from the main page
2. For each category, discover subcategories
3. For each subcategory, crawl all paginated listing pages
4. Collect all product URLs
5. Visit each product detail page and extract data
6. Deduplicate products
7. Export to CSV files in the `data/` directory

## Output Files

### products.csv

Contains detailed product information with the following fields:

| Field           | Description                                    |
|-----------------|------------------------------------------------|
| category        | Product category (e.g., "Computers")          |
| subcategory     | Product subcategory (e.g., "Laptops")         |
| title           | Product name/title                             |
| price           | Numeric price value                            |
| product_url     | Full URL to product detail page               |
| image_url       | Full URL to product image                      |
| description     | Product description text                       |
| review_count    | Number of reviews                              |
| details         | Additional product specifications              |
| source_page     | URL of the listing page where product was found|

### category_summary.csv

Contains aggregated statistics per subcategory:

| Field                  | Description                                    |
|------------------------|------------------------------------------------|
| subcategory            | Category > Subcategory name                    |
| total_products         | Total number of products                       |
| average_price          | Average price across products                  |
| min_price              | Minimum price                                  |
| max_price              | Maximum price                                  |
| missing_descriptions   | Count of products without descriptions         |
| duplicates_removed     | Total duplicates removed (global statistic)    |

## Git Branching Workflow

This project follows a structured Git branching strategy as required:

### Branch Structure

- **main**: Production-ready code
- **dev**: Development integration branch
- **feature/** branches: New features
  - `feature/catalog-navigation`: Category and subcategory discovery
  - `feature/product-details`: Product detail page parsing
- **fix/** branches: Bug fixes and improvements
  - `fix/url-resolution`: URL resolution enhancements
  - `fix/deduplication`: Product deduplication logic

### Workflow Followed

1. Created `main` branch with initial project setup
2. Created `dev` branch from `main`
3. Created feature branches from `dev`:
   - Implemented catalog navigation in `feature/catalog-navigation`
   - Implemented product parsing in `feature/product-details`
4. Merged feature branches into `dev`
5. Created fix branches from `dev`:
   - Enhanced URL resolution in `fix/url-resolution`
   - Added deduplication in `fix/deduplication`
6. Merged fix branches into `dev`
7. Tested complete scraper on `dev`
8. Merged `dev` into `main` for final release

### Commit History

The project maintains meaningful commit messages describing each change:
- Initial project setup
- Feature implementations
- Bug fixes and improvements
- Integration merges

## Technologies Used

### Required Tools

- **Git/GitHub**: Version control and collaboration
- **Python 3.14**: Programming language
- **uv**: Modern Python package manager and project manager
- **requests**: HTTP library for making web requests
- **BeautifulSoup4**: HTML parsing and web scraping

### Not Used (Per Requirements)

- ❌ Selenium
- ❌ Playwright
- ❌ Scrapy

## Key Implementation Details

### URL Resolution

The scraper properly handles:
- Relative URLs (e.g., `../path`, `./path`)
- Absolute paths (e.g., `/test-sites/...`)
- Full URLs
- Query parameters and fragments
- URL normalization for deduplication

### Pagination

- Discovers all pagination links on listing pages
- Visits each page sequentially
- Tracks visited URLs to avoid duplicates
- Handles edge cases (first page, last page, etc.)

### Error Handling

- Retry logic with exponential backoff for failed requests
- Graceful handling of missing HTML elements
- Safe parsing with default values
- Exception handling throughout the workflow

### Data Cleaning

- Price parsing from various formats ($X.XX, $X,XXX.XX)
- Text normalization (whitespace removal, unicode handling)
- Missing value handling
- Empty string cleaning

## Assumptions

1. **Website Structure**: Assumes the target website maintains its current HTML structure with consistent CSS classes
2. **Static Content**: Designed for static HTML pages (no JavaScript rendering required)
3. **Rate Limiting**: No explicit rate limiting implemented (suitable for test site)
4. **Network**: Assumes stable internet connection
5. **Categories**: Assumes categories are listed in the main navigation
6. **Product URLs**: Assumes each product has a unique URL

## Limitations

1. **JavaScript**: Cannot handle dynamically loaded content (JavaScript-rendered pages)
2. **Authentication**: No support for login/authentication required pages
3. **CAPTCHAs**: No CAPTCHA solving capability
4. **Rate Limits**: No built-in rate limiting or throttling
5. **Large Scale**: Performance may degrade with very large datasets (10,000+ products)
6. **Images**: Downloads image URLs but not the actual images themselves

## Testing

To test individual components:

```bash
# Test category discovery
uv run python -c "from scraper.crawler import CatalogCrawler; c = CatalogCrawler('https://webscraper.io/test-sites/e-commerce/static'); print(c.discover_categories())"

# Test product parsing
uv run python -c "from scraper.parsers import ProductParser; p = ProductParser('https://webscraper.io/test-sites/e-commerce/static'); print(p.parse_product_page('https://webscraper.io/test-sites/e-commerce/static/product/1', 'Test', 'Test', 'test'))"
```

## Troubleshooting

### Common Issues

**Issue**: `command not found: uv`
- **Solution**: Install uv using the installation command in Setup Instructions

**Issue**: Import errors
- **Solution**: Run `uv sync` to ensure all dependencies are installed

**Issue**: No products found
- **Solution**: Check internet connection and verify target website is accessible

**Issue**: Permission errors on data/ directory
- **Solution**: Ensure write permissions for the project directory

## Future Enhancements

Potential improvements for future versions:
- Add concurrent scraping with asyncio
- Implement request rate limiting
- Add proxy support for larger scale scraping
- Store data in database instead of CSV
- Add progress bar for visual feedback
- Implement incremental scraping (only new products)
- Add data validation and quality checks
- Export to additional formats (JSON, Excel, SQL)

## License

This project is created for educational purposes as part of a university assignment.

## Author

**University of Central Punjab**
Faculty of IT & CS
Department of Applied Computing & Technologies
Course: Tools & Technologies for Data Science

---

**Note**: This scraper is designed specifically for the webscraper.io test site. Always respect robots.txt and terms of service when scraping websites.
