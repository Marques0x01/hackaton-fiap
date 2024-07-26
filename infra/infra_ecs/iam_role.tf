resource "aws_iam_role" "role" {
  name = "fiap-app-role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Effect" : "Allow",
      "Principal" : {
        "Service" : "ecs-tasks.amazonaws.com"
      },
      "Action" : "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "policy" {
  name = "fiap-app-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Effect" : "Allow",
      "Action" : [
        "rds:*",
        "elasticloadbalancing:*",
        "ec2:*",
        "ecs:*",
        "ecr:*",
        "logs:*"
      ],
      "Resource" : "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "aws_iam_role_policy_attachment" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}
