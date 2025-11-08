# uapi-cli

A lightweight, developer-friendly command-line interface for the **[uAPI](https://docs.uapi.nl/)** SDK.  
Built for quick access to uAPI’s web intelligence endpoints — right from your terminal.

---

## 🚀 Overview

`uapi-cli` provides an elegant way to interact with uAPI’s REST endpoints without writing code.  
It’s powered by the official [`usdk`](https://pypi.org/project/usdk/) Python package and supports:

- **`extract`** – fetch and structure data from any public web URL  
- **`search`** – perform web searches or ask natural language questions

---

## 🧩 Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/marcingrzegzhik/uapi-cli.git
cd uapi-cli
pip install -e .
````

---

## 🔑 Setup

You’ll need your **UAPI API key** to authenticate.

```bash
export UAPI_API_KEY="your_real_api_key_here"
```

To make this permanent, add it to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export UAPI_API_KEY="your_real_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

---

## 💡 Usage

### Extract structured data from a webpage

```bash
uapi extract https://finance.yahoo.com/quote/AAPL/
```

Example output:

```
=== Extracted Data ===

company_name              : Apple Inc.
ticker                    : AAPL
exchange                  : NasdaqGS
market_cap                : 3967000000000
sector                    : Technology
industry                  : Consumer Electronics
similar_companies:
  [1]
    name                  : Samsung Electronics Co., Ltd.
    ticker                : 005930.KS
    price                 : 97900
  [2]
    name                  : GoPro, Inc.
    ticker                : GPRO
    price                 : 1.53
```

---

### Ask questions or search the web

```bash
uapi search When is the next solar eclipse?
```

Example output:

```
=== Answer ===
The next total solar eclipse will occur on August 12, 2026, visible across the Arctic and parts of Greenland and Iceland.

=== Sources ===
• NASA Eclipse Calendar — https://eclipse.gsfc.nasa.gov
• Space.com — https://www.space.com/solar-eclipses
```

---

## 🛠️ Development

Run locally for testing:

```bash
python uapi_cli.py extract https://example.com
python uapi_cli.py search "Best AI companies 2025"
```

Uninstall:

```bash
pip uninstall uapi-cli
```

---

## 🧰 Requirements

* Python **3.8+**
* `usdk` (installed automatically)
* A valid `UAPI_API_KEY`

---

## 📜 License

Licensed under the **Apache 2.0 License**.
See [LICENSE](LICENSE) for details.
