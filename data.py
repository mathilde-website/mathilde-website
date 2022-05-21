#!/usr/bin/env python
import pathlib

import frontmatter
import yaml

additional_yml_files = [
    "metadata.yml",
    "seo_metadata.yml",
]


def main():
    static_raw = pathlib.Path("combine_static.yml").read_text()
    data = yaml.safe_load(static_raw)

    for key, value in get_all_data().items():
        data["variables"][key] = {"default": value}

    pathlib.Path("combine.yml").write_text(yaml.safe_dump(data))


def get_all_data():
    path = pathlib.Path("content")
    data = {}

    for subpath in path.rglob("*.md"):
        file_data = extract_data(path=subpath)
        data[str(subpath.stem)] = file_data

    for filename in additional_yml_files:
        path = pathlib.Path(filename)
        data[path.stem] = yaml.safe_load(path.read_text())

    return data


def extract_data(path):
    metadata, content = frontmatter.parse(path.read_text())
    return {"path": str(path), "body": content, **metadata}


if __name__ == "__main__":
    main()
