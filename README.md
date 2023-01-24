<h1 align="center">Vextractor</h1>

<p align="center">
    <a href="https://github.com/IsFilimonov/vk-data-extractor"><img src="https://raw.githubusercontent.com/IsFilimonov/vk-data-extractor/main/assets/header.png" alt="Vextractor header"></a>
</p>

> 🐈‍⬛ Cat says meow!\
> 🐕 Dog says woof!\
> 🤖 Vextractor says vextract! vextract! vextract!

**Vextractor** is a quick and handy extractor of user data from [VKontakte](vk.com) from CLI.

The idea for this project arose from another project's needs. It is always more convenient to analyze data in tabular form. Not everyone can work directly with the vk API, just type a few commands into the console and get the result.

<p align="center">
    <a href="https://results.pre-commit.ci/latest/github/IsFilimonov/vk-data-extractor/main" target="_blank">
        <img src="https://results.pre-commit.ci/badge/github/IsFilimonov/vk-data-extractor/main.svg" alt="pre-commit"></a>
</p>

---

<p align="center"><a href="https://github.com/IsFilimonov/vk-data-extractor#usage">commands</a></p>

---

## Acknowledgements

- [Pallets Projects](https://palletsprojects.com/) for the [Click](https://github.com/pallets/click) CLI toolkit;
- Kirill aka [@python273](https://github.com/python273) and [contributors](https://github.com/python273/vk_api/graphs/contributors) for the [vk_api](https://github.com/python273/vk_api).


## Secrets

Fill `.env.example` and then rename it to `.env`.

Also you can use options `--login` and `--password`, but it's not as convenient.


## Installing

Install and update using [poetry](https://python-poetry.org/docs/cli/#install):
```bash
poetry install --only main
```

### Groups

Poetry [provides](https://python-poetry.org/docs/master/managing-dependencies/) a way to organize dependencies by groups. The Vextractor consists of:
- Main group;
- Dev dependencies;
- Typing dependencies;
- Docs dependencies;
- Tests dependencies.


## Usage

Vextractor uses the short cry `vextract` for convenience.

There are several ways to call Vextractor:
- Without activating virtual environment:
```bash
poetry run vextract
```
- With activating virtual environment:
```bash
poetry shell
vextract
```

### Help

**Note**: use one of the options: `-h` or `--help`, not both.

Available commands: `vextract` or `vextract -h/--help`.

Detail information for commands: `vextract birthdays -h/--help`

### Commands

- `vextract birthdays` -- Extract friends birthdays.


## LICENSE

Vextractor is licensed under the MIT/Expat license, see the [LICENSE](https://github.com/IsFilimonov/vk-data-extractor/blob/main/LICENSE) file for details.
