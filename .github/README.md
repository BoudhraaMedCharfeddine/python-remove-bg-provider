# GitHub Configuration

This directory contains all GitHub-related configuration files for the Python Remove Background Provider project.

## Workflows

### CI/CD Pipeline (`workflows/ci.yml`)
- **Triggers**: Push to main/develop, pull requests, releases
- **Features**:
  - Multi-version Python testing (3.11, 3.12)
  - Code linting with flake8
  - Type checking with mypy
  - Docker image building and pushing
  - Security scanning with Trivy
  - Coverage reporting to Codecov

### Docker Integration Tests (`workflows/docker-test.yml`)
- **Triggers**: Push to main/develop, pull requests, manual dispatch
- **Features**:
  - Comprehensive Docker testing
  - Docker Compose testing
  - Multiple model testing
  - Error handling validation
  - Performance testing

### Security Analysis (`workflows/security.yml`)
- **Triggers**: Push to main/develop, pull requests, weekly schedule, manual dispatch
- **Features**:
  - Dependency vulnerability scanning (safety, pip-audit)
  - Static code analysis (bandit, semgrep)
  - Docker image security scanning (Trivy)
  - License compliance checking

### Release and Deploy (`workflows/release.yml`)
- **Triggers**: Releases, manual dispatch
- **Features**:
  - Multi-architecture Docker image building
  - Release testing
  - Automatic changelog generation
  - Container registry publishing

### CodeQL (`workflows/codeql.yml`)
- **Triggers**: Push to main/develop, pull requests, weekly schedule
- **Features**:
  - Static code analysis for security vulnerabilities
  - Automatic upload to GitHub Security tab

## Issue Templates

### Bug Report (`ISSUE_TEMPLATE/bug_report.yml`)
- Structured bug reporting with version, deployment method, steps to reproduce
- Includes fields for expected vs actual behavior, logs, and additional context

### Feature Request (`ISSUE_TEMPLATE/feature_request.yml`)
- Structured feature requests with problem description, proposed solution
- Includes categorization and use case information

## Pull Request Template (`pull_request_template.md`)
- Comprehensive checklist for contributors
- Includes testing, security, documentation, and code quality checks

## Dependabot (`dependabot.yml`)
- Automatic dependency updates for:
  - Python packages (pip)
  - Docker base images
  - GitHub Actions
- Runs weekly on Mondays at 9:00 AM

## Labels (`labels.yml`)
- Comprehensive label system for:
  - Issue types (bug, enhancement, documentation, question)
  - Priority levels (high, medium, low)
  - Status tracking (needs-triage, in-progress, blocked, ready-for-review)
  - Categories (api, docker, performance, security, tests, ci/cd)
  - Model-specific labels (u2net, u2net_human_seg, silueta, isnet-general-use)
  - Size indicators (small, medium, large)
  - Breaking change indicators

## Usage

### Setting up GitHub Actions

1. **Push the workflow files** to your repository
2. **Enable GitHub Actions** in repository settings
3. **Configure secrets** if needed:
   - `GITHUB_TOKEN` (automatically provided)
   - `SNYK_TOKEN` (optional, for Snyk security scanning)

### Customizing Workflows

- **Modify triggers**: Update the `on:` section in workflow files
- **Add new jobs**: Follow the existing pattern in workflow files
- **Update dependencies**: Modify version numbers in workflow steps
- **Change schedules**: Update cron expressions for scheduled runs

### Adding New Workflows

1. Create a new `.yml` file in `workflows/`
2. Follow the existing naming convention
3. Include appropriate triggers and permissions
4. Test the workflow with a pull request

## Best Practices

### Security
- Use `GITHUB_TOKEN` with minimal required permissions
- Scan for secrets in code before pushing
- Regularly update action versions
- Use official actions from verified publishers

### Performance
- Use caching for dependencies and build artifacts
- Run tests in parallel when possible
- Use matrix strategies for multi-version testing
- Clean up resources after jobs complete

### Maintenance
- Regularly update GitHub Actions to latest versions
- Monitor workflow runs for failures
- Review and update dependencies monthly
- Keep workflow files clean and well-documented

## Troubleshooting

### Common Issues

1. **Permission errors**: Check workflow permissions in repository settings
2. **Dependency failures**: Verify package versions and availability
3. **Docker build failures**: Check Dockerfile syntax and base images
4. **Test failures**: Review test logs and update tests as needed

### Getting Help

- Check workflow logs in the Actions tab
- Review GitHub Actions documentation
- Open an issue for workflow-related problems
- Check the main project README for setup instructions




