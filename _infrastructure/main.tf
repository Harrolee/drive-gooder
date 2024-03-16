provider "aws" {
  region = "your_aws_region"
}

resource "aws_ecs_task_definition" "this" {
  family                   = "example-task"
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024

  container_definitions = jsonencode([
    {
      name      = "example-container"
      image     = "your_container_image"
      cpu       = 512
      memory    = 1024
      essential = true
      portMappings = [
        {
          containerPort = 80,
          hostPort      = 80,
          protocol      = "tcp",
        },
      ]
    },
  ])
}

resource "aws_ecs_cluster" "this" {
  name = "example-cluster"
}

resource "aws_ecs_service" "this" {
  name            = "example-service"
  cluster         = aws_ecs_cluster.example_cluster.id
  task_definition = aws_ecs_task_definition.example_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = ["your_subnet_id"]
    security_groups  = ["your_security_group_id"]
    assign_public_ip = true
  }

  depends_on = [aws_ecs_task_definition.example_task]
}
