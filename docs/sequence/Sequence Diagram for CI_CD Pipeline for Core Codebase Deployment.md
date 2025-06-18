sequenceDiagram
    actor "Git Repository" as GitVCS
    participant "CI/CD System" as CICDSystem
    participant "Staging Environment" as StagingEnv
    participant "Production Environment" as ProdEnv

    note over GitVCS: Process starts when a Developer commits and pushes code to the monitored branch in the Git Repository.
    GitVCS-CICDSystem: 1. [Webhook] Code Pushed to Core Branch (e.g., main, release/*)
    activate CICDSystem
    CICDSystem--GitVCS: HTTP 200 OK (Webhook Ack)

    CICDSystem-CICDSystem: 2. Trigger Core Codebase Deployment Pipeline

    CICDSystem-GitVCS: 3. Checkout/Clone Latest Code from Pushed Commit
    activate GitVCS
    GitVCS--CICDSystem: Source Code Files
    deactivate GitVCS

    CICDSystem-CICDSystem: 4. Build DFR Application Docker Image (Odoo + Custom Modules)
    CICDSystem-CICDSystem: 4.1. Push Docker Image to Registry (e.g., DockerHub, AWS ECR)

    CICDSystem-CICDSystem: 5. Run Automated Tests (Unit & Integration)

    alt 6.1. [Tests Passed]
        CICDSystem-StagingEnv: 6.1.1. Deploy Docker Image to Staging
        activate StagingEnv
        StagingEnv-StagingEnv: 6.1.1.1. Pull Image, Start Containers, Run DB Migrations
        StagingEnv--CICDSystem: Staging Deployment Status (Success)
        deactivate StagingEnv

        CICDSystem-CICDSystem: 6.1.2. Notify Team: Staging Ready for UAT (Build X)

        note over StagingEnv: User Acceptance Testing (UAT) is performed manually on the Staging Environment by designated testers. Approval is signaled back to the CI/CD System to proceed.
        CICDSystem-CICDSystem: 6.1.3. Await UAT Approval & Manual Trigger for Production

        note right of CICDSystem: If UAT is rejected, the 'Promote to Production' signal is not sent. The issue is reported, and the pipeline halts for this build regarding production deployment.
        CICDSystem-CICDSystem: 6.1.4. Receive 'Promote to Production' Signal for Build X (UAT Approved)

        CICDSystem-ProdEnv: 6.1.4.1. Deploy Docker Image to Production
        activate ProdEnv
        ProdEnv-ProdEnv: 6.1.4.1.1. Pull Image, Start Containers, Run DB Migrations
        ProdEnv--CICDSystem: Production Deployment Status (Success)
        deactivate ProdEnv

        CICDSystem-CICDSystem: 6.1.4.2. Notify Team: Production Deployment Complete (Build X)

    else 6.2. [Tests Failed]
        CICDSystem-CICDSystem: 6.2.1. Log Test Failure, Notify Developers. Pipeline Halted.
    end

    deactivate CICDSystem