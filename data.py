#!/usr/bin/env python
import pathlib

import frontmatter
import yaml

exclude = {pathlib.Path("content/admin/config.yml")}


def main():
    static_raw = pathlib.Path("combine_static.yml").read_text()
    data = yaml.safe_load(static_raw)

    for key, value in get_all_data().items():
        data["variables"][key] = {"default": value}

    pathlib.Path("combine.yml").write_text(yaml.safe_dump(data))


def get_all_data():
    path = pathlib.Path("content")
    data = {}
    mapping = {".md": extract_md, ".yml": extract_yml}

    for subpath in (*path.rglob("*.md"), *path.rglob("*.yml")):
        if subpath in exclude:
            continue

        file_data = mapping[subpath.suffix](path=subpath)
        name = str(subpath.stem.lstrip("_"))
        data[name] = file_data
        print(f"Copying {name} from {subpath}")

    return data


def extract_md(path):
    metadata, content = frontmatter.parse(path.read_text())
    return {"path": str(path), "body": content, **metadata}


def extract_yml(path):
    return yaml.safe_load(path.read_text())


if __name__ == "__main__":
    main()
