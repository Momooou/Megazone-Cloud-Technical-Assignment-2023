# iam role
resource "aws_iam_role" "hello_lambda_exec" {
  name = "hello-lambda"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

# iam role policy 
resource "aws_iam_role_policy_attachment" "hello_lambda_policy" {
  role       = aws_iam_role.hello_lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# lambda function
resource "aws_lambda_function" "hello" {
  function_name = "hello"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.lambda_hello.key

  runtime = "python3.9"
  handler = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.lambda_hello.output_base64sha256

  role = aws_iam_role.hello_lambda_exec.arn
}

# cloudwatch group
resource "aws_cloudwatch_log_group" "hello" {
  name = "/aws/lambda/${aws_lambda_function.hello.function_name}"

  retention_in_days = 14
}

# zip
data "archive_file" "lambda_hello" {
  type = "zip"

  source_dir  = "python_code"
  output_path = "python_code.zip"
}

# upload zip archive to s3
resource "aws_s3_object" "lambda_hello" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "hello.zip"
  source = data.archive_file.lambda_hello.output_path

  etag = filemd5(data.archive_file.lambda_hello.output_path)
}
