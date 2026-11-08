# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

An interactive, Windows-only console tool that scrapes an **NFC-e** (consumer electronic invoice) from the SEFAZ-CE portal (`http://nfce.sefaz.ce.gov.br/pages/consultaNota.jsf`) with Selenium + **Microsoft Edge**, writes it as a JSON file to `target/`, and then checks that the item totals add up to the paid total. User-facing messages and commit messages are in Portuguese.

## Commands

```powershell
.\venv\Scripts\Activate.ps1          # venv lives in ./venv (git-ignored)
pip install -r requirements.txt
python main.py                       # must run from repo root (relative paths: companies.txt, target/)
pyinstaller main.spec                # builds dist/main.exe (console app)
```

There are no tests, linter, or formatter configured.

Running `main.py` is interactive and needs a human: it asks for the 44-digit access key, then the **CAPTCHA** shown in the Edge window (up to 5 attempts), and loops until you type `exit`. You can't run it end-to-end non-interactively.

## Runtime requirements

- `driver/msedgedriver.exe` must match the installed Edge version. `driver/` is git-ignored. When Edge updates, startup fails with a message telling the user to download the matching driver.
- `target/` must exist (it's git-ignored, and the code does not create it).

## Architecture

`main.py` is a flat script with no `main()` function. At import time it builds every reader and starts the WebDriver, then runs the input loop. Each loop iteration:

1. Submits the access key and CAPTCHA. It knows the result page has loaded when the CAPTCHA field (`acompanhamentoForm:codigoAcesso`) can no longer be found (`NoSuchElementException`).
2. Picks the output filename: fantasy name, then company name, then the access key. The name is then normalized through `companies.txt`.
3. Builds the JSON dict field by field and writes `target/<YYYY-MM-DD HHMM> <company>.json`.
4. Runs `DataValidator` with `ROUND_HALF_UP`, and if that doesn't match, runs it again with truncation.

**Readers** (`src/readers/*Reader.py`): one class per JSON field, each with a single `get(...)` method.
- Most readers take the `driver`. They click a result-page tab (`tab_3` = products, `tab_4` = totals, `tab_6` = payments, `tab_7` = additional info) and then walk the DOM, usually by positional indexes such as `tr[6]` / `td[3]`. A change to the SEFAZ page layout breaks these readers.
- `ItemListReader` and `PaymentListReader` pair the `table.toggle.box` summary rows with the hidden `table.toggable.box` detail rows (they force `display:block` before reading them). They look up fields by their accent-insensitive label text through `getValueWithLabel`, which returns `0` when the label isn't found.
- Some readers parse the access key instead of the page: `MfeReader` (`[22:31]`) and `CfeKeyReader`. `main.py` also slices it directly: tax ID `[6:20]`, extract number `[31:37]`.
- Many JSON fields are placeholder stubs in `main.py` (`getIncrease`, `getTotalTaxes`, `getCustomer`, …). The JSON schema keeps fields and spellings from an earlier CF-e/SAT format (`satNumber`, `cfeKey`, `costumerTaxIdNumber`). Don't rename them, because the output format is consumed elsewhere.

**`ConverterUtils.toDecimal`** converts Brazilian-formatted numbers (`1.234,56`) to a `float`, and returns `0` on failure. `DataValidator` converts values back to `Decimal` through `str()` before doing arithmetic.

**`companies.txt`**: lines of `<CNPJ>;<standardized name>` (UTF-8). It is matched as a *substring* of the tax ID taken from the access key. If no line matches, `main.py` **appends** `<taxId>;<name> (nao padronizado)` to the file, so this tracked file changes as a side effect of running the tool. Those lines are meant to be edited by hand into proper names.
