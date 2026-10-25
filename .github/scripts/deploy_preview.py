# /// script
# requires-python = ">=3.12"
# ///
import json
import os
import pathlib
import re
import subprocess
import tempfile

WORKER_NAME = "mathilde-website"
# Cloudflare caps "<alias>-<worker name>" at 63 characters (a DNS label).
MAX_ALIAS_LENGTH = 63 - len(WORKER_NAME) - 1


def alias_for(branch):
    alias = re.sub(r"[^a-z0-9]+", "-", branch.lower()).strip("-")
    if not alias[:1].isalpha():
        alias = f"pr-{alias}"
    return alias[:MAX_ALIAS_LENGTH].rstrip("-")


def upload(alias):
    with tempfile.TemporaryDirectory() as tmp:
        output_file = pathlib.Path(tmp) / "wrangler.ndjson"
        subprocess.run(
            ["npx", "wrangler", "versions", "upload", "--preview-alias", alias],
            env={**os.environ, "WRANGLER_OUTPUT_FILE_PATH": str(output_file)},
            check=True,
        )
        for line in output_file.read_text().splitlines():
            entry = json.loads(line)
            if entry["type"] == "version-upload":
                return entry["preview_alias_url"]
    raise RuntimeError("wrangler did not report a preview URL")


def gh_api(path, payload):
    result = subprocess.run(
        ["gh", "api", path, "--method", "POST", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def record_deployment(url):
    repo = os.environ["GITHUB_REPOSITORY"]
    deployment = gh_api(
        f"repos/{repo}/deployments",
        {
            "ref": os.environ["HEAD_SHA"],
            "environment": "preview",
            "auto_merge": False,
            "required_contexts": [],
            "transient_environment": True,
        },
    )
    gh_api(
        f"repos/{repo}/deployments/{deployment['id']}/statuses",
        {
            "state": "success",
            "environment_url": url,
            "log_url": os.environ["RUN_URL"],
        },
    )


def main():
    url = upload(alias_for(os.environ["HEAD_REF"]))
    record_deployment(url)
    print(f"Preview: {url}")


if __name__ == "__main__":
    main()
