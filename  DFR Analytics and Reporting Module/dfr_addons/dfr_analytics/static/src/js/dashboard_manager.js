/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc";
import { KpiWidget } from "./kpi_widget";
import { ChartWidget } from "./chart_widget";

export class DashboardManager extends Component {
    static template = 'dfr_analytics.DashboardManager';
    static components = { KpiWidget, ChartWidget };

    state = useState({
        loading: true,
        error: null,
        kpiData: {
            total_registrations: 0,
            gender_disaggregation: {},
            age_distribution: {}, // To be implemented in analytics_service
            registration_trends: [],
            total_plots: 0,
            total_land_area: 0,
            average_plot_size: 0,
            land_distribution_by_size: {}, // To be implemented in analytics_service
            total_submissions: 0, // For a specific form or all
            submissions_per_form: {},
            response_distribution: {},
            form_name: '',
        },
        chartData: {
            registrationTrends: { labels: [], datasets: [] },
            genderDisaggregation: { labels: [], datasets: [] },
            ageDistribution: { labels: [], datasets: [] }, // To be populated
            landDistribution: { labels: [], datasets: [] }, // To be populated
            formResponseDistribution: {}, // For dynamic form field charts
        },
        filters: {
            date_from: null,
            date_to: null,
            geographic_area_ids: [],
            farmer_status_ids: [],
            dynamic_form_id: null,
        },
        dynamicForms: [],
        // Add other filter options if needed (e.g. for geo areas, statuses)
        // geographicAreaOptions: [],
        // farmerStatusOptions: [],
    });

    async onWillStart() {
        await this.fetchInitialData();
    }

    async fetchInitialData() {
        this.state.loading = true;
        this.state.error = null;
        try {
            // Fetch list of dynamic forms for the filter dropdown
            const dynamicForms = await jsonrpc('/web/dataset/search_read', {
                model: 'dfr.dynamic.form',
                fields: ['id', 'name'],
                domain: [], // Add security/filter if needed
            });
            this.state.dynamicForms = dynamicForms;

            // Fetch other filter options (example)
            // this.state.geographicAreaOptions = await jsonrpc('/web/dataset/search_read', { model: 'dfr.administrative.area', fields: ['id', 'name'], domain: [] });
            // this.state.farmerStatusOptions = await jsonrpc('/web/dataset/search_read', { model: 'dfr.farmer.status', fields: ['id', 'name'], domain: [] });


            await this.updateDashboardData(this.state.filters); // Load data with default/empty filters

        } catch (e) {
            console.error("Error fetching initial dashboard configuration:", e);
            this.state.error = "Failed to load dashboard configuration data.";
            this.state.loading = false;
        }
    }

    // Method to handle filter changes and update dashboard data
    async updateDashboardData(newFilters = {}) {
        // Update state with new filters
        this.state.filters = { ...this.state.filters, ...newFilters };
        this.state.loading = true;
        this.state.error = null;

        try {
            const farmerKpis = await jsonrpc('/web/dataset/call_kw/dfr.analytics.service/get_farmer_registration_kpis', {
                model: 'dfr.analytics.service',
                method: 'get_farmer_registration_kpis',
                args: [this.state.filters],
                kwargs: {},
            });
            const landKpis = await jsonrpc('/web/dataset/call_kw/dfr.analytics.service/get_landholding_summary_kpis', {
                model: 'dfr.analytics.service',
                method: 'get_landholding_summary_kpis',
                args: [this.state.filters],
                kwargs: {},
            });

            let formKpis = {
                total_submissions: 0,
                submissions_per_form: {},
                response_distribution: {},
                form_name: 'N/A',
            };
            if (this.state.filters.dynamic_form_id) {
                 formKpis = await jsonrpc('/web/dataset/call_kw/dfr.analytics.service/get_dynamic_form_submission_kpis', {
                    model: 'dfr.analytics.service',
                    method: 'get_dynamic_form_submission_kpis',
                    args: [this.state.filters.dynamic_form_id, this.state.filters],
                    kwargs: {},
                });
            } else {
                 // Fetch overview for all forms if no specific form is selected
                 formKpis = await jsonrpc('/web/dataset/call_kw/dfr.analytics.service/get_dynamic_form_submission_kpis', {
                    model: 'dfr.analytics.service',
                    method: 'get_dynamic_form_submission_kpis',
                    args: [null, this.state.filters], // Pass null for form_id
                    kwargs: {},
                });
            }


            this.state.kpiData = { ...farmerKpis, ...landKpis, ...formKpis };

            // Populate chart data structure
            this.state.chartData.registrationTrends = this._transformTrendData(farmerKpis.registration_trends);
            this.state.chartData.genderDisaggregation = this._transformPieData(farmerKpis.gender_disaggregation, 'Gender Distribution');
            // TODO: Add transformations for ageDistribution and landDistribution when data is available
            // this.state.chartData.ageDistribution = this._transformBarData(farmerKpis.age_distribution, 'Age Distribution');
            // this.state.chartData.landDistribution = this._transformBarData(landKpis.land_distribution_by_size, 'Land Size Distribution');

            if (this.state.filters.dynamic_form_id && formKpis.response_distribution) {
                this.state.chartData.formResponseDistribution = {}; // Reset
                for (const fieldLabel in formKpis.response_distribution) {
                    this.state.chartData.formResponseDistribution[fieldLabel] = this._transformBarData(
                        formKpis.response_distribution[fieldLabel],
                        fieldLabel
                    );
                }
            } else {
                 this.state.chartData.formResponseDistribution = {}; // Clear if no form selected
            }


        } catch (e) {
            console.error("Error fetching filtered dashboard data:", e);
            this.state.error = "Failed to load filtered dashboard data.";
        } finally {
            this.state.loading = false;
        }
    }

    _transformTrendData(rawData) {
        if (!rawData || rawData.length === 0) return { labels: [], datasets: [] };
        const sortedData = [...rawData].sort((a, b) => new Date(a.period) - new Date(b.period));
        return {
            labels: sortedData.map(item => item.period),
            datasets: [{
                label: 'Registrations per Month',
                data: sortedData.map(item => item.count),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        };
    }

    _transformPieData(rawData, label) {
        if (!rawData || Object.keys(rawData).length === 0) return { labels: [], datasets: [] };
        const labels = Object.keys(rawData);
        const data = Object.values(rawData);
        const backgroundColors = [
            'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)'
        ];
        const borderColors = backgroundColors.map(color => color.replace('0.6', '1'));
        return {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: backgroundColors.slice(0, labels.length),
                borderColor: borderColors.slice(0, labels.length),
                borderWidth: 1
            }]
        };
    }
    
    _transformBarData(rawData, label) {
        if (!rawData || Object.keys(rawData).length === 0) return { labels: [], datasets: [] };
        const labels = Object.keys(rawData);
        const data = Object.values(rawData);
        const backgroundColors = [
            'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)', 'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)',
            'rgba(100, 100, 100, 0.6)', 'rgba(200, 50, 50, 0.6)' 
        ]; // Add more colors if needed
        const borderColors = backgroundColors.map(color => color.replace('0.6', '1'));

        return {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: labels.map((_, i) => backgroundColors[i % backgroundColors.length]),
                borderColor: labels.map((_, i) => borderColors[i % borderColors.length]),
                borderWidth: 1
            }]
        };
    }

    onFilterChange(filterName, value) {
        const newFilters = { ...this.state.filters };
        newFilters[filterName] = value;
        if (filterName === 'dynamic_form_id' && value === "") { // Handle "Select Form" option
            newFilters[filterName] = null;
        } else if (filterName === 'dynamic_form_id' && value !== null) {
            newFilters[filterName] = parseInt(value);
        }
        this.updateDashboardData(newFilters);
    }
}