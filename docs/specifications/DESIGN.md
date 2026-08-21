---
name: Stitch
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#454652'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f1'
  outline: '#767683'
  outline-variant: '#c6c5d4'
  surface-tint: '#4c56af'
  primary: '#000666'
  on-primary: '#ffffff'
  primary-container: '#1a237e'
  on-primary-container: '#8690ee'
  inverse-primary: '#bdc2ff'
  secondary: '#b6171e'
  on-secondary: '#ffffff'
  secondary-container: '#da3433'
  on-secondary-container: '#fffbff'
  tertiary: '#301300'
  on-tertiary: '#ffffff'
  tertiary-container: '#4f2400'
  on-tertiary-container: '#ec7700'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e0e0ff'
  primary-fixed-dim: '#bdc2ff'
  on-primary-fixed: '#000767'
  on-primary-fixed-variant: '#343d96'
  secondary-fixed: '#ffdad6'
  secondary-fixed-dim: '#ffb3ac'
  on-secondary-fixed: '#410003'
  on-secondary-fixed-variant: '#930010'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb786'
  on-tertiary-fixed: '#311300'
  on-tertiary-fixed-variant: '#723600'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 44px
    fontWeight: '800'
    lineHeight: 52px
    letterSpacing: -1px
  headline-lg:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 30px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
  status-code:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '900'
    lineHeight: 16px
    letterSpacing: 1px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  margin-sm: 16px
  margin-md: 24px
  margin-lg: 32px
  gutter: 16px
  touch-target: 48px
---

## Brand & Style
The design system is engineered for high-stakes emergency management and public safety coordination. The brand personality is authoritative, resilient, and ultra-reliable. It prioritizes clarity over decoration, ensuring that personnel under extreme stress can process information instantaneously.

The design style is **Corporate / Modern** with a lean toward **High-Contrast / Utility**. It employs a structured, institutional aesthetic that mirrors physical emergency equipment—solid, dependable, and functional. Whitespace is used strategically to separate critical data streams, and visual flourishes are removed to prevent cognitive overload. The emotional response is one of calm control and institutional trust.

## Colors
The palette is rooted in established safety standards to ensure immediate recognition of status and urgency.

- **Primary (Deep Navy):** Used for global navigation, headers, and institutional branding. It establishes a "source of truth" and authority.
- **Emergency Red:** Reserved strictly for active hazards, life-threatening alerts, and critical stop actions.
- **Warning Orange:** Used for situational awareness, pending threats, and medium-priority notifications.
- **Safety Green:** Indicates cleared routes, successful deployments, and safe zones.
- **Neutrals:** A spectrum of cool greys and off-whites provides a non-distracting canvas for high-contrast data visualization.

The default mode is **Light**, optimized for high-glare outdoor environments where emergency responders typically operate.

## Typography
Typography is the primary tool for information hierarchy. This design system utilizes **Atkinson Hyperlegible Next** for headlines to ensure maximum readability for visually impaired users and those in low-light conditions. **Inter** is used for functional body text and data entry due to its neutral, systematic clarity.

- **Scale:** Use larger font sizes than standard consumer apps to accommodate rapid scanning.
- **Contrast:** Ensure all text-to-background ratios exceed WCAG AAA standards for critical information.
- **Emphasis:** Bold weights are used for status indicators and instructional labels to differentiate them from static content.

## Layout & Spacing
The layout follows a **Fluid Grid** model with strict adherence to an 8px base unit, ensuring consistent rhythm across ruggedized tablets and mobile devices.

- **Margins:** A minimum safe margin of 16px (mobile) or 32px (tablet/desktop) is maintained to prevent content from hitting device edges.
- **Touch Targets:** All interactive elements must maintain a minimum height/width of 48px to allow for use with gloved hands or in high-vibration environments (e.g., inside a vehicle or helicopter).
- **Responsive Behavior:** On mobile, columns stack vertically. On tablets, a split-view pattern is preferred, keeping the map or primary data feed visible while secondary controls occupy a side drawer.

## Elevation & Depth
In this design system, depth is used to indicate structural importance rather than aesthetic flourish.

- **Low-Contrast Outlines:** Surfaces are primarily separated by 1px solid borders in #E0E0E0. This creates a "blueprint" feel that is robust and legible.
- **Tonal Layers:** The background uses #F5F5F5, while active work surfaces use pure #FFFFFF. 
- **Shadows:** Avoid soft, ambient shadows. If elevation is required for a floating action button or modal, use a crisp, high-opacity 4px "drop" shadow to maintain the solid, physical feel of the UI.
- **State Indicators:** Use thick (4px) colored left-borders on cards to indicate urgency (e.g., a red border for an active disaster card).

## Shapes
Shapes are disciplined and "Soft" (0.25rem / 4px). This subtle rounding removes the harshness of sharp corners for better visual flow while maintaining a professional, institutional silhouette.

- **Standard Elements:** Buttons, input fields, and cards use a 4px corner radius.
- **Status Badges:** Use a slightly higher radius (8px) to distinguish them from structural elements.
- **Interactive Icons:** Should be contained within square or circular containers to provide clear, predictable tap areas.

## Components
Components are designed for high-visibility and error-reduction.

- **Buttons:** Primary buttons use the Deep Navy background with white text. Critical action buttons (e.g., "Dispatch") use Emergency Red. All buttons must have a height of at least 56px for emergency accessibility.
- **Input Fields:** Use thick 2px borders when focused. Labels must remain visible at all times (no disappearing placeholders) to prevent data entry errors.
- **Cards:** Used for incident reports. They must include a clear header, a status badge in the top right, and high-contrast primary text.
- **Chips/Badges:** Used for categorization (e.g., "Flood", "Fire"). These use a light tint of the category color with high-contrast dark text.
- **Status Indicators:** Use "Blinking State" indicators (a pulsating dot) next to "Live" data feeds to confirm the system is actively receiving updates.
- **Map Controls:** Floating, high-contrast circular buttons with thick borders to ensure visibility against complex satellite imagery.