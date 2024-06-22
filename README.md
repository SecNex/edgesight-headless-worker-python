# EdgeSight: Headless Player

## Introduction

This is a headless player which allow to screenshot any website and cache it in a local storage as a PNG file. It is based on [Playwright](https://playwright.dev/), a library to automate chromium, firefox and webkit browsers. **Headless Player** was designed to be used together with [EdgeSight](https://secnex.io/edgesight), a digital signage solution.

## Installation

```bash
git clone https://github.com/SecNex/edgesight-headless-worker-python.git
cd edgesight-headless-worker-python
pip install -r requirements.txt
```

## Usage

```bash
python app.py [OPTIONS]
```

### Options

- `--noapi`: Disable the API server and run only the headless player with a database connection.
- `--force`: Force a cleanup of the database before starting the application.

## Plugins

**Headless Player** has a plugin system that allows to extend its functionality.

## Integrations

**Headless Player** can't only take screenshots of websites. It can show images, videos, pdfs and, when you need, it can show **PowerBI** dashboards and reports too.

- [x] Websites
- [ ] Images
- [ ] Videos
- [ ] PDFs
- [ ] PowerBI
    - [ ] Dashboards
    - [ ] Reports