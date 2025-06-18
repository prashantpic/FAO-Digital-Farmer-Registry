/** @odoo-module **/

import { Component, useState, useRef, onWillStart, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc";

// Assume Leaflet.js and leaflet.css are loaded via assets_backend from static/lib/

export class MapViewComponent extends Component {
    static template = 'dfr_analytics.MapViewComponent';

    state = useState({
        geoData: null,
        loading: true,
        error: null,
        filters: {}, // Placeholder for map specific filters
    });

    mapRef = useRef("mapContainer");
    mapInstance = null;
    geoJsonLayer = null;
    _prevGeoDataString = null; // To compare if geoData actually changed

    async onWillStart() {
        await this.fetchGeoData();
    }

    onMounted() {
        if (typeof L === 'undefined') {
            console.error("Leaflet.js library not found. Map cannot be initialized.");
            this.state.error = "Mapping library (Leaflet.js) not found. Please ensure it is loaded.";
            return;
        }
        this.initializeMap();
    }
    
    onWillUpdateProps(nextProps, nextState) {
        // This is primarily for reacting to state changes, as props are not expected to change for this component.
        // Or if filters were passed as props.
        if (this.mapInstance && nextState.geoData) {
            const currentGeoDataString = JSON.stringify(nextState.geoData);
            if (currentGeoDataString !== this._prevGeoDataString) {
                this._updateGeoJsonLayer(nextState.geoData);
                this._prevGeoDataString = currentGeoDataString;
            }
        }
    }


    onWillUnmount() {
        if (this.mapInstance) {
            this.mapInstance.remove();
            this.mapInstance = null;
        }
    }

    async fetchGeoData() {
        this.state.loading = true;
        this.state.error = null;
        try {
            const data = await jsonrpc('/web/dataset/call_kw/dfr.analytics.service/get_farmer_plot_geo_data', {
                model: 'dfr.analytics.service',
                method: 'get_farmer_plot_geo_data',
                args: [this.state.filters],
                kwargs: {},
            });
            this.state.geoData = data;
            this._prevGeoDataString = JSON.stringify(data); // Store initial stringified data
        } catch (e) {
            console.error("Error fetching geo data:", e);
            this.state.error = e.message || "Failed to load geographical data.";
        } finally {
            this.state.loading = false;
        }
    }

    initializeMap() {
        if (this.mapRef.el && !this.mapInstance) {
            this.mapInstance = L.map(this.mapRef.el).setView([0, 0], 2); // Default view

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.mapInstance);

            if (this.state.geoData && this.state.geoData.length > 0) {
                this._addGeoJsonLayer(this.state.geoData);
            } else if (!this.state.loading && this.state.geoData && this.state.geoData.length === 0) {
                // If no data, maybe show a message or set a default view for a region
                this.mapInstance.setView([0,0], 2); // Default zoom if no data
            }
        }
    }

    _addGeoJsonLayer(geoJsonData) {
        if (!this.mapInstance || !geoJsonData) return;

        this.geoJsonLayer = L.geoJSON(geoJsonData, {
            onEachFeature: this._onEachFeature.bind(this),
            pointToLayer: this._pointToLayer.bind(this),
            style: this._styleFeature.bind(this),
        }).addTo(this.mapInstance);

        if (geoJsonData.length > 0 && this.geoJsonLayer.getBounds().isValid()) {
            this.mapInstance.fitBounds(this.geoJsonLayer.getBounds(), { padding: [20, 20] });
        } else {
             // Fallback if bounds are not valid (e.g., single point far away or no features)
             this.mapInstance.setView([0, 0], 2); // Or a default region if applicable
        }
    }

    _updateGeoJsonLayer(newGeoJsonData) {
        if (!this.mapInstance) return;
        if (this.geoJsonLayer) {
            this.mapInstance.removeLayer(this.geoJsonLayer);
            this.geoJsonLayer = null;
        }
        if (newGeoJsonData && newGeoJsonData.length > 0) {
            this._addGeoJsonLayer(newGeoJsonData);
        } else {
            // No data, ensure map is clear or shows default
            this.mapInstance.setView([0,0], 2);
        }
    }

    _onEachFeature(feature, layer) {
        if (feature.properties) {
            let popupContent = "";
            if (feature.properties.type === 'farmer_homestead') {
                popupContent += `<strong>Farmer Homestead</strong><br/>`;
                popupContent += `<b>Name:</b> ${feature.properties.name || 'N/A'}<br/>`;
                popupContent += `<b>UID:</b> ${feature.properties.farmer_uid || 'N/A'}`;
            } else if (feature.properties.type === 'plot') {
                popupContent += `<strong>Plot</strong><br/>`;
                popupContent += `<b>UID:</b> ${feature.properties.plot_uid || 'N/A'}<br/>`;
                popupContent += `<b>Farmer:</b> ${feature.properties.farmer_name || 'N/A'}<br/>`;
                popupContent += `<b>Size (Ha):</b> ${feature.properties.plot_size !== undefined ? feature.properties.plot_size : 'N/A'}`;
            } else {
                 popupContent = JSON.stringify(feature.properties, null, 2); // Default popup
            }
            layer.bindPopup(popupContent);
        }
    }

    _pointToLayer(feature, latlng) {
        let color = 'gray'; // Default color
        if (feature.properties) {
            if (feature.properties.type === 'farmer_homestead') color = 'blue';
            else if (feature.properties.type === 'plot') color = 'green';
        }
        return L.circleMarker(latlng, {
            radius: 6,
            fillColor: color,
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });
    }

    _styleFeature(feature) {
        if (feature.geometry.type === 'Polygon') {
            return {
                fillColor: '#3388ff', // Default Leaflet blue
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.5
            };
        }
        return {}; // Default style for points or other geometries
    }

    // Example method to be called if filters are added to this component's UI
    async applyMapFilters(newFilters) {
        this.state.filters = { ...this.state.filters, ...newFilters };
        await this.fetchGeoData(); // This will trigger onWillUpdateProps logic due to state change
    }
}