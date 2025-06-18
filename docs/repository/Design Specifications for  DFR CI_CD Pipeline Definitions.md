# Software Design Specification for DFR CI/CD Pipeline Definitions

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the DFR CI/CD Pipeline Definitions repository (`DFR_CICD_PIPELINES`). It outlines the design for CI/CD pipelines and supporting scripts to automate the build, testing, security scanning, packaging, and deployment of DFR software components, including Odoo backend modules and the Android mobile application. This specification will guide the implementation of CI/CD workflows using GitHub Actions, GitLab CI, and Jenkins, ensuring consistency, reliability, and auditable release processes.

### 1.2 Scope
The scope of this SDS covers the design of:
*   CI/CD pipeline definitions for GitHub Actions, GitLab CI, and Jenkins.
*   Reusable shell scripts for common CI/CD tasks (building Docker images, running tests, deploying applications, Git tagging).
*   Shared Groovy scripts for Jenkins pipeline utilities.
*   Integration points for SAST/DAST tools (SonarScanner CLI, OWASP ZAP).
*   Management of pipeline configurations and secrets.

### 1.3 Definitions, Acronyms, and Abbreviations
*   **CI:** Continuous Integration
*   **CD:** Continuous Deployment/Delivery
*   **DFR:** Digital Farmer Registry
*   **SDS:** Software Design Specification
*   **SAST:** Static Application Security Testing
*   **DAST:** Dynamic Application Security Testing
*   **SBOM:** Software Bill of Materials
*   **APK:** Android Package Kit
*   **AAB:** Android App Bundle
*   **YAML:** YAML Ain't Markup Language
*   **OCI:** Open Container Initiative (referring to Docker images)
*   **SLSA:** Supply-chain Levels for Software Artifacts (relevant for secure build practices)

## 2. System Overview
The CI/CD pipelines are a crucial part of the DFR operational infrastructure. They interact with source code repositories (`DFR_MOD_CORE_COMMON`, `DFR_MOD_FARMER_REGISTRY`, `DFR_MOBILE_APP`), testing repositories (`DFR_TEST_AUTOMATION`), and deployment script repositories (`DFR_DEPLOYMENT_SCRIPTS`). The primary goal is to automate the software delivery lifecycle, from code commit to deployment in various environments (Development, Staging, Production).

## 3. Design Considerations

### 3.1 Assumptions and Dependencies
*   Source code for Odoo modules and the mobile app resides in Git repositories accessible by the CI/CD platforms.
*   Deployment target environments (Staging, Production) are defined and accessible.
*   Docker registries are available for storing Odoo backend images.
*   App stores or private distribution channels are available for mobile app releases.
*   Credentials and secrets (e.g., API keys, deployment tokens, signing keys) are managed securely and accessible to the CI/CD pipelines (e.g., via GitHub Secrets, GitLab CI/CD variables, Jenkins Credentials).
*   SAST/DAST tools (SonarScanner, OWASP ZAP) are configured and accessible from CI/CD runners.
*   The `DFR_DEPLOYMENT_SCRIPTS` repository provides the necessary lower-level deployment scripts that `deploy_application.sh` might invoke.
*   The `DFR_TEST_AUTOMATION` repository provides test suites that `run_odoo_tests.sh` and mobile test jobs might invoke.

### 3.2 General Design
*   **Modularity:** Common tasks are encapsulated in reusable shell scripts. GitLab CI and Jenkins leverage templating/shared libraries.
*   **Parameterization:** Pipelines and scripts are parameterized to handle different environments, versions, and configurations.
*   **Security:**
    *   Secrets are managed securely using platform-specific features.
    *   SAST/DAST scans are integrated into pipelines.
    *   Principle of least privilege is applied to pipeline permissions.
*   **Idempotency:** Deployment scripts should be designed to be idempotent where possible.
*   **Error Handling:** Scripts and pipeline stages will implement robust error handling and provide clear failure messages.
*   **Notifications:** Pipelines should integrate notification mechanisms (e.g., email, Slack) for build/deployment status.
*   **Branching Strategy:** Pipelines will be triggered based on a defined branching strategy (e.g., GitFlow-like with `main`, `develop`, feature branches, release tags). Deployments to staging often from `develop` or `main`, and to production from release tags or `main`.
*   **Semantic Versioning:** Release tagging will follow Semantic Versioning 2.0.0 (e.g., `v1.0.0`). The `tag_git_release.sh` script facilitates this.

### 3.3 Technology Stack
*   **CI/CD Platforms:** GitHub Actions (primary), GitLab CI, Jenkins
*   **Scripting:** Shell (Bash 5.2.x), Groovy (for Jenkins shared libraries/pipelines)
*   **Workflow Definition:** YAML (for GitHub Actions, GitLab CI)
*   **Containerization:** Docker CLI 26.1.3
*   **Version Control:** Git 2.45.2
*   **SAST:** SonarScanner CLI 5.0.1.3006 (integrating with SonarQube/SonarCloud), Bandit (for Python)
*   **DAST:** OWASP ZAP 2.14.0
*   **Mobile Build Tools:** Android SDK, Gradle (for Android native/Flutter), Flutter SDK (if applicable)

## 4. Detailed Design Specifications

### 4.1 Common Utility Scripts (`dfr_operations/cicd_pipelines/scripts/common/`)

#### 4.1.1 `build_odoo_docker.sh`
*   **File Path:** `dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh`
*   **Description:** Shell script to build the DFR Odoo backend Docker image.
*   **Purpose:** Provides a reusable script to build the Docker image for the Odoo backend, ensuring consistency.
*   **Inputs/Parameters (Environment Variables or Arguments):**
    *   `DOCKER_IMAGE_NAME`: (Required) The name of the Docker image (e.g., `your-registry/dfr-odoo-backend`).
    *   `IMAGE_TAG`: (Required) The tag for the Docker image (e.g., `latest`, `v1.0.0`, commit SHA).
    *   `DOCKERFILE_PATH`: (Required) Path to the Dockerfile (e.g., `path/to/odoo_modules/Dockerfile`).
    *   `BUILD_CONTEXT`: (Required) The build context directory for the Docker build command (e.g., `path/to/odoo_modules`).
    *   `PUSH_IMAGE`: (Optional, boolean: `true`/`false`, default: `false`) Whether to push the image to a registry.
    *   `DOCKER_REGISTRY_URL`: (Optional) URL of the Docker registry. Required if `PUSH_IMAGE` is true.
    *   `DOCKER_USERNAME`: (Optional) Username for Docker registry login. Required if `PUSH_IMAGE` is true and registry requires auth.
    *   `DOCKER_PASSWORD`: (Optional, secret) Password for Docker registry login. Required if `PUSH_IMAGE` is true and registry requires auth.
    *   `BUILD_ARGS`: (Optional) String containing build arguments for Docker (e.g., "--build-arg KEY=VALUE").
*   **Key Logic/Operations:**
    1.  Validate required parameters.
    2.  Log in to Docker registry if `PUSH_IMAGE` is true and credentials are provided:
        bash
        echo "$DOCKER_PASSWORD" | docker login "$DOCKER_REGISTRY_URL" -u "$DOCKER_USERNAME" --password-stdin
        
    3.  Navigate to `BUILD_CONTEXT`.
    4.  Execute `docker build`:
        bash
        docker build $BUILD_ARGS -t "${DOCKER_IMAGE_NAME}:${IMAGE_TAG}" -f "${DOCKERFILE_PATH}" .
        
        *   Include standard labels like `org.opencontainers.image.source`, `org.opencontainers.image.revision`, `org.opencontainers.image.version`.
    5.  If `PUSH_IMAGE` is `true`:
        bash
        docker push "${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
        
*   **Outputs/Artifacts:** Locally built Docker image. Optionally, image pushed to a Docker registry.
*   **Error Handling:** Exit with a non-zero status code on failure (e.g., build failure, push failure). Log errors to `stderr`.
*   **Security Considerations:** Secure handling of `DOCKER_PASSWORD`.
*   **Implemented Features:** Docker Image Building (Odoo Backend)
*   **Requirement IDs:** `REQ-DIO-011`, `A.2.5`

#### 4.1.2 `run_odoo_tests.sh`
*   **File Path:** `dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh`
*   **Description:** Shell script to execute Odoo unit and/or integration tests.
*   **Purpose:** Standardizes the execution of Odoo tests within CI/CD pipelines.
*   **Inputs/Parameters (Environment Variables or Arguments):**
    *   `ODOO_DATABASE_NAME`: (Required) Name of the test database (e.g., `test_dfr_cicd`).
    *   `ODOO_MODULES_TO_TEST`: (Required) Comma-separated list of Odoo modules to test (e.g., `dfr_farmer_registry,dfr_dynamic_forms`). Can be `all` to test all DFR custom modules.
    *   `TEST_TYPE`: (Required, `unit` or `integration`) Specifies the type of tests to run.
    *   `ODOO_ADDONS_PATH`: (Required) Path to Odoo addons, including custom DFR modules and Odoo core addons.
    *   `ODOO_CONFIG_FILE`: (Optional) Path to an Odoo configuration file if needed.
    *   `DB_HOST`: (Optional, default: `localhost` or Docker service name) Database host.
    *   `DB_PORT`: (Optional, default: `5432`) Database port.
    *   `DB_USER`: (Optional, default: `odoo`) Database user.
    *   `DB_PASSWORD`: (Optional, secret, default: `odoo`) Database password.
*   **Key Logic/Operations:**
    1.  Validate required parameters.
    2.  Construct the Odoo test command.
        *   The command will likely be `odoo-bin`.
        *   `--test-enable` to enable test mode.
        *   `-d ${ODOO_DATABASE_NAME}` to specify the database.
        *   `-i ${ODOO_MODULES_TO_TEST}` to initialize/test specific modules.
        *   `--addons-path=${ODOO_ADDONS_PATH}`.
        *   `--stop-after-init` to run tests and exit.
        *   `--log-level=test` for appropriate logging.
        *   Potentially use `--test-tags` if Odoo tests are tagged by type (unit/integration).
        *   Example structure:
            bash
            odoo-bin \
                -d "${ODOO_DATABASE_NAME}" \
                -i "${ODOO_MODULES_TO_TEST}" \
                --addons-path="${ODOO_ADDONS_PATH}" \
                --test-enable \
                --stop-after-init \
                --log-level=test \
                --db_host="${DB_HOST}" \
                --db_port="${DB_PORT}" \
                --db_user="${DB_USER}" \
                --db_password="${DB_PASSWORD}"
                # Add --test-tags based on TEST_TYPE if available and used
            
    3.  Execute the Odoo test command.
    4.  Capture and report test results (exit code determines success/failure). Test output/logs should be available.
*   **Outputs/Artifacts:** Test execution logs. Exit code indicating test success or failure.
*   **Error Handling:** Exit with a non-zero status code if tests fail or the script encounters an error.
*   **Implemented Features:** Automated Unit Testing (Odoo Backend), Automated Integration Testing (Odoo Backend)
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-DIO-011`, `A.2.5`

#### 4.1.3 `deploy_application.sh`
*   **File Path:** `dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh`
*   **Description:** Generic shell script for deploying applications.
*   **Purpose:** Provides a common interface for application deployment logic, abstracting specific deployment tool commands.
*   **Inputs/Parameters (Environment Variables or Arguments):**
    *   `DEPLOYMENT_ENV`: (Required, e.g., `staging`, `production`) Target deployment environment.
    *   `APP_NAME`: (Required) Name of the application to deploy (e.g., `dfr-odoo-backend`, `dfr-mobile-app-distribution`).
    *   `IMAGE_TAG_OR_ARTIFACT_PATH`: (Required) Docker image tag (for containerized apps) or path to the deployment artifact (for mobile apps).
    *   `CONFIG_FILE_PATH`: (Optional) Path to an environment-specific configuration file (e.g., `docker-compose.yml`, Kubernetes manifest, deployment parameters).
    *   `DEPLOYMENT_TYPE`: (Required, e.g., `docker-compose`, `kubernetes`, `s3-upload`, `app-store-deploy`) Type of deployment.
    *   `KUBE_CONTEXT`: (Optional) Kubernetes context if `DEPLOYMENT_TYPE` is `kubernetes`.
    *   `AWS_PROFILE` / `GCP_PROJECT`: (Optional) Cloud provider credentials/profile.
*   **Key Logic/Operations:**
    1.  Validate required parameters.
    2.  Load environment-specific configurations from `CONFIG_FILE_PATH` if provided.
    3.  Execute deployment commands based on `DEPLOYMENT_TYPE`:
        *   **`docker-compose`:**
            bash
            docker-compose -f "${CONFIG_FILE_PATH}" pull # Ensure latest images referenced in compose file
            docker-compose -f "${CONFIG_FILE_PATH}" up -d --remove-orphans ${APP_NAME_SERVICE_IN_COMPOSE_IF_SPECIFIC}
            
        *   **`kubernetes`:**
            bash
            kubectl apply -f "${CONFIG_FILE_PATH}" --context "${KUBE_CONTEXT}"
            # May involve helm, kustomize, etc.
            
        *   **`s3-upload` (e.g., for static portal assets or mobile APKs):**
            bash
            aws s3 cp "${IMAGE_TAG_OR_ARTIFACT_PATH}" "s3://your-bucket/${DEPLOYMENT_ENV}/${APP_NAME}/" --profile "${AWS_PROFILE}"
            
        *   **`app-store-deploy` (conceptual, likely calls more specific tools like fastlane):**
            bash
            # fastlane deploy --env ${DEPLOYMENT_ENV} --apk ${IMAGE_TAG_OR_ARTIFACT_PATH}
            echo "Deploying ${APP_NAME} artifact ${IMAGE_TAG_OR_ARTIFACT_PATH} to ${DEPLOYMENT_ENV} app store track"
            
    4.  Perform basic post-deployment health checks (e.g., check if a service endpoint is responsive).
        bash
        # Example: curl -s -o /dev/null -w "%{http_code}" http://deployed-app-url
        
*   **Outputs/Artifacts:** Deployment status message.
*   **Error Handling:** Exit with a non-zero status code on deployment failure. Log errors.
*   **Implemented Features:** Deployment to Staging, Deployment to Production
*   **Requirement IDs:** `REQ-DIO-011`, `A.2.5`

#### 4.1.4 `tag_git_release.sh`
*   **File Path:** `dfr_operations/cicd_pipelines/scripts/common/tag_git_release.sh`
*   **Description:** Shell script to create and push a Git tag based on Semantic Versioning.
*   **Purpose:** Automates the process of tagging releases in Git according to Semantic Versioning principles.
*   **Inputs/Parameters (Environment Variables or Arguments):**
    *   `VERSION`: (Required) The semantic version string (e.g., `v1.2.3`). Must start with `v`.
    *   `GIT_REMOTE_NAME`: (Optional, default: `origin`) Name of the Git remote.
    *   `TAG_MESSAGE`: (Optional, default: `Release ${VERSION}`) Annotation message for the tag.
*   **Key Logic/Operations:**
    1.  Validate `VERSION` format (starts with `v`, follows SemVer pattern).
    2.  Create an annotated Git tag:
        bash
        git tag -a "${VERSION}" -m "${TAG_MESSAGE}"
        
    3.  Push the tag to the remote repository:
        bash
        git push "${GIT_REMOTE_NAME}" "${VERSION}"
        
*   **Outputs/Artifacts:** Git tag created and pushed to the remote repository.
*   **Error Handling:** Exit with a non-zero status code if Git commands fail.
*   **Implemented Features:** Semantic Versioning and Tagging
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-CM-002`, `A.2.5`

### 4.2 GitHub Actions Workflows (`dfr_operations/cicd_pipelines/github_actions/workflows/`)

#### 4.2.1 `dfr_odoo_backend_pipeline.yml`
*   **File Path:** `dfr_operations/cicd_pipelines/github_actions/workflows/dfr_odoo_backend_pipeline.yml`
*   **Description:** GitHub Actions workflow for the DFR Odoo backend.
*   **Purpose:** Defines the end-to-end CI/CD pipeline for DFR Odoo backend components.
*   **Triggers:**
    *   `push`: to `main` branch, `develop` branch, and tags matching `v*.*.*`.
    *   `pull_request`: targeting `main` or `develop` branches.
    *   `workflow_dispatch`: for manual runs.
*   **Environment Variables / Secrets:**
    *   `DOCKER_USERNAME`, `DOCKER_PASSWORD`: For Docker registry login (stored as GitHub secrets).
    *   `SONAR_TOKEN`, `SONAR_HOST_URL`: For SonarQube/SonarCloud integration (secrets).
    *   `ZAP_API_KEY`, `ZAP_TARGET_URL_STAGING`: For OWASP ZAP DAST scans (secrets, variables).
    *   `STAGING_DEPLOY_KEY`, `PRODUCTION_DEPLOY_KEY`: SSH keys or tokens for deployment (secrets).
    *   `ODOO_MASTER_PASSWORD_STAGING`, `ODOO_MASTER_PASSWORD_PRODUCTION`: (secrets).
    *   `DB_USER_STAGING`, `DB_PASSWORD_STAGING`, `DB_HOST_STAGING`, etc. for staging deployment.
    *   `DB_USER_PRODUCTION`, `DB_PASSWORD_PRODUCTION`, `DB_HOST_PRODUCTION`, etc. for production deployment.
    *   Feature Toggles (from repository config): `ENABLE_SAST_SCANS_PER_COMMIT`, `ENABLE_DAST_SCANS_PER_BUILD`, etc.
*   **Jobs:**
    1.  **`lint_code`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Steps:**
            *   Checkout code: `actions/checkout@v4`
            *   Setup Python.
            *   Install linting tools (e.g., `flake8`, `pylint`, `black --check`).
            *   Run linters on Odoo module paths.
    2.  **`unit_test_odoo`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Services:** `postgres:14-alpine` (with appropriate env vars for user/pass/db).
        *   **Steps:**
            *   Checkout code.
            *   Setup Python and Odoo dependencies.
            *   Execute `scripts/common/run_odoo_tests.sh` with `TEST_TYPE=unit`.
            *   Upload test results/coverage reports as artifacts.
    3.  **`integration_test_odoo`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Services:** `postgres:14-alpine`.
        *   **Steps:**
            *   Checkout code.
            *   Setup Python and Odoo dependencies.
            *   Execute `scripts/common/run_odoo_tests.sh` with `TEST_TYPE=integration`.
            *   Upload test results/coverage reports as artifacts.
    4.  **`sast_scan_sonar`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Conditional:** `if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop') && env.ENABLE_SAST_SCANS_PER_COMMIT == 'true'`
        *   **Steps:**
            *   Checkout code.
            *   Setup Java (for SonarScanner).
            *   Download and setup SonarScanner CLI.
            *   Run SonarScanner:
                bash
                sonar-scanner \
                  -Dsonar.projectKey=dfr_odoo_backend \
                  -Dsonar.sources=./dfr_addons \ # Adjust path
                  -Dsonar.host.url=${{ secrets.SONAR_HOST_URL }} \
                  -Dsonar.login=${{ secrets.SONAR_TOKEN }}
                
    5.  **`build_and_push_docker`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `lint_code`, `unit_test_odoo`, `integration_test_odoo` (conditionally `sast_scan_sonar` if it's a blocking check).
        *   **Conditional:** `if: success() && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop' || startsWith(github.ref, 'refs/tags/v'))`
        *   **Steps:**
            *   Checkout code.
            *   Set image tag (e.g., `develop` for develop branch, `main` or commit SHA for main, Git tag for tags).
            *   Login to Docker Registry using secrets.
            *   Execute `scripts/common/build_odoo_docker.sh` with `PUSH_IMAGE=true`.
    6.  **`dast_scan_zap`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `build_and_push_docker` (if scanning a deployed instance of the new image) or a separate deployment job for a temporary scan environment.
        *   **Conditional:** `if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop') && env.ENABLE_DAST_SCANS_PER_BUILD == 'true'`
        *   **Steps:**
            *   Deploy the application to a temporary staging/scan environment if not already deployed.
            *   Run OWASP ZAP scan (e.g., using ZAP Docker image, baseline scan or full scan against `ZAP_TARGET_URL_STAGING`).
                bash
                docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
                  -t $ZAP_TARGET_URL_STAGING -g gen.conf -r zap_report.html
                # Or use ZAP GitHub Action
                
            *   Upload ZAP report as an artifact.
    7.  **`deploy_staging`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `build_and_push_docker` (and potentially `dast_scan_zap` if it's a gate).
        *   **Environment:** `staging` (GitHub environment with protection rules and secrets).
        *   **Conditional:** `if: success() && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop') && env.AUTO_DEPLOY_TO_STAGING_ON_MAIN_MERGE == 'true'` (adjust branch logic as needed, e.g., `develop` deploys to staging).
        *   **Steps:**
            *   Checkout code (for deployment scripts/configs if not in image).
            *   Setup deployment tools (e.g., `docker-compose`, `kubectl`).
            *   Execute `scripts/common/deploy_application.sh` with staging environment parameters, image tag from `build_and_push_docker` job, and staging config files.
    8.  **`deploy_production`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `deploy_staging`.
        *   **Environment:** `production` (GitHub environment with protection rules, required reviewers, and secrets).
        *   **Conditional:** `if: success() && startsWith(github.ref, 'refs/tags/v') && env.REQUIRE_MANUAL_APPROVAL_FOR_PRODUCTION_DEPLOYMENT == 'true'` (or use GitHub Environments approval).
        *   **Steps:**
            *   (Manual approval step if not handled by GitHub Environments).
            *   Checkout code.
            *   Setup deployment tools.
            *   Execute `scripts/common/tag_git_release.sh` (if tagging is done at deployment, otherwise tag should trigger this).
            *   Execute `scripts/common/deploy_application.sh` with production environment parameters, image tag (from Git tag), and production config files.
*   **Implemented Features:** Automated Build (Odoo Backend), Automated Testing (Odoo Backend), Docker Image Packaging, SAST/DAST Integration, Deployment to Staging, Deployment to Production, Semantic Versioning Integration.
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-DIO-011`, `REQ-CM-002`, `A.2.5`.

#### 4.2.2 `dfr_mobile_app_pipeline.yml`
*   **File Path:** `dfr_operations/cicd_pipelines/github_actions/workflows/dfr_mobile_app_pipeline.yml`
*   **Description:** GitHub Actions workflow for the DFR Android Mobile App.
*   **Purpose:** Defines the end-to-end CI/CD pipeline for the DFR Android Mobile App.
*   **Triggers:**
    *   `push`: to `main` branch, `develop` branch, and tags matching `v*.*.*`.
    *   `pull_request`: targeting `main` or `develop` branches.
    *   `workflow_dispatch`: for manual runs.
*   **Environment Variables / Secrets:**
    *   `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD`: For signing release builds (secrets).
    *   Base64 encoded Keystore file (secret).
    *   `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON`: For deploying to Google Play Console (secret).
    *   `SONAR_TOKEN_MOBILE`, `SONAR_HOST_URL_MOBILE`: For SonarQube/SonarCloud (secrets).
    *   `MOBSF_API_KEY`, `MOBSF_SERVER_URL`: For MobSF integration (secrets, variables).
*   **Jobs:**
    1.  **`lint_and_static_analysis_mobile`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Steps:**
            *   Checkout code.
            *   Setup Java and Android SDK / Flutter SDK.
            *   Run linters (e.g., `ktlint`, Android Lint, `flutter analyze`).
            *   (Optional SAST if not combined) Run SAST (e.g., SonarScanner for Kotlin/Java/Dart, MobSF static analysis upload).
    2.  **`unit_tests_mobile`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Steps:**
            *   Checkout code.
            *   Setup Java and Android SDK / Flutter SDK.
            *   Run unit tests (e.g., `./gradlew testDebugUnitTest` or `flutter test`).
            *   Upload test results/coverage.
    3.  **`integration_widget_tests_mobile`**:
        *   **Runs-on:** `ubuntu-latest` (or `macos-latest` if iOS testing is needed for Flutter)
        *   **Steps:**
            *   Checkout code.
            *   Setup Java and Android SDK / Flutter SDK.
            *   Start Android emulator (if needed for instrumentation tests).
            *   Run integration/widget tests (e.g., `./gradlew connectedDebugAndroidTest` or `flutter test integration_test`).
            *   Upload test results.
    4.  **`build_mobile_app`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `lint_and_static_analysis_mobile`, `unit_tests_mobile`, `integration_widget_tests_mobile`.
        *   **Conditional:** `if: success() && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop' || startsWith(github.ref, 'refs/tags/v'))`
        *   **Steps:**
            *   Checkout code.
            *   Setup Java and Android SDK / Flutter SDK.
            *   Decode and setup signing keystore from secrets.
            *   Build release APK/AAB (e.g., `./gradlew assembleRelease bundleRelease` or `flutter build apk --release --split-per-abi && flutter build appbundle --release`).
            *   Set version name/code based on Git tag or build number.
            *   Archive APK/AAB artifacts.
    5.  **`security_scan_mobile_artifact`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `build_mobile_app`.
        *   **Conditional:** `if: success() && env.ENABLE_DAST_SCANS_PER_BUILD == 'true'` (Note: DAST for mobile is more complex; this might be a static analysis of the built artifact or a simplified dynamic scan).
        *   **Steps:**
            *   Download APK/AAB artifact.
            *   Run security scan (e.g., upload to MobSF for analysis).
            *   Upload scan report.
    6.  **`deploy_to_test_track_google_play`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `build_mobile_app` (and potentially `security_scan_mobile_artifact`).
        *   **Environment:** `mobile_staging` (GitHub environment).
        *   **Conditional:** `if: success() && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')`
        *   **Steps:**
            *   Download AAB artifact.
            *   Setup `fastlane` or use GitHub Actions for Google Play (e.g., `r0adkll/upload-google-play`).
            *   Upload AAB to an internal, alpha, or beta track in Google Play Console using service account JSON.
    7.  **`deploy_to_production_store_google_play`**:
        *   **Runs-on:** `ubuntu-latest`
        *   **Needs:** `deploy_to_test_track_google_play`.
        *   **Environment:** `mobile_production` (GitHub environment).
        *   **Conditional:** `if: success() && startsWith(github.ref, 'refs/tags/v')`
        *   **Steps:**
            *   (Manual approval step if needed).
            *   Promote build from test track to production or upload AAB directly to production track in Google Play Console.
            *   Optionally, call `scripts/common/tag_git_release.sh` if not already done.
*   **Implemented Features:** Automated Build (Mobile App), Automated Testing (Mobile App), Mobile App Packaging (APK/AAB), SAST/DAST Integration, Distribution to Test Tracks/Store, Semantic Versioning Integration.
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-DIO-011`, `REQ-CM-002`, `A.2.5`.

### 4.3 GitLab CI Definitions (`dfr_operations/cicd_pipelines/gitlab_ci/`)

#### 4.3.1 `.gitlab-ci.yml`
*   **File Path:** `dfr_operations/cicd_pipelines/gitlab_ci/.gitlab-ci.yml`
*   **Description:** Main GitLab CI pipeline configuration file.
*   **Purpose:** Defines all CI/CD stages and jobs for the DFR project within GitLab CI.
*   **Structure:**
    *   **`stages`**: `validate`, `test`, `build`, `scan`, `deploy_staging`, `deploy_production`.
    *   **`variables`**: Global variables like Docker image names, registry paths. Values often from GitLab CI/CD project/group variables.
        *   `DOCKER_IMAGE_NAME_ODOO`: `"$CI_REGISTRY_IMAGE/dfr-odoo-backend"`
        *   `DOCKER_IMAGE_NAME_MOBILE`: `"$CI_REGISTRY_IMAGE/dfr-mobile-app"`
        *   `SONAR_HOST_URL`, `SONAR_PROJECT_KEY_ODOO`, `SONAR_PROJECT_KEY_MOBILE`
        *   Environment-specific variables (e.g., `STAGING_KUBE_CONFIG`, `PROD_KUBE_CONFIG`) defined in GitLab CI/CD settings.
    *   **`include`**:
        *   `'/gitlab_ci/templates/odoo_jobs.yml'`
        *   `'/gitlab_ci/templates/mobile_jobs.yml'` (Assumed similar structure to odoo_jobs.yml but for mobile)
        *   `'/gitlab_ci/templates/common_jobs.yml'` (Assumed for common tasks like tagging or notifications)
    *   **`workflow:rules`**: Controls pipeline execution based on commit branch, tags, or event type (merge requests).
        *   Example: Run on `main`, `develop`, tags (`v*.*.*`), and merge requests.
*   **Job Definitions:**
    *   Jobs will extend templates from included files.
    *   Jobs will be assigned to appropriate stages.
    *   `rules` or `only/except` clauses will control job execution (e.g., deploy to production only on tags).
    *   Secrets and protected variables from GitLab CI/CD settings will be used for sensitive operations.
    *   **Example Job using template (Odoo lint):**
        yaml
        lint_odoo_code:
          extends: .odoo_lint_template # Defined in odoo_jobs.yml
          # No specific script needed here as it's in the template
        
    *   **Example Deployment Job (Odoo Staging):**
        yaml
        deploy_odoo_to_staging:
          extends: .deploy_application_template # Assumed in common_jobs.yml or odoo_jobs.yml
          stage: deploy_staging
          environment:
            name: staging/odoo-backend
            url: http://staging-dfr.example.com
          variables:
            DEPLOYMENT_ENV: staging
            APP_NAME: dfr-odoo-backend
            IMAGE_TAG: "$CI_COMMIT_SHA" # Or from a build job artifact
            CONFIG_FILE_PATH: "path/to/staging-docker-compose.yml" # Or k8s manifests
            DEPLOYMENT_TYPE: "docker-compose" # Or "kubernetes"
          script:
            - dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh # Called by template or directly
          rules:
            - if: '$CI_COMMIT_BRANCH == "develop"'
        
*   **Implemented Features:** Centralized CI/CD Orchestration, Automated Build (Odoo & Mobile), Automated Testing, Deployment Automation.
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-DIO-011`, `REQ-CM-002`, `A.2.5`.

#### 4.3.2 `gitlab_ci/templates/odoo_jobs.yml`
*   **File Path:** `dfr_operations/cicd_pipelines/gitlab_ci/templates/odoo_jobs.yml`
*   **Description:** GitLab CI template for DFR Odoo backend jobs.
*   **Purpose:** Provides standardized, reusable job definitions for Odoo CI/CD.
*   **Templates Defined:**
    *   **`.odoo_lint_template`**:
        *   `stage: validate`
        *   `image: python:3.9-slim` (or a custom image with tools)
        *   `script`:
            *   `pip install flake8`
            *   `flake8 path/to/dfr_addons/`
    *   **`.odoo_unit_test_template`**:
        *   `stage: test`
        *   `image: appropriate_odoo_test_image` (might need to be built in a prior step or a pre-built image with Odoo and dependencies)
        *   `services: - name: postgres:14-alpine alias: db`
        *   `variables`: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
        *   `before_script`: (Optional) Wait for PostgreSQL to be ready.
        *   `script`:
            *   `dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh --addons-path=./dfr_addons:/usr/lib/python3/dist-packages/odoo/addons --db_host=db --test-type=unit --modules-to-test=dfr_common,dfr_farmer_registry` (adjust paths and modules)
    *   **`.odoo_integration_test_template`**: Similar to unit test template but calls `run_odoo_tests.sh` with `TEST_TYPE=integration`.
    *   **`.build_odoo_docker_template`**:
        *   `stage: build`
        *   `image: docker:20.10.16`
        *   `services: - docker:20.10.16-dind`
        *   `variables`: `DOCKER_TLS_CERTDIR: "/certs"`
        *   `before_script`:
            *   `docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY`
        *   `script`:
            *   `IMAGE_TAG_VALUE=${CI_COMMIT_TAG:-$CI_COMMIT_SHA}`
            *   `dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh --docker-image-name "$DOCKER_IMAGE_NAME_ODOO" --image-tag "$IMAGE_TAG_VALUE" --dockerfile-path path/to/Dockerfile_odoo --build-context . --push-image true --docker-registry-url $CI_REGISTRY`
    *   **`.sast_sonar_odoo_template`**:
        *   `stage: scan`
        *   `image: sonarsource/sonar-scanner-cli:5.0`
        *   `variables`: `SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"`
        *   `cache: paths: - .sonar/cache`
        *   `script`:
            *   `sonar-scanner -Dsonar.projectKey=$SONAR_PROJECT_KEY_ODOO -Dsonar.sources=./dfr_addons -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.login=$SONAR_TOKEN`
    *   **`.dast_zap_odoo_template`**:
        *   `stage: scan`
        *   `image: owasp/zap2docker-stable`
        *   `variables`: `ZAP_TARGET_URL: $STAGING_APP_URL` (from deployment job or GitLab env var)
        *   `script`:
            *   `zap-baseline.py -t $ZAP_TARGET_URL -r zap_report.html`
            *   (Needs deployed instance)
        *   `artifacts: paths: [zap_report.html]`
*   **Implemented Features:** Reusable Odoo CI Jobs
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-DIO-011`

#### 4.3.3 `gitlab_ci/templates/mobile_jobs.yml` (Conceptual)
*   **File Path:** `dfr_operations/cicd_pipelines/gitlab_ci/templates/mobile_jobs.yml`
*   **Description:** GitLab CI template file containing reusable job definitions for DFR Android Mobile App CI/CD stages.
*   **Purpose:** Standardizes job definitions for mobile app CI/CD tasks.
*   **Templates (Conceptual):**
    *   `.mobile_lint_template` (Android Lint, ktlint, Flutter analyze)
    *   `.mobile_unit_test_template` (JUnit, Flutter unit tests)
    *   `.mobile_integration_test_template` (Espresso, Flutter integration tests, possibly with emulators)
    *   `.build_mobile_apk_aab_template` (Gradle build, Flutter build, signing)
    *   `.deploy_mobile_test_track_template` (fastlane, Google Play Publisher API)
    *   `.sast_mobfs_mobile_template` (MobSF static scan)
*   **Note:** Specifics depend on native Android vs. Flutter choice.

#### 4.3.4 `gitlab_ci/templates/common_jobs.yml` (Conceptual)
*   **File Path:** `dfr_operations/cicd_pipelines/gitlab_ci/templates/common_jobs.yml`
*   **Description:** GitLab CI template for common jobs like deployment or tagging.
*   **Purpose:** Provides reusable job definitions applicable to multiple components.
*   **Templates (Conceptual):**
    *   **`.deploy_application_template`**:
        *   `stage: deploy_staging` or `deploy_production`
        *   `image: appropriate_deploy_image` (e.g., with `docker-compose` or `kubectl`)
        *   `variables`: `DEPLOYMENT_ENV`, `APP_NAME`, `IMAGE_TAG`, `CONFIG_FILE_PATH`, `DEPLOYMENT_TYPE`.
        *   `script`:
            *   `dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh`
    *   **`.tag_git_release_template`**:
        *   `stage: deploy_production` (or a dedicated release stage)
        *   `image: alpine/git:latest`
        *   `script`:
            *   `dfr_operations/cicd_pipelines/scripts/common/tag_git_release.sh --version $CI_COMMIT_TAG --remote-name origin`
        *   `rules`:
            *   `- if: '$CI_COMMIT_TAG'`

### 4.4 Jenkins Pipeline Definitions (`dfr_operations/cicd_pipelines/jenkins/`)

#### 4.4.1 `pipelines/dfr_odoo_backend.Jenkinsfile`
*   **File Path:** `dfr_operations/cicd_pipelines/jenkins/pipelines/dfr_odoo_backend.Jenkinsfile`
*   **Description:** Jenkinsfile (declarative pipeline) for DFR Odoo backend CI/CD.
*   **Purpose:** Manages the CI/CD lifecycle for DFR Odoo backend components using Jenkins.
*   **Pipeline Structure (Declarative):**
    *   **`agent`**: `any` or a specific label for agents with Docker, Python.
    *   **`environment`**: Define global environment variables.
        *   `DOCKER_CREDENTIALS_ID = 'your-jenkins-docker-secret-id'`
        *   `ODOO_REPO_URL = 'your-git-repo-url'`
        *   `SONAR_CREDENTIALS_ID = 'your-jenkins-sonar-token-id'`
        *   `SONAR_HOST_URL = 'your-sonar-host-url'`
        *   `STAGING_DEPLOY_CREDENTIALS_ID`, `PROD_DEPLOY_CREDENTIALS_ID`
    *   **`tools`**: (If needed, e.g., `jdk 'AdoptOpenJDK 11'`, `maven 'Maven 3'`)
    *   **`stages`**:
        1.  **`Checkout`**:
            *   `git branch: env.BRANCH_NAME ?: 'main', url: ODOO_REPO_URL`
        2.  **`Lint Code`**:
            *   `sh 'flake8 path/to/dfr_addons/'`
        3.  **`Unit Tests (Odoo)`**:
            *   (Requires Docker agent or pre-configured Odoo test environment with PostgreSQL)
            *   `sh 'dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh --test-type=unit ...'`
        4.  **`Integration Tests (Odoo)`**:
            *   (Similar setup to Unit Tests)
            *   `sh 'dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh --test-type=integration ...'`
        5.  **`SAST Scan (SonarQube)`**:
            *   `when { expression { return env.ENABLE_SAST_SCANS_PER_COMMIT == 'true' && (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'develop') } }`
            *   `withCredentials([string(credentialsId: SONAR_CREDENTIALS_ID, variable: 'SONAR_TOKEN_VALUE')]) { sh "sonar-scanner -Dsonar.login=${SONAR_TOKEN_VALUE} ..." }`
        6.  **`Build Docker Image`**:
            *   `script {`
                *   `def imageName = "your-registry/dfr-odoo-backend:${env.BRANCH_NAME == 'main' ? env.TAG_NAME ?: env.BUILD_ID : env.BUILD_ID}"` // Complex tagging logic
                *   `def imageTag = env.BRANCH_NAME == 'main' ? (env.TAG_NAME ?: 'latest') : (env.BRANCH_NAME.replace('/', '-') + '-' + env.BUILD_ID)`
                *   `sh "dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh --docker-image-name your-registry/dfr-odoo-backend --image-tag ${imageTag} --dockerfile-path Dockerfile_odoo --build-context . --push-image true --docker-registry-url your-registry-url"` (Uses credentials from Jenkins `withCredentials`)
            *   `}`
        7.  **`DAST Scan (OWASP ZAP)`**:
            *   `when { expression { return env.ENABLE_DAST_SCANS_PER_BUILD == 'true' && (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'develop') } }`
            *   (Deploy to temp env, then run ZAP against it)
            *   `archiveArtifacts artifacts: 'zap_report.html', fingerprint: true`
        8.  **`Deploy to Staging`**:
            *   `when { branch 'develop' ; or branch 'main' if AUTO_DEPLOY_TO_STAGING_ON_MAIN_MERGE == 'true' }`
            *   `input message: 'Approve deployment to Staging?'` (if manual approval needed)
            *   `withCredentials(...) { sh "dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh --deployment-env staging --app-name dfr-odoo-backend --image-tag-or-artifact-path ${imageTagFromBuild} --config-file-path path/to/staging-config.yml --deployment-type docker-compose" }`
        9.  **`Deploy to Production`**:
            *   `when { tag 'v*.*.*' ; or (branch 'main' if not deploying from tags) }`
            *   `input message: 'CRITICAL: Approve deployment to Production?'`
            *   `script { if (env.TAG_NAME) { sh "dfr_operations/cicd_pipelines/scripts/common/tag_git_release.sh --version ${env.TAG_NAME}" } }` (Tagging might be manual or a separate job that triggers this)
            *   `withCredentials(...) { sh "dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh --deployment-env production --app-name dfr-odoo-backend --image-tag-or-artifact-path ${imageTagFromBuildOrTag} --config-file-path path/to/prod-config.yml --deployment-type docker-compose" }`
    *   **`post` block**: For notifications, cleanup.
*   **Implemented Features:** Automated Build (Odoo Backend), Automated Testing (Odoo Backend), Docker Image Packaging, Deployment Automation.
*   **Requirement IDs:** `REQ-PCA-013`, `REQ-DIO-011`, `REQ-CM-002`, `A.2.5`.

#### 4.4.2 `jenkins/pipelines/dfr_mobile_app.Jenkinsfile` (Conceptual)
*   **File Path:** `dfr_operations/cicd_pipelines/jenkins/pipelines/dfr_mobile_app.Jenkinsfile`
*   **Description:** Jenkinsfile for DFR Android Mobile App CI/CD.
*   **Purpose:** Manages the CI/CD lifecycle for the DFR Android Mobile App using Jenkins.
*   **Pipeline Structure (Conceptual, similar to Odoo backend but with mobile-specific stages):**
    *   Checkout
    *   Lint & Static Analysis (Android Lint, ktlint/Flutter analyze, SonarScanner for mobile, MobSF static)
    *   Unit Tests (JUnit/Flutter tests)
    *   Integration/Widget Tests (Espresso/Flutter integration_test, potentially with Android Emulator plugin)
    *   Build App (Gradle/Flutter build APK/AAB, signing with Jenkins credentials for keystore)
    *   Security Scan Artifact (MobSF on APK/AAB)
    *   Deploy to Test Track (Google Play Publisher plugin or fastlane)
    *   Deploy to Production Store (Google Play Publisher plugin or fastlane, with manual approval)

#### 4.4.3 `jenkins/vars/dfrPipelineUtils.groovy`
*   **File Path:** `dfr_operations/cicd_pipelines/jenkins/vars/dfrPipelineUtils.groovy`
*   **Description:** Shared Groovy script for Jenkins pipelines.
*   **Purpose:** Provides utility functions to simplify and standardize Jenkins pipeline definitions.
*   **Functions:**
    *   `notifyBuildStatus(String buildResult, String recipientList, String customMessage = "")`:
        *   **Logic:** Sends an email notification about the build status. Uses Jenkins `mail` step.
        *   **Parameters:**
            *   `buildResult`: Typically `currentBuild.currentResult` (e.g., 'SUCCESS', 'FAILURE').
            *   `recipientList`: Comma-separated string of email addresses.
            *   `customMessage`: Optional additional message content.
    *   `performSastScan(Map config)`:
        *   **Logic:** Executes a SAST scan using a configured tool. Abstracted to allow different tools.
        *   **Parameters (Map `config`):**
            *   `toolName`: (String) e.g., 'sonar', 'bandit'.
            *   `projectKey`: (String) Project identifier for the SAST tool.
            *   `sourcesPath`: (String) Path to source code.
            *   `sonarHostUrl`: (String, optional, for Sonar) SonarQube server URL.
            *   `sonarLoginToken`: (String, optional, secret, for Sonar) SonarQube token.
        *   **Example call:** `dfrPipelineUtils.performSastScan toolName: 'sonar', projectKey: 'dfr_odoo', sourcesPath: './dfr_addons', sonarHostUrl: env.SONAR_HOST_URL, sonarLoginToken: env.SONAR_TOKEN_VALUE`
    *   `runCustomDeploymentStep(String environment, String appName, String scriptPath)`:
        *   **Logic:** Executes a custom deployment script.
        *   **Parameters:**
            *   `environment`: Target environment (e.g., 'staging').
            *   `appName`: Application name.
            *   `scriptPath`: Path to the custom deployment script.
*   **Implemented Features:** Reusable Jenkins Pipeline Logic
*   **Requirement IDs:** `REQ-DIO-011`

## 5. Configuration Management
*   **Pipeline Feature Toggles:** As defined in repository configuration (`ENABLE_SAST_SCANS_PER_COMMIT`, etc.). These will be passed as environment variables to the pipelines or used in conditional logic within pipeline definitions.
*   **Database Configurations:** Staging/Production DB connection details (`STAGING_DB_HOST_PIPELINE_VAR`, etc.) will be managed as secrets/protected variables within the respective CI/CD platforms and accessed by deployment scripts/stages.
*   **Secrets Management:**
    *   **GitHub Actions:** Use GitHub Encrypted Secrets for API keys, passwords, tokens.
    *   **GitLab CI:** Use GitLab CI/CD Variables (masked and protected) for sensitive data.
    *   **Jenkins:** Use Jenkins Credentials Plugin for storing and injecting secrets.
*   **Environment-Specific Configurations:** Deployment scripts (`deploy_application.sh`) will accept paths to environment-specific configuration files (e.g., `docker-compose.staging.yml`, `k8s-manifests/prod/`). These files are expected to be version-controlled in the `DFR_DEPLOYMENT_SCRIPTS` repository or a dedicated configuration repository.

## 6. Integration Points
*   **Source Code Repositories:** DFR Odoo modules, DFR Mobile App. Pipelines will checkout code from these.
*   **Docker Registry:** (e.g., Docker Hub, GitHub Container Registry, GitLab Container Registry, AWS ECR). Pipelines will push and pull Docker images.
*   **SAST Tools:** SonarQube/SonarCloud, Bandit. Pipelines will execute scanners and potentially upload results.
*   **DAST Tools:** OWASP ZAP. Pipelines will orchestrate scans against deployed test instances.
*   **Deployment Targets:** Staging and Production environments (could be VMs, Kubernetes clusters, Cloud PaaS).
*   **Mobile App Stores/Distribution:** Google Play Console (for test tracks and production).
*   **Notification Services:** Email, Slack (or other chatops tools) for pipeline status updates.

## 7. Error Handling and Logging
*   All scripts will use `set -e` and `set -o pipefail` (or equivalent) to ensure errors cause script termination.
*   Pipeline stages will fail upon non-zero exit codes from scripts.
*   CI/CD platforms provide detailed logging for each job and step.
*   Error messages from tools (linters, testers, scanners, deployment tools) will be captured in CI/CD logs.
*   Notifications will be sent for pipeline failures.

## 8. Scalability and Performance
*   CI/CD infrastructure (runners/agents) should be scalable to handle concurrent builds.
*   Pipeline efficiency will be monitored, optimizing long-running jobs (e.g., through caching, parallelization).

## 9. Testing of Pipelines
*   Pipelines will be tested by triggering them on feature branches and pull requests.
*   Deployment to staging will serve as a key validation point before production deployment.
*   Manual triggers (`workflow_dispatch`) will allow for on-demand testing of specific pipeline configurations.

## 10. Documentation
*   This SDS document.
*   README files within subdirectories (`github_actions/`, `gitlab_ci/`, `jenkins/`, `scripts/`) explaining the purpose and usage of the pipelines and scripts.
*   Comments within pipeline definition files (YAML, Groovy) and shell scripts.
*   Documentation on how to configure pipeline variables and secrets for each CI/CD platform.
*   As per `REQ-CM-014`, CI/CD pipeline logic and configuration will be part of the overall technical documentation.