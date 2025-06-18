# Specification

# 1. Files

- **Path:** dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh  
**Description:** Shell script to build the DFR Odoo backend Docker image. Takes parameters for image tag, Dockerfile path, and build context. Used by various CI/CD pipelines.  
**Template:** Shell Script  
**Dependancy Level:** 0  
**Name:** build_odoo_docker  
**Type:** UtilityScript  
**Relative Path:** scripts/common/build_odoo_docker.sh  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Docker Image Building (Odoo Backend)
    
**Requirement Ids:**
    
    - REQ-DIO-011
    - A.2.5
    
**Purpose:** Provides a reusable script to build the Docker image for the Odoo backend, ensuring consistency across different CI/CD platforms.  
**Logic Description:** 1. Accepts DOCKER_IMAGE_NAME, IMAGE_TAG, DOCKERFILE_PATH, BUILD_CONTEXT as arguments/env vars. 2. Navigates to the build context. 3. Executes 'docker build' command with provided arguments and appropriate labels. 4. Optionally pushes the image to a configured Docker registry if PUSH_IMAGE argument is true.  
**Documentation:**
    
    - **Summary:** Builds a Docker image for the DFR Odoo application. Inputs: image name, tag, Dockerfile path, build context. Outputs: built Docker image (optionally pushed).
    
**Namespace:**   
**Metadata:**
    
    - **Category:** BuildScript
    
- **Path:** dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh  
**Description:** Shell script to execute Odoo unit and/or integration tests. Configurable via environment variables or arguments to specify test types and modules. Used by CI/CD pipelines.  
**Template:** Shell Script  
**Dependancy Level:** 0  
**Name:** run_odoo_tests  
**Type:** UtilityScript  
**Relative Path:** scripts/common/run_odoo_tests.sh  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Unit Testing (Odoo Backend)
    - Automated Integration Testing (Odoo Backend)
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    - A.2.5
    
**Purpose:** Standardizes the execution of Odoo tests within CI/CD pipelines.  
**Logic Description:** 1. Accepts ODOO_DATABASE_NAME, ODOO_MODULES_TO_TEST, TEST_TYPE (unit/integration) as arguments/env vars. 2. Sets up a test database if required. 3. Executes Odoo test runner command (e.g., odoo-bin test --addons-path ... --test-enable -d test_db -i module_to_test). 4. Reports test results (exit code, summary).  
**Documentation:**
    
    - **Summary:** Runs Odoo tests. Inputs: database name, modules, test type. Outputs: test results.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** TestScript
    
- **Path:** dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh  
**Description:** Generic shell script for deploying applications. Can be adapted for Docker Compose, Kubernetes, or other deployment methods based on parameters. Used by CI/CD pipelines for staging/production deployments.  
**Template:** Shell Script  
**Dependancy Level:** 0  
**Name:** deploy_application  
**Type:** UtilityScript  
**Relative Path:** scripts/common/deploy_application.sh  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Deployment to Staging
    - Deployment to Production
    
**Requirement Ids:**
    
    - REQ-DIO-011
    - A.2.5
    
**Purpose:** Provides a common interface for application deployment logic, abstracting specific deployment tool commands.  
**Logic Description:** 1. Accepts DEPLOYMENT_ENV (staging/production), APP_NAME, IMAGE_TAG, CONFIG_FILE_PATH as arguments/env vars. 2. Loads environment-specific configurations. 3. Executes deployment commands (e.g., docker-compose up -d, kubectl apply -f). 4. Performs basic health checks post-deployment.  
**Documentation:**
    
    - **Summary:** Deploys an application. Inputs: environment, app name, image tag, config file. Outputs: deployment status.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** DeploymentScript
    
- **Path:** dfr_operations/cicd_pipelines/scripts/common/tag_git_release.sh  
**Description:** Shell script to create and push a Git tag based on Semantic Versioning. Used by CI/CD pipelines for release tagging.  
**Template:** Shell Script  
**Dependancy Level:** 0  
**Name:** tag_git_release  
**Type:** UtilityScript  
**Relative Path:** scripts/common/tag_git_release.sh  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Semantic Versioning and Tagging
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-CM-002
    - A.2.5
    
**Purpose:** Automates the process of tagging releases in Git according to Semantic Versioning principles.  
**Logic Description:** 1. Accepts VERSION (e.g., v1.2.3), GIT_REMOTE_NAME as arguments/env vars. 2. Creates an annotated Git tag: 'git tag -a $VERSION -m "Release $VERSION"'. 3. Pushes the tag to the remote repository: 'git push $GIT_REMOTE_NAME $VERSION'.  
**Documentation:**
    
    - **Summary:** Creates and pushes a Git release tag. Inputs: version string, remote name. Outputs: Git tag created and pushed.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** VersionControlScript
    
- **Path:** dfr_operations/cicd_pipelines/github_actions/workflows/dfr_odoo_backend_pipeline.yml  
**Description:** GitHub Actions workflow definition for the DFR Odoo backend. Automates build, test, SAST/DAST, Docker packaging, and deployment to staging & production environments.  
**Template:** GitHub Actions Workflow YAML  
**Dependancy Level:** 1  
**Name:** dfr_odoo_backend_pipeline  
**Type:** PipelineDefinition  
**Relative Path:** github_actions/workflows/dfr_odoo_backend_pipeline.yml  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    - CI/CD Pipeline
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Build (Odoo Backend)
    - Automated Testing (Odoo Backend)
    - Docker Image Packaging
    - SAST/DAST Integration
    - Deployment to Staging
    - Deployment to Production
    - Semantic Versioning Integration
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    - REQ-CM-002
    - A.2.5
    
**Purpose:** Defines the end-to-end CI/CD pipeline for the DFR Odoo backend components using GitHub Actions.  
**Logic Description:** name: DFR Odoo Backend CI/CD
on: [push, pull_request, workflow_dispatch]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...] # Checkout, setup Python, run linters (flake8)
  unit_test:
    runs-on: ubuntu-latest
    steps: [...] # Checkout, setup Odoo env, call scripts/common/run_odoo_tests.sh (unit)
  integration_test:
    runs-on: ubuntu-latest
    steps: [...] # Checkout, setup Odoo env with DB, call scripts/common/run_odoo_tests.sh (integration)
  sast_scan:
    runs-on: ubuntu-latest
    steps: [...] # Checkout, run SAST tool (e.g., SonarQube scanner, Bandit)
  build_docker:
    runs-on: ubuntu-latest
    needs: [lint, unit_test, integration_test, sast_scan]
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    steps: [...] # Checkout, login to Docker registry, call scripts/common/build_odoo_docker.sh and push
  dast_scan_container:
    runs-on: ubuntu-latest
    needs: build_docker
    steps: [...] # Pull image, run DAST tool against container or deploy to temp env for scan
  deploy_staging:
    runs-on: ubuntu-latest
    needs: [build_docker, dast_scan_container] # Potentially dast_scan_container
    if: github.ref == 'refs/heads/main' # Or develop branch
    environment: staging
    steps: [...] # Checkout, setup deploy tools, call scripts/common/deploy_application.sh with staging configs
  deploy_production:
    runs-on: ubuntu-latest
    needs: deploy_staging
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    steps: [...] # Checkout, setup deploy tools, call scripts/common/deploy_application.sh with prod configs, potentially call scripts/common/tag_git_release.sh if not tagged before build  
**Documentation:**
    
    - **Summary:** GitHub Actions workflow for DFR Odoo backend. Triggers on pushes/PRs. Includes linting, testing, security scans, Docker build/push, and deployments.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** CICDPipeline
    
- **Path:** dfr_operations/cicd_pipelines/github_actions/workflows/dfr_mobile_app_pipeline.yml  
**Description:** GitHub Actions workflow definition for the DFR Android Mobile App. Automates build (APK/AAB), test, SAST/DAST, packaging, and distribution to test tracks or app stores.  
**Template:** GitHub Actions Workflow YAML  
**Dependancy Level:** 1  
**Name:** dfr_mobile_app_pipeline  
**Type:** PipelineDefinition  
**Relative Path:** github_actions/workflows/dfr_mobile_app_pipeline.yml  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    - CI/CD Pipeline
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Build (Mobile App)
    - Automated Testing (Mobile App)
    - Mobile App Packaging (APK/AAB)
    - SAST/DAST Integration
    - Distribution to Test Tracks/Store
    - Semantic Versioning Integration
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    - REQ-CM-002
    - A.2.5
    
**Purpose:** Defines the end-to-end CI/CD pipeline for the DFR Android Mobile App using GitHub Actions.  
**Logic Description:** name: DFR Mobile App CI/CD
on: [push, pull_request, workflow_dispatch]
jobs:
  lint_and_static_analysis:
    runs-on: ubuntu-latest
    steps: [...] # Checkout, setup Android/Flutter env, run linters, SAST (e.g., MobSF static analysis)
  unit_tests:
    runs-on: ubuntu-latest # Or macos for iOS if Flutter cross-platform builds are ever included
    steps: [...] # Checkout, setup env, run unit tests (e.g., ./gradlew test or flutter test)
  integration_widget_tests:
    runs-on: ubuntu-latest
    steps: [...] # Checkout, setup env, run integration/widget tests (e.g., ./gradlew connectedCheck or flutter test integration_test)
  build_app:
    runs-on: ubuntu-latest
    needs: [lint_and_static_analysis, unit_tests, integration_widget_tests]
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    steps: [...] # Checkout, setup env, build APK/AAB (e.g., ./gradlew assembleRelease or flutter build apk --release), sign app, archive artifacts.
  security_scan_artifact:
    runs-on: ubuntu-latest
    needs: build_app
    steps: [...] # Download artifact, run DAST/security scan on APK/AAB (e.g., MobSF dynamic analysis if feasible in CI)
  deploy_to_test_track:
    runs-on: ubuntu-latest
    needs: [build_app, security_scan_artifact]
    if: github.ref == 'refs/heads/main'
    steps: [...] # Download artifact, deploy to Google Play Console internal/alpha/beta track using fastlane or similar.
  deploy_to_production_store:
    runs-on: ubuntu-latest
    needs: deploy_to_test_track
    if: startsWith(github.ref, 'refs/tags/v')
    steps: [...] # Promote build from test track to production or upload directly to production store.  
**Documentation:**
    
    - **Summary:** GitHub Actions workflow for DFR Mobile App. Triggers on pushes/PRs. Includes linting, testing, security scans, build/signing of APK/AAB, and distribution.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** CICDPipeline
    
- **Path:** dfr_operations/cicd_pipelines/gitlab_ci/.gitlab-ci.yml  
**Description:** Main GitLab CI pipeline configuration file for the DFR project. Orchestrates build, test, and deployment stages for both Odoo backend and mobile app components, potentially including templates.  
**Template:** GitLab CI YAML  
**Dependancy Level:** 1  
**Name:** .gitlab-ci  
**Type:** PipelineDefinition  
**Relative Path:** gitlab_ci/.gitlab-ci.yml  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    - CI/CD Pipeline
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized CI/CD Orchestration
    - Automated Build (Odoo & Mobile)
    - Automated Testing
    - Deployment Automation
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    - REQ-CM-002
    - A.2.5
    
**Purpose:** Defines all CI/CD stages and jobs for the DFR project within the GitLab CI ecosystem.  
**Logic Description:** stages:
  - validate
  - test
  - build
  - scan
  - deploy_staging
  - deploy_production

variables:
  DOCKER_IMAGE_NAME_ODOO: $CI_REGISTRY_IMAGE/dfr-odoo-backend
  # Other global variables

include:
  - '/gitlab_ci/templates/odoo_jobs.yml'
  - '/gitlab_ci/templates/mobile_jobs.yml'
  - '/gitlab_ci/templates/common_jobs.yml'

# Workflow rules to control when pipelines run
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_TAG'

# Example of job definition using a template
lint_odoo:
  stage: validate
  extends: .odoo_lint_template

deploy_odoo_staging:
  stage: deploy_staging
  extends: .deploy_template
  variables:
    DEPLOY_ENV: staging
    APP_NAME: dfr-odoo-backend
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
      when: on_success  
**Documentation:**
    
    - **Summary:** Root GitLab CI configuration. Defines stages and includes job templates for different components of the DFR system.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** CICDPipeline
    
- **Path:** dfr_operations/cicd_pipelines/gitlab_ci/templates/odoo_jobs.yml  
**Description:** GitLab CI template file containing reusable job definitions for DFR Odoo backend CI/CD stages like linting, testing, and building.  
**Template:** GitLab CI YAML Template  
**Dependancy Level:** 0  
**Name:** odoo_jobs  
**Type:** PipelineTemplate  
**Relative Path:** gitlab_ci/templates/odoo_jobs.yml  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Odoo CI Jobs
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    
**Purpose:** Provides standardized job definitions for Odoo backend CI/CD tasks to be included in the main .gitlab-ci.yml.  
**Logic Description:** .odoo_lint_template:
  stage: validate
  image: python:3.9-slim
  script:
    - pip install flake8
    - flake8 path/to/odoo/modules

.odoo_unit_test_template:
  stage: test
  image: $DOCKER_IMAGE_NAME_ODOO:$CI_COMMIT_SHORT_SHA # Assumes a base odoo image or one built in a prior stage for testing
  services:
    - postgres:14-alpine
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: test_user
    POSTGRES_PASSWORD: test_password
  script:
    - dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh unit

.build_odoo_docker_template:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
    - dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh $DOCKER_IMAGE_NAME_ODOO $CI_COMMIT_TAG # or $CI_COMMIT_SHORT_SHA
    - docker push $DOCKER_IMAGE_NAME_ODOO:$CI_COMMIT_TAG # or $CI_COMMIT_SHORT_SHA  
**Documentation:**
    
    - **Summary:** Contains GitLab CI job templates for Odoo backend linting, unit testing, and Docker image building.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** CICDPipelineTemplate
    
- **Path:** dfr_operations/cicd_pipelines/jenkins/pipelines/dfr_odoo_backend.Jenkinsfile  
**Description:** Jenkinsfile (declarative or scripted pipeline) for DFR Odoo backend CI/CD. Defines stages for build, test, scan, and deployment.  
**Template:** Jenkins Pipeline (Groovy)  
**Dependancy Level:** 1  
**Name:** dfr_odoo_backend.Jenkinsfile  
**Type:** PipelineDefinition  
**Relative Path:** jenkins/pipelines/dfr_odoo_backend.Jenkinsfile  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    - CI/CD Pipeline
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Automated Build (Odoo Backend)
    - Automated Testing (Odoo Backend)
    - Docker Image Packaging
    - Deployment Automation
    
**Requirement Ids:**
    
    - REQ-PCA-013
    - REQ-DIO-011
    - REQ-CM-002
    - A.2.5
    
**Purpose:** Manages the CI/CD lifecycle for DFR Odoo backend components using Jenkins.  
**Logic Description:** pipeline {
    agent any // Or specific agent with Docker, Python, Odoo tools
    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        ODOO_REPO_URL = 'git@github.com:your-org/dfr-odoo-modules.git'
        // Other environment variables
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: env.BRANCH_NAME ?: 'main', url: ODOO_REPO_URL
            }
        }
        stage('Lint') {
            steps {
                sh 'flake8 path/to/odoo/modules'
            }
        }
        stage('Unit Tests') {
            steps {
                // Could use a Docker agent with PostgreSQL service
                sh 'dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh unit'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def imageName = "your-registry/dfr-odoo-backend:${env.BUILD_ID}"
                    sh "dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh ${imageName} ${env.BUILD_ID} Dockerfile_odoo ."
                    withCredentials([string(credentialsId: DOCKER_CREDENTIALS_ID, variable: 'DOCKER_HUB_TOKEN')]) {
                        sh "echo $DOCKER_HUB_TOKEN | docker login -u your_docker_user --password-stdin"
                        sh "docker push ${imageName}"
                    }
                }
            }
        }
        stage('Deploy to Staging') {
            when { branch 'develop' }
            steps {
                input 'Approve deployment to Staging?' // Manual approval gate
                sh "dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh staging dfr-odoo-backend ${env.BUILD_ID} path/to/staging-config.yml"
            }
        }
        stage('Deploy to Production') {
            when { branch 'main' ; หรือ tag 'v*' }
            steps {
                input 'Approve deployment to Production?'
                sh "dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh production dfr-odoo-backend ${env.BUILD_ID} path/to/prod-config.yml"
                sh "dfr_operations/cicd_pipelines/scripts/common/tag_git_release.sh v${env.BUILD_ID} origin" // Example tagging
            }
        }
    }
}  
**Documentation:**
    
    - **Summary:** Jenkins declarative pipeline for DFR Odoo backend. Covers checkout, lint, tests, Docker build/push, and conditional deployments.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** CICDPipeline
    
- **Path:** dfr_operations/cicd_pipelines/jenkins/vars/dfrPipelineUtils.groovy  
**Description:** Shared Groovy script for Jenkins pipelines, containing reusable functions for common CI/CD tasks within the DFR project (e.g., notification, custom deployment steps).  
**Template:** Jenkins Shared Library Script (Groovy)  
**Dependancy Level:** 0  
**Name:** dfrPipelineUtils  
**Type:** UtilityScript  
**Relative Path:** jenkins/vars/dfrPipelineUtils.groovy  
**Repository Id:** DFR_CICD_PIPELINES  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable Jenkins Pipeline Logic
    
**Requirement Ids:**
    
    - REQ-DIO-011
    
**Purpose:** Provides utility functions to simplify and standardize Jenkins pipeline definitions for the DFR project.  
**Logic Description:** // Example of a shared function
def notifyBuildStatus(String status, String recipientEmail) {
    echo "Notifying ${recipientEmail} of build status: ${status}"
    // mail to: recipientEmail, subject: "Build ${status}: ${currentBuild.fullDisplayName}", body: "Build details: ${currentBuild.absoluteUrl}"
}

def performSastScan(String toolName, String projectKey) {
    echo "Performing SAST scan with ${toolName} for project ${projectKey}"
    // sh "sast_tool_cli_command --project-key=${projectKey} ..."
}

return this;  
**Documentation:**
    
    - **Summary:** Contains shared Groovy functions for Jenkins pipelines, such as notification utilities or custom scan integrations.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** CICDPipelineUtility
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - ENABLE_SAST_SCANS_PER_COMMIT
  - ENABLE_DAST_SCANS_PER_BUILD
  - AUTO_DEPLOY_TO_STAGING_ON_MAIN_MERGE
  - REQUIRE_MANUAL_APPROVAL_FOR_PRODUCTION_DEPLOYMENT
  
- **Database Configs:**
  
  - STAGING_DB_HOST_PIPELINE_VAR
  - STAGING_DB_PORT_PIPELINE_VAR
  - PRODUCTION_DB_HOST_PIPELINE_VAR
  - PRODUCTION_DB_PORT_PIPELINE_VAR
  


---

