---
id: devops
title: DevOps for developers
version: 1
activity_kinds: code, browser, writing
lesson_to_practice: balanced
timeboxes: lesson=10, exercise=45, review=5, project=90, placement=15
red_thread: yes
survey_ceiling: discovered
---

# DevOps for developers

## Outcome and boundary

For a developer who writes applications and wants to ship and run them alone. By the end, the learner takes
an application made of a frontend, an API and a database, and on their own: packages it with Docker, runs the
whole stack locally with Compose, tests and builds it in a GitHub Actions pipeline, describes its
infrastructure in Terraform, deploys it on AWS, runs it on Kubernetes, watches it with logs, metrics and
alerts, and handles an incident with a runbook and a postmortem. The learner can explain and defend each
choice in a technical interview.

The target is a developer who delivers, not a DevOps or SRE engineer. Kubernetes is taught to the level of
"I deploy, configure and debug my application on a cluster", never to cluster administration.

Starting point, declared and not observed: some Docker and some GitHub Actions, without ease; no Linux
administration, networking, Terraform, AWS or Kubernetes. The placement test (15 minutes) mainly compresses
the shell, Git and Docker units. What was demonstrated in another program does not count here.

Budget is zero. Everything runs on the learner's Mac by default: Docker, Compose, `kind` for Kubernetes,
LocalStack and Terraform for AWS, GitHub Actions on a public repository, Prometheus and Grafana in
containers. Real AWS is reached only in the AWS units, only with the free offer, and only after a billing
alarm is in place. Opening an AWS account requires a bank card, so every real-AWS step has a LocalStack
equivalent and stays optional. The free-tier terms are checked on the AWS site at that moment, since they
change.

Activities are of three kinds. Code: shell scripts, Dockerfiles, workflows, Terraform, Kubernetes manifests
and small application changes, each checked by a test or a command whose result is stated in advance; the
learner writes every line. Browser: short quizzes after lessons and for reviews. Writing: a deployment plan,
a runbook, a postmortem, ADRs.

Sources, all free: roadmap.sh DevOps as the skeleton, The Missing Semester (MIT) for the shell, Linux Journey,
the Docker documentation, the GitHub Actions documentation, The Twelve-Factor App, the HashiCorp Terraform
tutorials, the AWS documentation and AWS Skill Builder free courses, the Kubernetes documentation and its
tutorials, the Prometheus, Grafana and OpenTelemetry documentation, the Google SRE book (free online), and the
OWASP CI/CD Security Top 10.

Deliberately out of scope: cluster administration, writing Kubernetes operators, Ansible and configuration
management in depth, multi-cloud, Azure and Google Cloud, on-call rotations, and AWS certification
preparation. Helm, GitOps with Argo CD, serverless, service meshes, Ansible and other clouds are surveyed only.

The program stands alone: a stranger can follow it without any other. It keeps its own evidence.

## Red-thread project

One application is shipped through the whole program, in its own public Git repository. It must have a
frontend, an API and a database. It is chosen with the learner before the Docker unit: an application the
learner already wrote, or, if none fits, a deliberately small one the learner writes during that unit. Techne
never writes the application.

From the Docker unit on, each unit lands on the project: Dockerfiles, the Compose stack, the CI pipeline, the
release and deployment pipeline, the Terraform code, the AWS deployment, the Kubernetes manifests, the
observability stack, the pipeline's security checks, and finally a runbook and a postmortem of a simulated
incident. The project is never ahead of what was taught.

Project sessions are bounded at 90 minutes. Work arrives as tickets, written in English on GitHub, like
commits and pull requests. A ticket is done when its pipeline is green and its pull request is merged.

## Sequence

### Unit 1 — Linux and the shell (compressible by placement)

- The filesystem, paths, files and directories; users, groups and permissions.
- Processes, signals, exit codes; environment variables; standard streams, pipes and redirections.
- `grep`, `find`, `sed`, `awk`, `jq` on real logs and JSON.
- Bash scripts: variables, conditions, loops, functions, `set -euo pipefail`.
- SSH and keys; package managers; services and `systemd` in a container.
- Exercise: a script that parses a log file and reports errors, with tests run by `bats`.

### Unit 2 — Networking for developers

- IP addresses, ports, TCP and UDP; localhost and `0.0.0.0`.
- DNS and its records; `dig`, `curl -v`, `nc`.
- HTTP over TLS, certificates and certificate authorities.
- Reverse proxies and load balancers; a reverse proxy in front of two services.
- Exercise: diagnose three broken setups (wrong port, wrong bind address, wrong DNS name).

### Unit 3 — Git for delivery (compressible by placement)

- Branches, merging and rebasing, resolving a conflict.
- Pull requests, review, protected branches.
- Conventional commits, tags and semantic versioning; trunk-based development.
- Red thread: the application is chosen, its repository created, its first tickets written.

### Unit 4 — Docker

- Images, containers and layers; what a container is and is not.
- Writing a Dockerfile; build context and `.dockerignore`; layer caching.
- Multi-stage builds; small and non-root images.
- Volumes and bind mounts; container networks; ports.
- Debugging a container: logs, `exec`, `inspect`.
- Red thread: a Dockerfile for the API and one for the frontend.

### Unit 5 — Compose and the local stack

- Several services, their network and their volumes; healthchecks and startup order.
- Configuration from the environment (Twelve-Factor); `.env` files; secrets kept out of images.
- Development stack versus production stack.
- Red thread: the whole application starts with one `docker compose up`.

### Unit 6 — Continuous integration with GitHub Actions

- Workflows, events, jobs, steps and runners; the job's environment.
- Dependency caching; matrices; artifacts; services in a job (a database for tests).
- Secrets and variables; permissions of `GITHUB_TOKEN`.
- Reusable workflows and composite actions; reading a failed run.
- Red thread: lint, tests and image build on every pull request.

### Unit 7 — Releases and continuous delivery

- Container registries (GitHub Container Registry); tagging images by version and by commit.
- Environments and manual approvals; promotion from staging to production.
- Deployment strategies: recreate, rolling, blue-green, canary; rollback.
- Database migrations during a deployment.
- Red thread: a tag publishes a versioned image and a changelog.

### Unit 8 — Infrastructure as code with Terraform

- Why declare infrastructure; providers, resources, data sources.
- `plan` and `apply`; state, and why it is shared and locked.
- Variables, outputs, modules; environments.
- Practised against LocalStack, then the Docker provider.
- Red thread: the project's infrastructure described in Terraform.

### Unit 9 — AWS foundations

- The account, regions and availability zones; the shared responsibility model.
- Billing: budgets and billing alarms, set before anything else; free-tier limits.
- IAM: users, roles, policies, least privilege; never using the root account.
- VPC, subnets, security groups; EC2; S3; RDS.
- The AWS CLI; everything also done in Terraform.

### Unit 10 — Shipping on AWS

- The frontend on S3 with CloudFront.
- The API in a container on EC2, behind a reverse proxy with TLS; the database on RDS.
- Container services compared: ECS on Fargate, App Runner, Lambda; what each costs.
- GitHub Actions authenticating to AWS with OIDC, without stored keys.
- CloudWatch logs and alarms.
- Red thread: the application deployed on AWS by the pipeline, or on LocalStack when real AWS is skipped.

### Unit 11 — Kubernetes for developers

- What Kubernetes solves; the cluster, nodes and the control plane, at reading level.
- Pods, Deployments, ReplicaSets, Services; `kubectl` and a local cluster with `kind`.
- ConfigMaps and Secrets; resource requests and limits; liveness and readiness probes.
- Ingress; rolling updates and rollback.
- Debugging: `describe`, `logs`, `events`, a pod that crashes in a loop.
- Red thread: the application runs on a local cluster.

### Unit 12 — Observability

- Structured logs and correlation identifiers.
- Metrics: Prometheus, the four golden signals, Grafana dashboards.
- Traces with OpenTelemetry.
- Alerts that are worth waking up for; SLIs, SLOs and error budgets.
- Red thread: dashboards and two alerts on the running application.

### Unit 13 — Security in the delivery chain

- Secrets management; least privilege for pipelines.
- Dependency updates with Dependabot; image scanning with Trivy; an SBOM.
- Pinning actions and images; the OWASP CI/CD Security Top 10.
- Red thread: the pipeline fails on a critical vulnerability.

### Unit 14 — Running in production

- Backups and a tested restore.
- Incidents: detecting, mitigating, communicating; runbooks.
- Blameless postmortems.
- Cost: reading a bill, what costs money when idle, shutting things down.
- Red thread: a simulated incident on the application, its runbook and its postmortem.

## Subject catalogue

### Linux and the shell — `dolinux.*`

`filesystem`, `permissions`, `processes-signals`, `exit-codes`, `env-vars`, `streams-pipes`, `text-tools`,
`jq`, `bash-scripting`, `ssh`, `packages-services`

### Networking — `donet.*`

`ip-ports`, `tcp-udp`, `bind-address`, `dns`, `diagnostic-tools`, `tls`, `reverse-proxy`, `load-balancer`

### Git for delivery — `dogit.*`

`branches`, `merge-rebase`, `conflicts`, `pull-requests`, `protected-branches`, `conventional-commits`,
`tags-semver`, `trunk-based`

### Docker — `dodocker.*`

`images-containers`, `dockerfile`, `build-cache`, `multi-stage`, `non-root`, `volumes`, `networks`,
`debugging`

### Compose — `docompose.*`

`services`, `healthchecks`, `twelve-factor-config`, `env-secrets`, `dev-vs-prod`

### Continuous integration — `doci.*`

`workflow-anatomy`, `triggers`, `caching`, `matrix`, `artifacts`, `job-services`, `secrets`,
`token-permissions`, `reusable-workflows`, `failed-runs`

### Continuous delivery — `docd.*`

`registry`, `image-tagging`, `environments`, `promotion`, `deploy-strategies`, `rollback`,
`deploy-migrations`, `changelog`

### Terraform — `doiac.*`

`declarative`, `providers-resources`, `plan-apply`, `state`, `remote-state-locking`, `variables-outputs`,
`modules`, `environments`

### AWS foundations — `doaws.*`

`regions-azs`, `shared-responsibility`, `billing-alarms`, `iam`, `least-privilege`, `vpc-subnets`,
`security-groups`, `ec2`, `s3`, `rds`, `cli`

### Shipping on AWS — `doship.*`

`static-cloudfront`, `api-on-ec2`, `tls-certificates`, `container-services`, `oidc-deploy`, `cloudwatch`

### Kubernetes — `dok8s.*`

`why-kubernetes`, `architecture`, `pods`, `deployments`, `services`, `kubectl`, `config-secrets`,
`resources`, `probes`, `ingress`, `rolling-updates`, `debugging`

### Observability — `doobs.*`

`structured-logs`, `correlation-ids`, `metrics`, `golden-signals`, `dashboards`, `tracing`, `alerting`,
`slo-error-budget`

### Delivery security — `dosec.*`

`secrets-management`, `pipeline-privilege`, `dependency-updates`, `image-scanning`, `sbom`, `pinning`,
`cicd-top10`

### Production — `doprod.*`

`backups-restore`, `incident-response`, `runbooks`, `postmortems`, `cost`

### Survey — `dosurvey.*`

`helm`, `gitops-argocd`, `ansible`, `serverless`, `service-mesh`, `other-clouds`

## Adaptation rules

- A new notion is taught in a 10-minute lesson, checked by a short quiz, practised on an isolated exercise,
  then applied to the project. The project never receives a notion that has not been practised in isolation.
- Units 1, 3 and 4 compress to their unproven subjects when the placement test shows the rest.
- Exercises are one mechanism at a time, each with a check stated in advance (a test, a command and its
  expected output, a green run). Difficulty rises by removing scaffolding, then by combining two earlier
  mechanisms, then by diagnosing a deliberately broken setup.
- Every real-AWS activity has a LocalStack or local equivalent, and the learner chooses. No real-AWS activity
  opens before a billing alarm exists, and each one ends by checking that nothing billable is left running.
- A subject already demonstrated in this program goes straight to a harder use inside the project.
- Transfer is the unannounced reuse of an earlier mechanism in a later ticket (a healthcheck turned into a
  readiness probe, a shell pipeline used to read a failed CI log). Used correctly without help, it counts as
  transferred.
- Survey subjects attach to the lessons of neighbouring units and never get a unit of their own.
