[
  {
    "name": "fiap-app",
    "image": "010526254534.dkr.ecr.us-east-2.amazonaws.com/agenda:latest",
    "cpu": 256,
    "memory": 512,
    "networkMode": "awsvpc",
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fiap-app",
          "awslogs-region": "us-east-2",
          "awslogs-stream-prefix": "ecs"
        }
    },
    "portMappings": [
      {
        "containerPort": 8080,
        "hostPort": 8080
      }
    ]
  }
]