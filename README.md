# Bookmark Processing Script

Automates bookmark creation process for multiple domains from a CSV file.

## Features

-   Processes CSV files with email addresses
-   Automatic duplicate prevention
-   Environment variable configuration
-   Error handling and logging
-   Fallback to default image when missing
-   Optimized HTTP connections

## Setup

1. Install dependencies:

```title bash:install
pip install -r requirements.txt
```

2. Create .env file with your credentials:

    BASE_URL="your_base_url"
    AUTH_COOKIE="your_auth_cookie"
    DEFAULT_IMAGE="optional_default_image_url"

3. Prepare CSV file (input.csv) with email addresses:

```title csv:emails
emails
user1@example.com
user2@test.org
```

## The script will:

    Read domains from input.csv

    Remove duplicates

    Process each unique domain

    Output progress and results

## Error Handling

    Skips invalid email formats

    Continues processing after individual domain errors

    Logs failures to console

**Key Improvements:**

1. **CSV Processing:**

    - Reads emails from CSV file
    - Extracts unique domains automatically
    - Handles file not found and invalid formats

2. **Duplicate Prevention:**

    - Maintains set of processed domains
    - Skips already processed entries

3. **Environment Configuration:**

    - Uses `.env` file for sensitive data
    - Configurable default image URL

4. **Error Handling:**

    - Robust try/except blocks
    - Timeouts for network requests
    - Validation of environment variables

5. **Optimizations:**

    - Reusable HTTP headers
    - Connection pooling via requests
    - Batch processing of domains

6. **Image Handling:**

    - Automatic fallback to default image
    - Configurable via environment variable

7. **Structure:**
    - Class-based design for maintainability
    - Separate methods for different responsibilities
    - Configurable timeout values

**Notes:**

1. The CSV file must have an "emails" column header
2. Invalid emails will be skipped automatically
3. Network errors will be logged but won't stop processing
4. The script preserves case in domains but processes them case-insensitively
5. All sensitive configuration is stored in `.env` file
