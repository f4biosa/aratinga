<h1 align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset=".github/aratinga.svg">
        <source media="(prefers-color-scheme: dark)" srcset=".github/aratinga-inverse.svg">
        <img width="343" src=".github/aratinga.svg" alt="Aratinga">
    </picture>
</h1>

# Aratinga - CMS

Aratinga is a web Content Management System (CMS) built in Python / Django and Wagtail.

A professional alternative for creating and marketing websites with Wagtail.

### Run:

```cli
aratinga start mysite
```

### Messages:

###### Creating a Aratinga project called mysite

###### Success\! mysite has been created

### Next steps:

```cli
cd mysite
```

```cli
python manage.py migrate
```

```cli
python manage.py createsuperuser
```

```cli
python manage.py runserver
```

### Go to: 'http://localhost:8000/admin/' and start editing your CMS site\!

-----

## 🧪 Tests (Aratinga Package Development)

Instructions for setting up the environment and running the `aratinga` package tests.

### 1\. Test Environment Setup

Before running the tests for the first time, the environment must be prepared.

**1.1. Create the "Host" Project**
The `aratinga` tests run "against" a real Django project. This project must be a "sibling" to the `aratinga` folder.

```bash
# 1. Navigate to the folder containing the 'aratinga' repository (e.g., C:\Repositories\)
cd ..

# 2. Create the host project (e.g., 'mysite')
aratinga start mysite

# 3. Go back to the Aratinga folder
cd aratinga
```

*(The name `mysite` is just an example. It can be any valid project name, but remember it for the next step.)*

**1.2. Create `pytest.ini` in the Host**
`pytest` needs to know which Django settings to use. Create the file `../mysite/pytest.ini` and paste the following content:

```copy to clipboard
[pytest]
DJANGO_SETTINGS_MODULE = mysite.settings.dev
python_paths = . ../aratinga/src
django_find_project = false
```

*(**Important:** If you used a different name than `mysite` in step 1.1, adjust the `DJANGO_SETTINGS_MODULE` to `yourname.settings.dev`.)*

**1.3. Install Test Dependencies**
The tests require `pytest`, `pytest-django`, and `pytest-playwright`.

```bash
  # While in the 'aratinga/' folder
  uv pip install pytest pytest-django pytest-playwright
```

**1.4. Install Playwright Browsers**

```bash
  uv run playwright install
```

**1.5. Create the E2E Test Theme**
The upload test (`test_theme_crud.py`) expects a ZIP file with a specific name (due to the regex in `forms.py`).

1.  Create a simple folder (e.g., `test_e2e`) with an `index.html` file inside.
2.  Compress it into a file named `aratinga-theme_test_e2e.zip`.
3.  Place this file in `aratinga/src/aratinga/tests/endpoint_to_endpoint/`.

### 2\. Unit Tests

Tests that check the `aratinga` app logic in isolation (e.g., `test_theme.py`).

1.  **Set up the environment** (required in PowerShell):

    ```bash
    # Tell Python where to find the 'mysite' project and the 'src' of aratinga
    $env:PYTHONPATH = "../mysite;src"
    ```

2.  **Run the unit tests:**

    ```bash
    # We use --ds to force the use of the correct settings
    uv run pytest src/aratinga/tests/test_theme.py --ds=mysite.settings.dev
    ```

### 3\. Endpoint-to-Endpoint (E2E) Tests

Tests that simulate real user clicks on the site (login, upload, etc.) using Playwright.

1.  **Set up the environment** (required in PowerShell):

    ```powershell
    # 1. Set up the PYTHONPATH (same as unit tests)
    $env:PYTHONPATH = "../mysite;src"

    # 2. Allow Django (Sync) to run with Playwright (Async)
    $env:DJANGO_ALLOW_ASYNC_UNSAFE = "1"
    ```

2.  **Run the E2E tests:**

    Execute to test **without** a GUI (headless browser 🙈):

    ```bash
    uv run pytest src/aratinga/tests/endpoint_to_endpoint/ --ds=mysite.settings.dev
    ```

    Execute to test **with** a GUI (headed browser 👀):

    ```bash
    uv run pytest src/aratinga/tests/endpoint_to_endpoint/ --ds=mysite.settings.dev --headed
    ```