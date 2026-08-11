Update the appearance and visual design of the **existing Streamlit application** using the attached DLS logo as the primary visual reference.

### 1. Analyze Before Modifying

* First inspect the entire existing Streamlit application and understand its current UI structure, pages, components, navigation, forms, buttons, cards, tables, inputs, dialogs, and layouts.
* Do **not** change existing application functionality, business logic, workflows, API integrations, state management, or data processing.
* The task is strictly a **UI/UX and visual appearance enhancement** unless a small structural change is absolutely required to achieve the design.

### 2. Color Palette

Use the attached DLS logo as the source of truth for the application's visual identity.

Primary colors:

* DLS Blue: `#006FCF`
* White: `#FFFFFF`

Create a complementary neutral palette around these colors:

* Page/background: very light neutral/blue-tinted white
* Surface/cards: `#FFFFFF`
* Primary actions: `#006FCF`
* Primary hover/active state: a slightly darker blue derived from `#006FCF`
* Text: dark charcoal/navy for readability
* Secondary text: muted gray
* Borders/dividers: subtle light gray/blue
* Success/warning/error colors should remain semantically distinguishable and should not conflict with the DLS blue branding.

Do not introduce unrelated strong colors.

### 3. Overall Design Direction

Create a polished **enterprise-grade, modern, minimal, professional Streamlit UI** inspired by the DLS logo.

The UI should have:

* Clean white surfaces
* DLS blue used strategically for branding and primary actions
* Strong visual hierarchy
* Consistent spacing and alignment
* Rounded cards/containers where appropriate
* Subtle borders and shadows
* Modern typography
* Clear section separation
* Consistent button styling
* Professional form controls
* Minimal visual clutter

Avoid:

* Excessive gradients
* Excessive shadows
* Large decorative elements
* Random colors
* Overly rounded/cartoon-like components
* Heavy blue backgrounds covering the entire application
* Changing functionality just for visual purposes

### 4. Header / Branding

Use the provided DLS logo prominently but appropriately.

* Add the DLS logo to the application's primary header/navigation area where appropriate.
* Maintain the logo's aspect ratio.
* Do not distort, recolor, or modify the logo.
* Create a clean header that visually establishes the DLS branding.
* Use `#006FCF` as the primary brand accent.

If the application already has a header, improve its styling rather than unnecessarily creating a duplicate header.

### 5. Navigation

Improve the existing navigation experience while preserving its current behavior.

Apply:

* Clear active-page indication using DLS blue
* Consistent spacing
* Professional typography
* Subtle hover states
* Clean separators where appropriate

Do not remove existing navigation functionality.

### 6. Buttons

Standardize all buttons across the application.

Primary buttons:

* Background: `#006FCF`
* Text: white
* Subtle hover transition
* Consistent height, padding, border radius, and typography

Secondary buttons:

* White/light background
* DLS blue border/text
* Blue hover state

Danger/destructive buttons should retain an appropriate red semantic color rather than being converted to blue.

Ensure buttons look consistent throughout the application.

### 7. Input Fields and Forms

Improve all:

* Text inputs
* Select boxes
* File upload controls
* Date inputs
* Text areas
* Checkboxes
* Radio buttons
* Multiselect controls

Use:

* Clean white backgrounds
* Subtle borders
* Consistent border radius
* Clear labels
* DLS blue focus states
* Proper spacing between fields
* Consistent control heights

Focus states should use the DLS blue rather than Streamlit's default styling where possible.

### 8. Cards and Sections

Where the application currently presents logical sections, use clean cards/containers.

Cards should have:

* White background
* Subtle border
* Very light shadow
* Consistent padding
* Moderate border radius
* Clear heading hierarchy

Use DLS blue as an accent for:

* Section headers
* Icons
* Top borders
* Status indicators
* Important metrics

Do not overuse blue.

### 9. Tables and Data Presentation

Modernize existing tables/dataframes without changing their underlying data.

Use:

* Clean white surface
* Clear column headers
* Subtle row separators
* Appropriate hover states
* DLS blue for important headers or selected states
* Good horizontal/vertical spacing

Ensure tables remain readable and usable on different screen sizes.

### 10. Typography

Establish a consistent typography hierarchy:

* Application title: strong and prominent
* Page titles: clear and professional
* Section headings: medium/strong weight
* Body text: highly readable
* Helper text: smaller and muted

Avoid excessive font sizes and unnecessary uppercase text.

### 11. Status / Feedback Components

Improve:

* Success messages
* Warning messages
* Error messages
* Information messages
* Progress indicators
* Loading states

Maintain their semantic colors while styling their containers to match the DLS visual language.

### 12. Responsive Layout

Ensure the UI remains usable across:

* Desktop
* Laptop
* Smaller browser widths

Avoid unnecessary horizontal scrolling.

Use Streamlit columns and containers thoughtfully and preserve the application's existing responsive behavior.

### 13. Streamlit-Specific Styling

Inspect the existing CSS and Streamlit configuration before adding new styles.

Prefer:

* Centralized CSS/theme definitions
* Reusable style classes/components
* CSS variables for the color palette
* Minimal `unsafe_allow_html` usage
* Maintainable styling rather than large duplicated CSS blocks

For example, define the branding palette centrally:

```css
:root {
    --dls-blue: #006FCF;
    --dls-white: #FFFFFF;
    --dls-text: #1F2937;
    --dls-muted: #6B7280;
    --dls-border: #D9E2EC;
    --dls-background: #F7FAFC;
}
```

Adapt these values to the existing application architecture rather than blindly replacing existing styles.

### 14. Preserve Existing Functionality

This is critical.

DO NOT:

* Remove features
* Change business logic
* Change API calls
* Change database operations
* Change session/state behavior
* Change existing workflows
* Rename functional variables unnecessarily
* Remove existing pages/components unless explicitly required
* Break existing functionality to achieve visual changes

The final application should behave exactly as it did before, but with a significantly improved visual design.

### 15. Existing Project Conventions

Before making changes:

1. Identify the Streamlit entry point.
2. Identify reusable UI components.
3. Identify existing CSS/theme files.
4. Identify the current navigation implementation.
5. Identify page-specific styling.
6. Identify duplicated styling that can be consolidated.
7. Reuse the existing architecture wherever possible.

Do not create unnecessary files or restructure the project unless required.

### 16. Final Validation

After implementing the redesign:

* Run the Streamlit application.
* Verify that every page loads successfully.
* Verify navigation.
* Verify all buttons.
* Verify forms and inputs.
* Verify tables.
* Verify dialogs/modals.
* Verify file upload components.
* Verify error/success states.
* Verify that no existing functionality has been broken.
* Check for CSS conflicts and inconsistent styling.

### Expected Result

The final application should look like a polished **DLS-branded enterprise application**:

**DLS Blue `#006FCF` + White + clean neutral surfaces + modern typography + subtle borders/shadows + strong spacing + consistent components.**

The redesign should feel like a cohesive professional product rather than a collection of individually styled Streamlit components.

Most importantly, **use the attached DLS logo and its blue `#006FCF` as the visual source of truth, while preserving 100% of the application's existing functionality.**
