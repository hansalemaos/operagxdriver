# OperaGx webdriver with cdc patch. 

## pip install operagxdriver 


```python
    Start the Opera WebDriver and return the WebDriver instance.

    This function starts the Opera WebDriver, which allows you to automate interactions
    with the Opera web browser. It uses the Selenium library and requires the paths to
    the Opera browser executable and the Opera WebDriver executable.

    Important! A CDC patch (from https://github.com/ultrafunkamsterdam/undetected-chromedriver ) is applied before running the EXE file.

    Note: Before running this function, make sure to download the appropriate Opera
    WebDriver version that matches your installed Opera browser version.
    https://github.com/operasoftware/operachromiumdriver/releases

    Args:
        opera_browser_exe (str): The file path to the Opera browser executable.
        opera_driver_exe (str): The file path to the Opera WebDriver executable.
        userdir (str, optional): The user directory for the Opera profile. If provided,
            the browser will use this directory to store the user data (cookies, history,
            etc.). If not provided, the default profile will be used.
        arguments (tuple, optional): Additional command-line arguments to pass to the
            Opera WebDriver when launching the browser. Defaults to a tuple containing the
            following arguments: (
                "--no-sandbox",
                "--test-type",
                "--no-default-browser-check",
                "--no-first-run",
                "--incognito",
                "--start-maximized",
            )

    Returns:
        selenium.webdriver.remote.webdriver.WebDriver:
        The WebDriver instance for the running Opera browser.

    Example:
        from operagxdriver import start_opera_driver

        driver = start_opera_driver(
            opera_browser_exe=r"C:\Program Files\Opera GX\opera.exe",
            opera_driver_exe=r"C:\Users\hansc\Downloads\operadriver_win64\operadriver.exe",
            userdir='c:\\operabrowserprofile',
            arguments=(
                "--no-sandbox",
                "--test-type",
                "--no-default-browser-check",
                "--no-first-run",
                "--incognito",
                "--start-maximized",
            )
        )

```