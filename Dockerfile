# AWS Lambda base image
FROM public.ecr.aws/lambda/python:3.13

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your lambda code
COPY lambda/ .

# Command for Lambda
CMD ["handler.lambda_handler"]