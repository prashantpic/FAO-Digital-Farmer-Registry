/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, onWillUnmount, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ImportProgressWidget extends Component {
    static template = "dfr_data_tools.ImportProgressWidget";
    static props = {
        jobId: { type: Number, optional: false },
    };

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            progress: 0,
            statusText: "Initializing...",
            successfulRecords: 0,
            failedRecords: 0,
            totalRecordsProcessed: 0,
            totalRecordsInFile: 0,
            jobState: "draft",
            errorMessage: "",
        });
        this.intervalId = null;
    }

    async onWillStart() {
        if (this.props.jobId) {
            await this._fetchProgress();
        }
    }

    onMounted() {
        // Start polling only if the job is in a state that implies it's running or could run
        if (this.props.jobId && ['draft', 'in_progress'].includes(this.state.jobState)) {
             this.intervalId = setInterval(async () => {
                await this._fetchProgress();
            }, 5000); // Poll every 5 seconds
        }
    }

    onWillUnmount() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }

    async _fetchProgress() {
        if (!this.props.jobId) {
            this.state.statusText = "No Job ID provided.";
            // Potentially stop polling if jobId becomes invalid
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
            return;
        }
        try {
            const data = await this.rpc("/dfr_data_tools/job_progress/" + this.props.jobId, {});
            if (data.error) {
                this.state.statusText = `Error: ${data.error}`;
                this.state.errorMessage = `Error fetching progress: ${data.error}`;
                 if (this.intervalId) {
                    clearInterval(this.intervalId);
                    this.intervalId = null;
                 }
            } else {
                this.state.totalRecordsInFile = data.total_records_in_file || 0;
                this.state.totalRecordsProcessed = data.total_records_processed || 0;
                this.state.successfulRecords = data.successful_records || 0;
                this.state.failedRecords = data.failed_records || 0;
                this.state.jobState = data.state;

                if (this.state.totalRecordsInFile > 0) {
                    this.state.progress = Math.round((this.state.totalRecordsProcessed / this.state.totalRecordsInFile) * 100);
                } else {
                    this.state.progress = data.state === 'done' ? 100 : (data.state === 'in_progress' ? 0 : this.state.progress);
                }
                
                this.state.statusText = `State: ${data.state}. Processed: ${this.state.totalRecordsProcessed || 0}/${this.state.totalRecordsInFile || 0}. Success: ${this.state.successfulRecords || 0}, Failed: ${this.state.failedRecords || 0}.`;

                if (data.state === 'error' && !this.state.errorMessage) {
                    const jobDetails = await this.rpc("/web/dataset/call_kw/data.import.job/read", {
                        model: "data.import.job",
                        method: "read",
                        args: [[this.props.jobId], ['log_summary']],
                        kwargs: {},
                    });
                    if (jobDetails && jobDetails.length > 0) {
                        this.state.errorMessage = jobDetails[0].log_summary || "Job failed. Check detailed logs.";
                    }
                }


                if (['done', 'error', 'cancelled'].includes(data.state)) {
                    if (this.intervalId) {
                        clearInterval(this.intervalId);
                        this.intervalId = null;
                    }
                } else if (!this.intervalId && ['draft', 'in_progress'].includes(data.state)) {
                    // Re-start polling if it stopped but job is still active (e.g. page reload)
                     this.intervalId = setInterval(async () => {
                        await this._fetchProgress();
                    }, 5000);
                }
            }
        } catch (error) {
            console.error("Error fetching import progress:", error);
            this.state.statusText = "Error fetching progress.";
            this.state.errorMessage = `RPC Error: ${error.message || String(error)}`;
            if (this.intervalId) {
                clearInterval(this.intervalId);
                this.intervalId = null;
            }
        }
    }
}

registry.category("view_widgets").add("import_progress_widget", ImportProgressWidget);