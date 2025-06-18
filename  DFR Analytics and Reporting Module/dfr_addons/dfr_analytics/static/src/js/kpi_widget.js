/** @odoo-module **/

import { Component } from "@odoo/owl";

export class KpiWidget extends Component {
    static template = 'dfr_analytics.KpiWidget';

    static props = {
        title: String,
        value: { type: [String, Number], optional: true }, // Make optional to handle loading/N/A
        icon: { type: String, optional: true },
        trend: { type: String, optional: true }, // 'up', 'down', 'neutral'
        percentage_change: { type: [String, Number], optional: true },
    };

    get displayValue() {
        return this.props.value !== undefined && this.props.value !== null ? this.props.value : 'N/A';
    }
}