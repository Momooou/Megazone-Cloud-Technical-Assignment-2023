resource "aws_apigatewayv2_integration" "api_integration" {
  api_id = aws_apigatewayv2_api.api_gateway.id

  integration_uri    = aws_lambda_function.url_shortener.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "post" {
  api_id = aws_apigatewayv2_api.api_gateway.id

  route_key = "POST /urlshortener"
  target    = "integrations/${aws_apigatewayv2_integration.api_integration.id}"
}

resource "aws_apigatewayv2_route" "redirect" {
  api_id = aws_apigatewayv2_api.api_gateway.id

  route_key = "POST /urlshortener/{haha}"
  target    = "integrations/${aws_apigatewayv2_integration.api_integration.id}"
}

resource "aws_lambda_permission" "api_invoke_policy" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.url_shortener.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api_gateway.execution_arn}/*/*"
}

output "api_base_url" {
  value = aws_apigatewayv2_stage.api_gateway_stg.invoke_url
}

resource "local_file" "api_base_url" {
    content  = aws_apigatewayv2_stage.api_gateway_stg.invoke_url
    filename = "docs/api_base_url.txt"
}