# 🧠 Daily News AI Agent (AWS Lambda + Docker + Terraform)

An AI-powered serverless system that fetches latest news (AI, stocks, tech), summarizes it using Google ADK, and sends a daily email digest.

---

# 🚀 Tech Stack

- AWS Lambda (Docker-based)
- Amazon ECR (Container Registry)
- Amazon EventBridge (Scheduler)
- Amazon SES (Email)
- Terraform (Infrastructure as Code)
- Google ADK (AI Agent)
- Docker (Containerization)

---

# ⚠️ Why Docker Lambda?

The project uses heavy AI dependencies (Google ADK), which exceed AWS Lambda zip limits:

| Limit Type       | Value      |
| ---------------- | ---------- |
| Zip Upload Limit | ~50–70 MB  |
| Unzipped Limit   | 250 MB     |
| Our App Size     | ~700 MB ❌ |

👉 Solution: **Use Docker-based Lambda (10 GB limit)**

---

# 🐳 Docker Setup (Mac - Apple Silicon Compatible)

## 📁 Project Structure

```
daily-news-agent/
│
├── lambda/
│   ├── handler.py
│   ├── agent.py
│   ├── email_service.py
│   └── config.py
│
├── requirements.txt
└── Dockerfile
```

---

## 🧾 Dockerfile

```
FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY lambda/ .

CMD ["handler.lambda_handler"]
```

---

# 🏗️ Build Docker Image (IMPORTANT)

Mac (M1/M2/M3) builds ARM images by default ❌
AWS Lambda expects AMD64 ✅

👉 Use this command:

```
docker buildx build \
  --platform linux/amd64 \
  --provenance=false \
  --output=type=docker \
  -t daily-news-agent .
```

---

## 🔍 Verify Image

```
docker images
```

Optional:

```
docker inspect daily-news-agent | grep Architecture
```

👉 Should show: `amd64`

---

# ☁️ Push to Amazon ECR

## 1. Create Repository

```
aws ecr create-repository \
  --repository-name daily-news-agent \
  --region ap-south-1
```

---

## 2. Login to ECR

```
aws ecr get-login-password --region ap-south-1 \
| docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

---

## 3. Tag Image

```
docker tag daily-news-agent:latest \
<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/daily-news-agent:latest
```

---

## 4. Push Image

```
docker push \
<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/daily-news-agent:latest
```

---

# 🧪 Verify Image Format (CRITICAL)

```
aws ecr describe-images \
  --repository-name daily-news-agent \
  --region ap-south-1
```

👉 Must show:

```
application/vnd.docker.distribution.manifest.v2+json
```

❌ If you see:

```
application/vnd.oci.image.manifest.v1+json
```

👉 Lambda will fail → rebuild with correct command

---

# ⚙️ Terraform Configuration (Lambda)

```
resource "aws_lambda_function" "news_lambda" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_exec.arn

  package_type = "Image"
  image_uri    = "<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/daily-news-agent:latest"

  architectures = ["x86_64"]

  timeout     = 60
  memory_size = 512

  environment {
    variables = {
      SES_SENDER     = var.email_sender
      SES_RECEIVER   = var.email_receiver
      GOOGLE_API_KEY = var.google_api_key
    }
  }
}
```

---

# 🚀 Deploy

```
terraform apply
```

---

# 🧠 Common Issues & Fixes

## ❌ Error: `RequestEntityTooLargeException`

👉 Zip too big → use Docker

---

## ❌ Error: `image manifest not supported`

👉 OCI format → rebuild using:

```
docker buildx build --platform linux/amd64 --provenance=false --output=type=docker -t daily-news-agent .
```

---

## ❌ Lambda not triggering

👉 Check EventBridge cron (UTC vs IST)

---

## ❌ Email not sending

👉 Verify SES email + IAM permissions

---

# 🧹 Cleanup (Optional)

## Delete local images

```
docker system prune -a -f
```

---

## Delete ECR repo

```
aws ecr delete-repository \
  --repository-name daily-news-agent \
  --region ap-south-1 \
  --force
```

---

# 📌 Key Learnings

- Docker Lambda removes deployment limits
- Mac builds ARM by default → must force AMD64
- Lambda only supports Docker V2 image format
- Terraform manages infra, not image build

---

# 🚀 Future Improvements

- Better email formatting (HTML)
- Add stock portfolio insights
- Store history in S3/DynamoDB
- CI/CD with GitHub Actions

---

# 🧠 Author

Aditya Joshi
Built as part of AI + Cloud learning journey 🚀
