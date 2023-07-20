import io
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome import service
import sys

cfg = sys.modules[__name__]
cfg.webdriver_service = None


def patch_exe(executable_path):
    # from https://github.com/ultrafunkamsterdam/undetected-chromedriver
    if is_binary_patched(executable_path=executable_path):
        return True
    start = time.perf_counter()
    with io.open(executable_path, "r+b") as fh:
        content = fh.read()
        match_injected_codeblock = re.search(rb"\{window\.cdc.*?;\}", content)
        if match_injected_codeblock:
            target_bytes = match_injected_codeblock[0]
            new_target_bytes = b'{console.log("undetected chromedriver 1337!")}'.ljust(
                len(target_bytes), b" "
            )
            new_content = content.replace(target_bytes, new_target_bytes)
            if new_content == content:
                print(
                    "something went wrong patching the driver binary. could not find injection code block"
                )
            else:
                print(
                    "found block:\n%s\nreplacing with:\n%s"
                    % (target_bytes, new_target_bytes)
                )
            fh.seek(0)
            fh.write(new_content)
    print("patching took us {:.2f} seconds".format(time.perf_counter() - start))


def is_binary_patched(executable_path=None):
    try:
        with io.open(executable_path, "rb") as fh:
            return fh.read().find(b"undetected chromedriver") != -1
    except FileNotFoundError:
        return False


def start_opera_driver(
    opera_browser_exe,
    opera_driver_exe,
    userdir=None,
    arguments=(
        "--no-sandbox",
        "--test-type",
        "--no-default-browser-check",
        "--no-first-run",
        "--incognito",
        "--start-maximized",
    ),
):
    r"""
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
    """
    if not os.path.exists(opera_driver_exe):
        raise OSError('Opera driver not found! Download it from: https://github.com/operasoftware/operachromiumdriver/releases')
    # Patch the Opera WebDriver binary to make it undetected by certain detections
    patch_exe(opera_driver_exe)

    # Create the user directory if provided
    if userdir:
        if not os.path.exists(userdir):
            os.makedirs(userdir)

    # Start the WebDriver service
    cfg.webdriver_service = service.Service(opera_driver_exe)
    cfg.webdriver_service.start()

    # Configure Opera WebDriver options
    options = webdriver.ChromeOptions()
    options.binary_location = opera_browser_exe
    options.add_experimental_option("w3c", True)
    if userdir:
        options.add_argument(f"--user-data-dir={userdir}")
    for a in arguments:
        options.add_argument(a)

    # Create and return the WebDriver instance
    driver = webdriver.Remote(cfg.webdriver_service.service_url, options=options)
    return driver

