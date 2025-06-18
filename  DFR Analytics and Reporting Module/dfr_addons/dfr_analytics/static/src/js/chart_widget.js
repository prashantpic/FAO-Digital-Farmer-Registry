/** @odoo-module **/

import { Component, useRef, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";

// Assume Chart.js is loaded globally or via assets_backend.
// If not, it needs to be imported or loaded explicitly.
// e.g. import Chart from 'chart.js/auto'; // if using npm and bundler

export class ChartWidget extends Component {
    static template = 'dfr_analytics.ChartWidget';

    static props = {
        chartType: String, // e.g., 'bar', 'line', 'pie', 'doughnut'
        chartData: Object, // Chart.js data structure: { labels: [], datasets: [] }
        chartOptions: { type: Object, optional: true }, // Chart.js options
        title: { type: String, optional: true }, // Optional title for the chart
    };

    canvasRef = useRef("canvas");
    chartInstance = null;

    onMounted() {
        if (typeof Chart === 'undefined') {
            console.error("Chart.js library not found. Chart cannot be initialized.");
            const canvasEl = this.canvasRef.el;
            if (canvasEl) {
                const ctx = canvasEl.getContext('2d');
                ctx.font = "16px Arial";
                ctx.fillStyle = "red";
                ctx.textAlign = "center";
                ctx.fillText("Chart.js not loaded", canvasEl.width / 2, canvasEl.height / 2);
            }
            return;
        }
        this._renderChart();
    }

    onWillUpdateProps(nextProps) {
        if (!this.chartInstance || typeof Chart === 'undefined') return;

        let needsUpdate = false;
        if (JSON.stringify(nextProps.chartData) !== JSON.stringify(this.props.chartData)) {
            this.chartInstance.data = nextProps.chartData;
            needsUpdate = true;
        }
        if (JSON.stringify(nextProps.chartOptions) !== JSON.stringify(this.props.chartOptions)) {
            this.chartInstance.options = { ...(this.props.chartOptions || {}), ...nextProps.chartOptions }; // Merge options
            needsUpdate = true;
        }
        if (nextProps.chartType !== this.props.chartType) {
            // If chart type changes, we need to destroy and re-create
            this.chartInstance.destroy();
            this.chartInstance = null; // Mark for re-creation
            this._renderChart(nextProps); // Re-render with new props
            return; // Exit as chart is re-rendered
        }

        if (needsUpdate) {
            this.chartInstance.update();
        }
    }

    onWillUnmount() {
        if (this.chartInstance) {
            this.chartInstance.destroy();
            this.chartInstance = null;
        }
    }

    _renderChart(propsToUse = this.props) {
        if (this.canvasRef.el && !this.chartInstance) { // Ensure not already initialized
            const defaultOptions = {
                responsive: true,
                maintainAspectRatio: false, // Allows setting canvas height/width via CSS on container
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: !!propsToUse.title,
                        text: propsToUse.title || ''
                    }
                }
            };
            this.chartInstance = new Chart(this.canvasRef.el, {
                type: propsToUse.chartType,
                data: propsToUse.chartData,
                options: { ...defaultOptions, ...(propsToUse.chartOptions || {}) },
            });
        }
    }
}