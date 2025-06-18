/**
 * Sends a build notification.
 *
 * @param config A Map containing the notification configuration.
 * Expected keys:
 *   - buildResult (String, Required): The result of the build (e.g., currentBuild.currentResult).
 *   - recipientList (String, Required): Comma-separated string of email addresses or notification channel.
 *   - customMessage (String, Optional): Additional custom message content.
 *   - mailer (Object, Optional): Jenkins mail step object for advanced configuration. If not provided, basic mail step is used.
 */
def notifyBuildStatus(Map config) {
    if (!config.buildResult || !config.recipientList) {
        error "notifyBuildStatus: 'buildResult' and 'recipientList' are required parameters."
        return
    }

    String buildResult = config.buildResult
    String recipientList = config.recipientList
    String customMessage = config.customMessage ?: ""
    String subject = "Jenkins Build ${buildResult}: ${env.JOB_NAME} - #${env.BUILD_NUMBER}"
    String body = """
    <p>Build Result: ${buildResult}</p>
    <p>Job: ${env.JOB_NAME}</p>
    <p>Build Number: ${env.BUILD_NUMBER}</p>
    <p>Build URL: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
    """
    if (customMessage) {
        body += "<p>Custom Message: ${customMessage}</p>"
    }

    // Example using Jenkins 'mail' step.
    // Ensure Mailer Plugin is installed and configured in Jenkins.
    // This is a basic example; more complex logic for Slack, Teams, etc., would go here.
    echo "Sending notification: Subject='${subject}', To='${recipientList}'"
    try {
        if (config.mailer) {
            config.mailer to: recipientList, subject: subject, body: body, mimeType: 'text/html'
        } else {
            mail to: recipientList, subject: subject, body: body, mimeType: 'text/html'
        }
        echo "Notification sent successfully."
    } catch (Exception e) {
        echo "Error sending notification: ${e.getMessage()}"
        // Decide if this failure should affect the build status
    }
}

/**
 * Performs a Static Application Security Testing (SAST) scan.
 *
 * @param config A Map containing the SAST scan configuration.
 * Expected keys:
 *   - toolName (String, Required): Name of the SAST tool (e.g., 'sonar', 'bandit').
 *   - projectKey (String, Optional): Project identifier for the SAST tool (especially for SonarQube).
 *   - sourcesPath (String, Required): Path to the source code to be scanned.
 *   - sonarHostUrl (String, Optional, for Sonar): SonarQube server URL.
 *   - sonarLoginTokenVar (String, Optional, for Sonar): Environment variable name holding the SonarQube token.
 *   - sonarCredentialsId (String, Optional, for Sonar): Jenkins credential ID for SonarQube token.
 *   - customCliArgs (String, Optional): Additional command-line arguments for the SAST tool.
 */
def performSastScan(Map config) {
    if (!config.toolName || !config.sourcesPath) {
        error "performSastScan: 'toolName' and 'sourcesPath' are required parameters."
        return
    }

    String toolName = config.toolName.toLowerCase()
    String sourcesPath = config.sourcesPath
    String projectKey = config.projectKey ?: env.JOB_NAME // Default project key
    String customCliArgs = config.customCliArgs ?: ""

    echo "Performing SAST scan with tool: ${toolName}"
    echo "Sources path: ${sourcesPath}"

    switch (toolName) {
        case 'sonar':
        case 'sonarqube':
            if (!config.sonarHostUrl) {
                error "performSastScan (Sonar): 'sonarHostUrl' is required."
                return
            }
            if (!config.sonarLoginTokenVar && !config.sonarCredentialsId) {
                error "performSastScan (Sonar): Either 'sonarLoginTokenVar' (env var name) or 'sonarCredentialsId' (Jenkins credential) is required."
                return
            }

            String sonarScannerCmd = "sonar-scanner -Dsonar.projectKey=${projectKey} -Dsonar.sources=${sourcesPath} -Dsonar.host.url=${config.sonarHostUrl}"
            if (env.BRANCH_NAME && env.BRANCH_NAME !=~ /(?i)(master|main|develop)/ && env.CHANGE_ID) { // Assuming pull/merge request
                sonarScannerCmd += " -Dsonar.pullrequest.branch=${env.BRANCH_NAME}"
                sonarScannerCmd += " -Dsonar.pullrequest.key=${env.CHANGE_ID}" // Or appropriate PR ID variable
                if (env.CHANGE_TARGET) {
                    sonarScannerCmd += " -Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
                }
            }
            
            sonarScannerCmd += " ${customCliArgs}" // Add any custom args

            if (config.sonarCredentialsId) {
                withCredentials([string(credentialsId: config.sonarCredentialsId, variable: 'SONAR_TOKEN_VALUE')]) {
                    sh "${sonarScannerCmd} -Dsonar.login=${SONAR_TOKEN_VALUE}"
                }
            } else if (config.sonarLoginTokenVar) {
                // Ensure the environment variable config.sonarLoginTokenVar is set (e.g., from Jenkins global env or secrets)
                if (!env."${config.sonarLoginTokenVar}") {
                     error "performSastScan (Sonar): Environment variable '${config.sonarLoginTokenVar}' for Sonar token is not set."
                     return
                }
                sh "${sonarScannerCmd} -Dsonar.login=${env."${config.sonarLoginTokenVar}"}"
            }
            break
        case 'bandit':
            // Example for Bandit (Python SAST tool)
            // Ensure bandit is installed in the agent environment
            sh "bandit -r ${sourcesPath} -f json -o bandit_report.json ${customCliArgs}"
            // Optionally archive the report
            archiveArtifacts artifacts: 'bandit_report.json', allowEmptyArchive: true
            echo "Bandit scan complete. Report: bandit_report.json"
            break
        default:
            error "performSastScan: Unsupported SAST tool '${toolName}'. Supported tools: 'sonar', 'bandit'."
            return
    }
    echo "SAST scan with ${toolName} completed."
}

/**
 * Runs a custom deployment step, typically executing a specified script.
 *
 * @param config A Map containing the deployment step configuration.
 * Expected keys:
 *   - environment (String, Required): Target deployment environment (e.g., 'staging', 'production').
 *   - appName (String, Required): Name of the application being deployed.
 *   - scriptPath (String, Required): Path to the deployment script to execute.
 *   - scriptArgs (String, Optional): Arguments to pass to the deployment script.
 *   - deploymentCredentialsId (String, Optional): Jenkins credential ID for deployment (e.g., SSH key, token).
 */
def runCustomDeploymentStep(Map config) {
    if (!config.environment || !config.appName || !config.scriptPath) {
        error "runCustomDeploymentStep: 'environment', 'appName', and 'scriptPath' are required parameters."
        return
    }

    String environment = config.environment
    String appName = config.appName
    String scriptPath = config.scriptPath
    String scriptArgs = config.scriptArgs ?: ""

    echo "Running custom deployment step for app '${appName}' to environment '${environment}' using script '${scriptPath}'."

    // Construct the command
    String command = "sh \"${scriptPath} ${scriptArgs}\""

    // Wrap with credentials if specified
    if (config.deploymentCredentialsId) {
        // This is a generic example. The type of credential (e.g., sshUserPrivateKey, usernamePassword)
        // and how it's used (e.g., withSSH, withCredentials block type) depends on the deployment script's needs.
        // For a generic script, we might pass credential values as environment variables.
        echo "Executing with deployment credentials ID: ${config.deploymentCredentialsId}"
        // Example: If it's a username/password
        // withCredentials([usernamePassword(credentialsId: config.deploymentCredentialsId, usernameVariable: 'DEPLOY_USER', passwordVariable: 'DEPLOY_PASS')]) {
        //    env.DEPLOYMENT_ENV = environment // Pass other necessary env vars
        //    env.APP_NAME = appName
        //    evaluate(command) // Use evaluate if command is built dynamically with env vars from credentials
        // }
        // For simplicity, this example assumes the script handles credentials internally or via env vars
        // set by a more specific withCredentials block if needed by the caller of this utility.
        // A common pattern is for `scriptPath` to be one of the common/deploy_application.sh scripts
        // which itself expects environment variables for things like IMAGE_TAG, CONFIG_FILE_PATH, etc.
        // These should be set in the 'environment' block of the Jenkinsfile stage or directly before calling this utility.
        
        // This utility focuses on executing the script. Credential handling for the script's execution context
        // should be managed by the calling Jenkinsfile stage.
        // If the script itself needs to be executed within a `withCredentials` block, the Jenkinsfile
        // should wrap the call to `runCustomDeploymentStep` within that block.
        // However, if the credential ID is passed here, we could attempt a generic `withCredentials`.
        withCredentials([[$class: 'StringBinding', credentialsId: config.deploymentCredentialsId, variable: 'DEPLOY_SECRET_CONTENT']]) {
            // DEPLOY_SECRET_CONTENT can be used by the script if it expects a secret file path or content via env.
            // This is very generic; specific credential types need specific bindings.
            echo "Deployment script will run with DEPLOY_SECRET_CONTENT available (if StringBinding used)."
            sh "${scriptPath} ${scriptArgs}"
        }

    } else {
        sh "${scriptPath} ${scriptArgs}"
    }

    echo "Custom deployment step for '${appName}' to '${environment}' completed."
}

return this