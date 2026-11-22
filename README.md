# Daily News Agent Lambda

Serverless daily email digest that fetches AI and Indian market RSS headlines, summarizes them with Gemini through `google-genai`, formats an HTML email, and sends it through Amazon SES.

## Tech Stack

- AWS Lambda
- Amazon SES
- Google Gemini via `google-genai`
- Google News RSS
- Python 3.13 by default
- Zip-based Lambda deployment

## Project Structure

```text
.
├── lambda/
│   ├── agent.py
│   ├── config.py
│   ├── email_service.py
│   ├── handler.py
│   ├── html_formatter.py
│   └── news_service.py
├── package.sh
├── requirements.txt
└── README.md
```

## Environment Variables

Configure these in Lambda:

```text
GOOGLE_API_KEY=<your Gemini API key>
SES_SENDER=<verified SES sender email>
SES_RECEIVERS=<recipient1@example.com,recipient2@example.com>
```

`SES_SENDER` and every address in `SES_RECEIVERS` must be valid for your SES setup. If SES is still in sandbox mode, the sender and all recipients usually need to be verified.

For backward compatibility, `SES_RECEIVER=<recipient email>` still works when `SES_RECEIVERS` is not set.

With Terraform, pass multiple recipients as a list:

```hcl
email_receivers = [
  "recipient1@example.com",
  "recipient2@example.com",
]
```

## Dependencies

`requirements.txt` intentionally stays small:

```text
google-genai>=1.66.0,<2.0.0
cryptography>=46.0.0,<48.0.0
boto3
python-dotenv
```

`google-genai` is pinned to the current 1.x line because `google-cloud-aiplatform` requires `google-genai>=1.66.0,<2.0.0`. `cryptography` is capped below 48 to remain compatible with `pyOpenSSL 26.1.0`.

`boto3` is listed for local development, but `package.sh` excludes it from the zip because AWS Lambda already includes `boto3` and `botocore` in the Python runtime.

The project no longer uses Google ADK. Direct `google-genai` keeps the deployment much smaller.

## Build Lambda Zip

Run:

```bash
./package.sh
```

This creates:

```text
lambda.zip
```

The script installs dependencies using Lambda-compatible Linux wheels:

```bash
pip3 install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.13 \
  --only-binary=:all:
```

It also removes `__pycache__`, `.pyc`, tests, console scripts, and excludes AWS SDK packages already available in Lambda.

## Runtime And Architecture

Defaults:

```text
Python: 3.13
Architecture: x86_64
Platform: manylinux2014_x86_64
```

If your Lambda runtime is Python 3.12:

```bash
LAMBDA_PYTHON_VERSION=3.12 ./package.sh
```

If your Lambda architecture is ARM64:

```bash
LAMBDA_PLATFORM=manylinux2014_aarch64 ./package.sh
```

For ARM64 with Python 3.12:

```bash
LAMBDA_PYTHON_VERSION=3.12 LAMBDA_PLATFORM=manylinux2014_aarch64 ./package.sh
```

Make sure these match your Lambda function settings.

## Why The Packaging Script Matters

Some dependencies, especially `pydantic_core`, include compiled native files. If you run a normal `pip install` on macOS, pip may install macOS binaries. Lambda needs Linux binaries.

The common failure looks like:

```text
Unable to import module 'handler': No module named 'pydantic_core._pydantic_core'
```

The fix is to build the zip with Lambda Linux wheels, which `package.sh` now does.

You can verify the zip contains the Linux binary:

```bash
unzip -l lambda.zip | grep 'pydantic_core/_pydantic_core'
```

Expected for Python 3.13 x86_64:

```text
pydantic_core/_pydantic_core.cpython-313-x86_64-linux-gnu.so
```

## Deploy

Upload `lambda.zip` to your Lambda function.

Handler:

```text
handler.lambda_handler
```

Recommended settings:

```text
Runtime: Python 3.13
Architecture: x86_64
Timeout: 60 seconds or higher
Memory: 512 MB or higher
```

## Common Issues

### `pydantic_core._pydantic_core` import error

The zip was probably built for macOS or the wrong Lambda runtime/architecture. Rebuild with:

```bash
./package.sh
```

For Python 3.12 or ARM64, use the environment overrides shown above.

### Email not sending

Check:

- SES sender verification
- SES sandbox restrictions
- Lambda IAM permission for `ses:SendEmail`
- Region matches `ap-south-1` in `lambda/email_service.py`

### Empty or failed news fetch

The RSS fetch uses Google News RSS over the network. Make sure the Lambda has outbound internet access. If the function is inside a VPC, it may need NAT access.

## Notes

- RSS parsing uses Python standard library XML parsing, not `feedparser`, to avoid extra packaging complications.
- `lambda.zip` is intentionally not expected to include `google-adk`, `boto3`, `botocore`, or `feedparser`.
- The current zip is small enough for normal Lambda zip deployment.
