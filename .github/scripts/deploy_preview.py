# /// script
# requires-python = ">=3.12"
# ///
import json
import os
import pathlib
import re
import subprocess
import sys
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


def set_status(deployment_id, state, url=None):
    payload = {"state": state, "log_url": os.environ["RUN_URL"]}
    if url:
        payload["environment_url"] = url
    gh_api(
        f"repos/{os.environ['GITHUB_REPOSITORY']}/deployments/{deployment_id}/statuses",
        payload,
    )


def start():
    deployment = gh_api(
        f"repos/{os.environ['GITHUB_REPOSITORY']}/deployments",
        {
            "ref": os.environ["HEAD_SHA"],
            "environment": "preview",
            "auto_merge": False,
            "required_contexts": [],
            "transient_environment": True,
        },
    )
    set_status(deployment["id"], "in_progress")
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"deployment_id={deployment['id']}\n")


def deploy():
    url = upload(alias_for(os.environ["HEAD_REF"]))
    set_status(os.environ["DEPLOYMENT_ID"], "success", url)
    print(f"Preview: {url}")


def fail():
    set_status(os.environ["DEPLOYMENT_ID"], os.environ["FAILED_STATE"])


def main():
    {"start": start, "deploy": deploy, "fail": fail}[sys.argv[1]]()


if __name__ == "__main__":
    main()
