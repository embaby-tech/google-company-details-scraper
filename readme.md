# GoogleScraper

GoogleScraper is a Python-based library designed to fetch data from Google Search. It uses web scraping techniques to extract search results and detailed business information, including social media profiles and LinkedIn pages. It is an effective tool for conducting market research, gathering company insights, and creating business intelligence.

## Features

- **Search Queries**: Extract search result links and titles from Google Search.
- **Business Information**: Retrieve detailed business information such as title, description, founders, headquarters, employees count, and social media links.
- **LinkedIn Integration**: Search for and extract LinkedIn company pages.
- **Proxy Support**: Uses SmartProxy for secure and anonymous requests.

## Prerequisites

- Python 3.8 or higher
- A SmartProxy account with username and password
- Environment variables for SmartProxy credentials

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/googlescraper.git
   cd googlescraper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the project root.
   - Add your SmartProxy credentials:
     ```env
     SMARTPROXY_USERNAME=your_username
     SMARTPROXY_PASSWORD=your_password
     ```

## Usage

### Initialization

Create an instance of `GoogleScraper`:
```python
from google_scraper import GoogleScraper

google = GoogleScraper()
```

### Perform a Search

Use the `search` method to perform a Google search:
```python
data = google.search("Strabag SE", linkedin=True)
print(data)
```

### Extracted Data

The `search` method returns:
- `query`: The search query string.
- `results`: A list of search result links and titles.
- `business_info`: A dictionary of extracted business details, such as:
  - `title`, `subtitle`, `description`
  - `founders`, `employees count`, `CEO`
  - `LinkedIn`, `Wikipedia`, and other social media links.

### Example

Below is a complete example:
```python
from google_scraper import GoogleScraper

google = GoogleScraper()

data = google.search("Google LLC", linkedin=True)
print(data['business_info'])
```

## Directory Structure

```
googlescraper/
├── google_scraper.py      # Main script
├── requirements.txt       # Dependencies
├── .env                   # Environment variables
```

## Dependencies

- `requests` for HTTP requests
- `BeautifulSoup4` for HTML parsing
- `rich` for enhanced terminal output
- `python-dotenv` for managing environment variables

## Notes

- Ensure your SmartProxy credentials are valid; otherwise, requests will fail.
- Use the scraper responsibly and adhere to Google’s terms of service.

## Contributing

Contributions are welcome! If you encounter bugs or have feature requests, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
