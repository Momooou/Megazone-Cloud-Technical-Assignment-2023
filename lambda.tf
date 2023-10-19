# IAM role
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"

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

# IAM role policy 
resource "aws_iam_role_policy_attachment" "lambda_exec_role_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# lambda function
resource "aws_lambda_function" "url_shortener" {
  function_name = "url-shortener"

  # pacakge location
  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.upload_zip.key

  runtime = "python3.9"
  handler = "lambda_function.url_shortener"

  source_code_hash = data.archive_file.code_archive.output_base64sha256

  role = aws_iam_role.lambda_exec_role.arn
}

# cloudwatch group
resource "aws_cloudwatch_log_group" "url_shortenr_log_group" {
  name = "/aws/lambda/${aws_lambda_function.url_shortener.function_name}"

  retention_in_days = 14
}

# zip
data "archive_file" "code_archive" {
  type = "zip"

  source_dir  = "python_code"
  output_path = "python_code.zip"
}

# upload zip archive to s3
resource "aws_s3_object" "upload_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "code.zip"
  source = data.archive_file.code_archive.output_path

  etag = filemd5(data.archive_file.code_archive.output_path)
}
