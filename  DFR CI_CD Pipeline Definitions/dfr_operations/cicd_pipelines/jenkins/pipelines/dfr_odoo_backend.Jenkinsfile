// Declarative Pipeline for DFR Odoo Backend

pipeline {
    agent any // Or specify a label: agent { label 'docker-python-agent' }

    environment {
        // CI/CD Platform & Tool Configuration
        DOCKER_CREDENTIALS_ID = 'jenkins-docker-registry-credentials' // Jenkins credential ID for Docker registry
        SONAR_CREDENTIALS_ID = 'jenkins-sonarqube-token' // Jenkins credential ID for SonarQube token
        SONAR_HOST_URL = 'https://your-sonarqube-instance.com' // Your SonarQube server URL
        ODOO_REPO_URL = 'https://github.com/your-org/your-dfr-odoo-repo.git' // Your Odoo modules Git repository

        // Application Specific Configuration
        DOCKER_IMAGE_REGISTRY = 'your-docker-registry.com' // E.g., docker.io, ghcr.io
        DOCKER_IMAGE_BASE_NAME = 'dfr-odoo-backend'
        ODOO_MODULES_PATH = 'dfr_addons' // Relative path to Odoo modules in the checked-out code
        PYTHON_LINT_TARGET_PATH = "${env.ODOO_MODULES_PATH}"
        DOCKERFILE_PATH = 'Dockerfile_odoo' // Relative path to the Dockerfile
        BUILD_CONTEXT = '.'

        // Test Configuration
        ODOO_TEST_DB_PREFIX = 'test_dfr_jenkins'
        ODOO_MODULES_TO_TEST_UNIT = 'dfr_farmer_registry,dfr_dynamic_forms' // Comma-separated
        ODOO_MODULES_TO_TEST_INTEGRATION = 'all'
        ODOO_ADDONS_PATH_CI = "${env.ODOO_MODULES_PATH}:/usr/lib/python3/dist-packages/odoo/addons" // Adjust Odoo core addons path for test env

        // Deployment Configuration (placeholders, manage actual values via Jenkins credentials or config files)
        STAGING_CONFIG_FILE_PATH = 'dfr_deployment_scripts/odoo/staging/docker-compose.yml'
        PRODUCTION_CONFIG_FILE_PATH = 'dfr_deployment_scripts/odoo/production/docker-compose.yml'
        STAGING_DEPLOY_CREDENTIALS_ID = 'jenkins-staging-deploy-credentials'
        PROD_DEPLOY_CREDENTIALS_ID = 'jenkins-production-deploy-credentials'
        ZAP_TARGET_URL_STAGING = 'http://staging-dfr-odoo.example.com' // Example, replace with actual

        // Feature Toggles (can be boolean parameters for the Jenkins job)
        ENABLE_SAST_SCANS_PER_COMMIT = true
        ENABLE_DAST_SCANS_PER_BUILD = true
        AUTO_DEPLOY_TO_STAGING_ON_MAIN_MERGE = true // True for develop, false for main typically
        REQUIRE_MANUAL_APPROVAL_FOR_PRODUCTION_DEPLOYMENT = true
    }

    tools {
        // If specific JDK or Maven versions are needed by SonarScanner or other tools
        // jdk 'AdoptOpenJDK 17'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: env.BRANCH_NAME ?: 'main']], // BRANCH_NAME is typically set by Jenkins
                    userRemoteConfigs: [[url: ODOO_REPO_URL]]
                ])
                script {
                    // Set a dynamic image tag for the current build
                    if (env.TAG_NAME) { // If it's a tag build (e.g., v1.0.0)
                        env.IMAGE_TAG = env.TAG_NAME
                    } else if (env.BRANCH_NAME == 'main') {
                        env.IMAGE_TAG = "main-${env.BUILD_ID}"
                    } else if (env.BRANCH_NAME == 'develop') {
                        env.IMAGE_TAG = "develop-${env.BUILD_ID}"
                    } else { // Feature branches
                        env.IMAGE_TAG = "${env.BRANCH_NAME.replace('/', '-')}-${env.BUILD_ID}"
                    }
                    env.FULL_DOCKER_IMAGE_NAME = "${DOCKER_IMAGE_REGISTRY}/${DOCKER_IMAGE_BASE_NAME}"
                    echo "Calculated Image Tag: ${env.IMAGE_TAG}"
                    echo "Full Docker Image Name with Tag: ${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}"
                }
            }
        }

        stage('Lint Code') {
            steps {
                echo "Running Linters..."
                // Example using flake8. Add other linters as needed.
                // Ensure the agent has Python and linters installed or use a Dockerized linter.
                sh "pip install flake8 bandit" // Or install globally on agent / use virtualenv
                sh "flake8 ${env.PYTHON_LINT_TARGET_PATH}"
                sh "bandit -r ${env.PYTHON_LINT_TARGET_PATH} -f html -o bandit_report.html"
                archiveArtifacts artifacts: 'bandit_report.html', fingerprint: true
            }
        }

        stage('Unit Tests (Odoo)') {
            // This stage might require a Docker agent with PostgreSQL service capability
            // or a pre-configured Odoo test environment.
            agent {
                // Example: using a Docker agent with a sidecar container for Postgres
                // docker {
                //     image 'python:3.9-slim' // Base image with Python
                //     args '-v /var/run/docker.sock:/var/run/docker.sock' // If script needs to run Docker
                //     // registryUrl "${env.DOCKER_IMAGE_REGISTRY}" // If image is private
                //     // registryCredentialsId "${env.DOCKER_CREDENTIALS_ID}"
                // }
                // TODO: Define how PostgreSQL is provided for tests. Using host DB for now.
                label 'any'
            }
            steps {
                echo "Running Odoo Unit Tests..."
                // Assumes odoo-bin and dependencies are available in the agent's PATH or test script handles it
                // Provide DB credentials securely if not using a service container
                withCredentials([
                    string(credentialsId: 'odoo-test-db-password', variable: 'ODOO_TEST_DB_PASSWORD') // Example credential
                ]) {
                    sh """
                        dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh \\
                            --odoo-database-name "${env.ODOO_TEST_DB_PREFIX}_unit_${env.BUILD_ID}" \\
                            --odoo-modules-to-test "${env.ODOO_MODULES_TO_TEST_UNIT}" \\
                            --test-type "unit" \\
                            --odoo-addons-path "${env.ODOO_ADDONS_PATH_CI}" \\
                            --db-host "localhost" \\
                            --db-user "odoo_test_user" \\
                            --db-password "\${ODOO_TEST_DB_PASSWORD}"
                    """
                }
                // archiveArtifacts artifacts: '**/odoo_test_results/*.xml', fingerprint: true // If XML reports are generated
            }
        }

        stage('Integration Tests (Odoo)') {
            agent { label 'any' } // Similar agent requirements as Unit Tests
            steps {
                echo "Running Odoo Integration Tests..."
                withCredentials([
                    string(credentialsId: 'odoo-test-db-password', variable: 'ODOO_TEST_DB_PASSWORD')
                ]) {
                     sh """
                        dfr_operations/cicd_pipelines/scripts/common/run_odoo_tests.sh \\
                            --odoo-database-name "${env.ODOO_TEST_DB_PREFIX}_integration_${env.BUILD_ID}" \\
                            --odoo-modules-to-test "${env.ODOO_MODULES_TO_TEST_INTEGRATION}" \\
                            --test-type "integration" \\
                            --odoo-addons-path "${env.ODOO_ADDONS_PATH_CI}" \\
                            --db-host "localhost" \\
                            --db-user "odoo_test_user" \\
                            --db-password "\${ODOO_TEST_DB_PASSWORD}"
                    """
                }
                // archiveArtifacts artifacts: '**/odoo_integration_test_results/*.xml', fingerprint: true
            }
        }

        stage('SAST Scan (SonarQube)') {
            when {
                expression { return env.ENABLE_SAST_SCANS_PER_COMMIT == 'true' && (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'develop') }
            }
            steps {
                echo "Performing SAST Scan with SonarQube..."
                // Assumes SonarScanner CLI is available on the agent or use 'withSonarQubeEnv'
                withCredentials([string(credentialsId: env.SONAR_CREDENTIALS_ID, variable: 'SONAR_TOKEN_VALUE')]) {
                    // Example: sh "sonar-scanner -Dsonar.projectKey=dfr_odoo_backend -Dsonar.sources=${env.ODOO_MODULES_PATH} -Dsonar.host.url=${env.SONAR_HOST_URL} -Dsonar.login=${SONAR_TOKEN_VALUE}"
                    // Using dfrPipelineUtils if available and configured for Sonar
                    script {
                        if (common.dfrPipelineUtils) { // Check if shared library step is loaded
                            common.dfrPipelineUtils.performSastScan(
                                toolName: 'sonar',
                                projectKey: 'dfr_odoo_backend_jenkins',
                                sourcesPath: env.ODOO_MODULES_PATH,
                                sonarHostUrl: env.SONAR_HOST_URL,
                                sonarLoginToken: SONAR_TOKEN_VALUE
                            )
                        } else {
                             sh """
                                # Ensure SonarScanner CLI is in PATH
                                sonar-scanner \\
                                  -Dsonar.projectKey=dfr_odoo_backend_jenkins \\
                                  -Dsonar.sources=${env.ODOO_MODULES_PATH} \\
                                  -Dsonar.host.url=${env.SONAR_HOST_URL} \\
                                  -Dsonar.login=${SONAR_TOKEN_VALUE} \\
                                  -Dsonar.branch.name=${env.BRANCH_NAME}
                                  # Add PR parameters if it's a PR build:
                                  # -Dsonar.pullrequest.base=...
                                  # -Dsonar.pullrequest.branch=...
                                  # -Dsonar.pullrequest.key=...
                             """
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker Image: ${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}"
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        dfr_operations/cicd_pipelines/scripts/common/build_odoo_docker.sh \\
                            --docker-image-name "${env.FULL_DOCKER_IMAGE_NAME}" \\
                            --image-tag "${env.IMAGE_TAG}" \\
                            --dockerfile-path "${env.DOCKERFILE_PATH}" \\
                            --build-context "${env.BUILD_CONTEXT}" \\
                            --push-image "true" \\
                            --docker-registry-url "${env.DOCKER_IMAGE_REGISTRY}" \\
                            --docker-username "\${DOCKER_USER}" \\
                            --docker-password "\${DOCKER_PASS}" \\
                            --build-args "--build-arg VCS_REF=${env.GIT_COMMIT} --build-arg VERSION=${env.IMAGE_TAG}"
                    """
                }
            }
        }

        stage('DAST Scan (OWASP ZAP)') {
            when {
                expression { return env.ENABLE_DAST_SCANS_PER_BUILD == 'true' && (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'develop') }
            }
            steps {
                echo "Performing DAST Scan with OWASP ZAP..."
                // This step assumes the application (using the just-built image) is deployed to a temporary
                // or staging environment accessible at ZAP_TARGET_URL_STAGING.
                // The actual deployment to a scan environment is not included here for brevity.
                // It might involve a temporary `docker run` or deployment to a k8s namespace.
                
                // Example using official ZAP Docker image for baseline scan:
                // Ensure Docker is available on the agent
                sh """
                    docker run --rm -v \$(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \\
                        -t "${env.ZAP_TARGET_URL_STAGING}" \\
                        -g gen.conf \\
                        -r zap_report.html \\
                        -J zap_report.json
                        # Add -P PORT if ZAP needs to proxy through a specific port
                """
                archiveArtifacts artifacts: 'zap_report.html, zap_report.json', fingerprint: true
            }
        }

        stage('Deploy to Staging') {
            when {
                expression { return (env.BRANCH_NAME == 'develop' || (env.BRANCH_NAME == 'main' && env.AUTO_DEPLOY_TO_STAGING_ON_MAIN_MERGE == 'true')) }
            }
            steps {
                echo "Preparing to deploy to Staging: Image ${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}"
                input message: "Approve deployment to Staging environment for image ${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}?", submitterParameter: 'APPROVER_USER'
                
                withCredentials([file(credentialsId: env.STAGING_DEPLOY_CREDENTIALS_ID, variable: 'STAGING_DEPLOY_KEY_PATH')]) {
                    // Assuming deploy_application.sh can use SSH keys or other creds passed via env vars or files
                    // Or, if it needs specific env vars for cloud provider CLI:
                    // withAWS(credentials: env.STAGING_AWS_CREDENTIALS_ID, region: 'us-east-1') { ... }
                    sh """
                        dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh \\
                            --deployment-env "staging" \\
                            --app-name "${env.DOCKER_IMAGE_BASE_NAME}" \\
                            --image-tag-or-artifact-path "${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}" \\
                            --config-file-path "${env.STAGING_CONFIG_FILE_PATH}" \\
                            --deployment-type "docker-compose"
                            # Add --kube-context or --aws-profile if needed by the script and configured
                    """
                }
            }
        }

        stage('Deploy to Production') {
            when {
                // Deploy to production from version tags (e.g., v1.0.0) or main branch if not deploying from tags.
                // Manual approval is typically always enforced for production.
                anyOf {
                    tag 'v*.*.*'
                    expression { return env.BRANCH_NAME == 'main' && !env.TAG_NAME } // Main branch if not a tag build
                }
            }
            steps {
                echo "Preparing to deploy to Production: Image ${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}"
                script {
                    if (env.TAG_NAME) {
                        echo "Deploying tag ${env.TAG_NAME} to Production."
                    } else {
                        echo "Deploying branch ${env.BRANCH_NAME} (commit ${env.GIT_COMMIT.take(7)}) to Production."
                    }
                }

                if (env.REQUIRE_MANUAL_APPROVAL_FOR_PRODUCTION_DEPLOYMENT == 'true') {
                    input message: "CRITICAL: Approve deployment to Production environment for image ${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}?", submitterParameter: 'APPROVER_USER'
                }

                // If tagging is done as part of production deployment flow triggered by main branch merge (not by tag itself)
                script {
                    if (env.TAG_NAME == null && env.BRANCH_NAME == 'main') {
                        // This logic is complex: if main branch deploys to prod, a tag should be created.
                        // Usually, a tag build triggers prod deployment. This is a fallback.
                        // Consider having a separate job to create tags, which then triggers this deployment.
                        // For now, let's assume if it's a main branch deploy, we might want to tag it.
                        // A proper version needs to be determined (e.g., from a file, or incremented).
                        // def newVersion = "vX.Y.Z" // This needs a versioning strategy
                        // sh "dfr_operations/cicd_pipelines/scripts/common/tag_git_release.sh --version ${newVersion}"
                        echo "Production deployment from main branch. Consider tagging strategy."
                    }
                }
                
                withCredentials([file(credentialsId: env.PROD_DEPLOY_CREDENTIALS_ID, variable: 'PROD_DEPLOY_KEY_PATH')]) {
                    sh """
                        dfr_operations/cicd_pipelines/scripts/common/deploy_application.sh \\
                            --deployment-env "production" \\
                            --app-name "${env.DOCKER_IMAGE_BASE_NAME}" \\
                            --image-tag-or-artifact-path "${env.FULL_DOCKER_IMAGE_NAME}:${env.IMAGE_TAG}" \\
                            --config-file-path "${env.PRODUCTION_CONFIG_FILE_PATH}" \\
                            --deployment-type "docker-compose"
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Current result: ${currentBuild.currentResult}"
            // Call shared library for notification
            script {
                if (common.dfrPipelineUtils) { // Check if shared library step is loaded
                    common.dfrPipelineUtils.notifyBuildStatus(
                        buildResult: currentBuild.currentResult,
                        recipientList: 'devops-alerts@example.com,product-owner@example.com', // Configure recipients
                        customMessage: "DFR Odoo Backend pipeline '${env.JOB_NAME}' build #${env.BUILD_NUMBER} completed."
                    )
                } else {
                    echo "dfrPipelineUtils not found. Skipping notification."
                    // Fallback basic mail step if library not present
                    // mail to: 'dev-team@example.com',
                    //      subject: "Jenkins Build ${currentBuild.currentResult}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    //      body: "Check build log at ${env.BUILD_URL}"
                }
            }
            // Cleanup workspace or other resources
            cleanWs()
        }
        success {
            echo "Pipeline successfully completed."
        }
        failure {
            echo "Pipeline failed."
            // Additional failure actions, e.g., create Jira ticket
        }
        // aborted {}
        // unstable {}
    }
}