# DFR Mobile Application Overview

This guide provides an overview of the Digital Farmer Registry (DFR) Mobile Application, designed for enumerators to efficiently manage farmer data in the field.

**Target Audience:** Enumerators

## 1. Introduction to the DFR Mobile App

The DFR Mobile Application is a powerful tool that allows you to:

*   Register new farmers and their households.
*   Update existing farmer information.
*   Record farm and plot details, including GPS coordinates.
*   Complete dynamic forms for various surveys and data collection activities.
*   Work offline and synchronize data when an internet connection is available.

## 2. Installation and Setup

### 2.1 Installation
The DFR Mobile Application can be installed on your assigned Android device.

*   **For devices managed by MDM (Mobile Device Management):** The application may be automatically pushed to your device or available via a managed app store. [Placeholder: Specific MDM instructions for each country, e.g., "Refer to your IT support for MDM installation steps."]
*   **For manual installation (if applicable):**
    1.  Download the `.apk` file from the official source provided by your supervisor. [Placeholder: Link to official APK download location if publicly accessible or instructions on how to receive it]
    2.  Enable "Install from Unknown Sources" in your Android settings if prompted.
    3.  Open the downloaded `.apk` file and follow the on-screen prompts to install.

    !!! warning "Security Notice"
        Only install the DFR Mobile Application from official sources provided by the DFR project team or your national administration.

### 2.2 Initial Login
Once installed, you will need to log in with the credentials provided to you.

1.  Open the DFR Mobile App.
2.  Enter your **Username** and **Password**.
    *   [Placeholder: Image of login screen - `assets/images/enumerator-manual/mobile-login-screen.png`]
    *   Alt text: Mobile app login screen
3.  Tap the **Login** button.

    !!! info "First Time Login"
        The first time you log in, the app may need to download initial configuration data. Ensure you have a stable internet connection for this.

## 3. Navigating the App

The main interface of the app is designed for ease of use.

*   **Dashboard/Home Screen:** After login, you'll see the main dashboard. This typically shows:
    *   Quick access to common tasks (e.g., "Register New Farmer", "Search Farmer").
    *   Sync status indicator.
    *   Summary of pending data.
    *   [Placeholder: Image of mobile app dashboard - `assets/images/enumerator-manual/mobile-dashboard.png`]
    *   Alt text: Mobile app dashboard
*   **Navigation Menu:** Usually accessible via a "hamburger" icon (☰) or a bottom navigation bar. This menu provides links to different sections like:
    *   Farmer List
    *   Form Submissions
    *   Settings
    *   Help/About
    *   [Placeholder: Details on menu structure and icons]

## 4. Key Functionalities

### 4.1 Farmer Search
You can search for existing farmers using various criteria.
*   See [Farmer Search (Mobile)](01-farmer-search.md) for detailed instructions.

### 4.2 Farmer Registration (New Farmers)
Register new farmers, their households, farms, and plots.
*   See [Farmer Registration (Mobile)](02-farmer-registration-mobile.md) for detailed instructions.

### 4.3 Editing Farmer Profiles
Update information for already registered farmers.
*   [Placeholder: Link to a future section on editing farmer profiles, e.g., `03-editing-farmer-profile.md`]

### 4.4 Accessing and Completing Dynamic Forms
The app allows you to fill out various forms assigned for data collection.
*   See [Dynamic Forms on Mobile](./05-dynamic-forms-mobile.md) for detailed instructions.

### 4.5 GPS Data Capture
When registering plots or other geographical features, the app will use your device's GPS to capture location coordinates.
*   Ensure your device's GPS/Location Services are enabled and set to high accuracy.
*   [Placeholder: Tips for accurate GPS capture, e.g., be in an open area, wait for GPS lock.]

### 4.6 QR Code Scanning
The app may support QR code scanning for quick farmer identification or other purposes.
*   [Placeholder: Instructions on how to use QR code scanning feature if available.]

## 5. Offline Mode and Data Synchronization

A key feature of the DFR Mobile App is its ability to work offline.

*   **Offline Data Storage:** All data you collect (new registrations, form submissions, edits) is saved locally on your device. You can continue working even without an internet connection.
*   **Synchronization Process:** When an internet connection (Wi-Fi or mobile data) is available, you must synchronize your data with the central DFR server.
    1.  Navigate to the Sync section of the app (often indicated by a sync icon 🔄).
    2.  Tap the "Sync Now" or similar button.
    3.  The app will upload your pending data and download any updates or new forms from the server.
    *   [Placeholder: Image of sync screen/button - `assets/images/enumerator-manual/mobile-sync-screen.png`]
    *   Alt text: Mobile app data synchronization screen

    !!! success "Successful Sync"
        After a successful sync, your pending data count should be zero, and the app should indicate that it is up-to-date.

    !!! important "Regular Synchronization"
        It is crucial to synchronize your data regularly (e.g., at the end of each workday, or whenever a stable connection is available) to:
        *   Ensure your collected data is safely backed up on the server.
        *   Receive the latest updates, form definitions, and farmer data.
        *   Prevent data loss in case of device issues.

*   See [Data Synchronization](./06-data-synchronization.md) for more details and troubleshooting.

## 6. Language Selection

The DFR Mobile App may support multiple languages.

*   You can typically change the language in the app's **Settings** menu.
*   [Placeholder: Specific steps for language selection and list of supported languages for the country.]
*   [Placeholder: Image of language selection setting - `assets/images/enumerator-manual/mobile-language-setting.png`]
*   Alt text: Mobile app language selection setting

## 7. Battery and Data Usage Considerations

*   **Battery:** Using GPS and having the screen on for extended periods can consume battery.
    *   Carry a power bank if you expect long days in the field.
    *   Close the app when not actively using it for long durations.
    *   [Placeholder: Country-specific advice on battery management.]
*   **Data Usage:** Data synchronization will use your internet connection.
    *   Prefer Wi-Fi for large syncs if available.
    *   Be mindful of your mobile data plan. The app is designed to be efficient, but large amounts of data (especially photos, if supported) can consume more data.
    *   [Placeholder: Estimates of data usage per registration/form, if available.]

## 8. Basic Troubleshooting

If you encounter issues:

1.  **Check Internet Connection:** Ensure you have a stable internet connection if you are trying to sync or log in for the first time.
2.  **Restart the App:** Close the app completely and reopen it.
3.  **Restart Device:** Sometimes, restarting your mobile device can resolve minor issues.
4.  **Check Storage:** Ensure your device has sufficient internal storage space.
5.  **Sync Issues:**
    *   If sync fails, check error messages (if any).
    *   Try syncing again later with a better connection.
    *   Refer to the [Data Synchronization](./06-data-synchronization.md#troubleshooting-synchronization-issues) section.
6.  **Contact Support:** If problems persist, contact your supervisor or the designated DFR support team.
    *   [Placeholder: Contact details for national DFR support team.]

*   See [Troubleshooting Mobile App Issues](./07-troubleshooting-mobile.md) for more detailed guidance.

---

This overview provides a general guide. Specific features and workflows might vary slightly based on the app version and country-specific configurations. Always refer to training provided by your national DFR team.