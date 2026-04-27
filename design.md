---
name: Flowrix3D Design System
colors:
  surface: '#fcf8fb'
  surface-dim: '#dcd9dc'
  surface-bright: '#fcf8fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7ea'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#4c4546'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#7e7576'
  outline-variant: '#cfc4c5'
  surface-tint: '#5e5e5e'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#1b1b1b'
  on-primary-container: '#848484'
  inverse-primary: '#c6c6c6'
  secondary: '#635e57'
  on-secondary: '#ffffff'
  secondary-container: '#e9e1d8'
  on-secondary-container: '#69645d'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#1a1e00'
  on-tertiary-container: '#81893f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c6'
  on-primary-fixed: '#1b1b1b'
  on-primary-fixed-variant: '#474747'
  secondary-fixed: '#e9e1d8'
  secondary-fixed-dim: '#cdc5bd'
  on-secondary-fixed: '#1e1b16'
  on-secondary-fixed-variant: '#4b4640'
  tertiary-fixed: '#e1e994'
  tertiary-fixed-dim: '#c4cd7b'
  on-tertiary-fixed: '#1a1e00'
  on-tertiary-fixed-variant: '#444b05'
  background: '#fcf8fb'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
spacing:
  container-max: 1280px
  gutter: 1.5rem
  margin-mobile: 1rem
  stack-sm: 0.5rem
  stack-md: 1.5rem
  stack-lg: 4rem
  section-padding: 8rem
---

## Brand & Style

This design system is defined by architectural precision and a high-end, gallery-like aesthetic. It targets a sophisticated audience that values clarity, technical excellence, and "quiet luxury." The visual language is strictly minimalist, stripping away all decorative elements to focus entirely on the product and content.

The style is a blend of **Minimalism** and **Modern Corporate**, emphasizing a flat hierarchy. By avoiding depth cues like shadows and gradients, the UI relies on spatial relationships, deliberate whitespace, and hairline strokes to establish structure. The resulting atmosphere is one of effortless confidence and premium utility.

## Colors

The color strategy uses a monochrome foundation to ensure the 3D assets and products remain the focal point.

- **Primary Action:** Pure Solid Black (#000000) is reserved exclusively for high-priority calls to action, creating a powerful focal point against the white canvas.
- **Surface Palette:** Pure White (#FFFFFF) serves as the primary canvas, while Light Gray (#F5F5F7) is utilized for secondary sections, sidebar backgrounds, and metadata containers to provide subtle structural separation without introducing heavy visual weight.
- **Typography:** Off-black (#1D1D1F) is used for body text to maintain high legibility while appearing softer and more premium than pure black. Secondary information uses Muted Gray (#86868B).
- **Accents:** The tertiary color (#A5AD5F) is applied sparingly for status indicators or subtle promotional tags, maintaining brand fidelity with the source identity.

## Typography

This design system utilizes **Inter** for its sharp, systematic clarity and excellent legibility at all scales. The type hierarchy is designed to be functional and unobtrusive.

Headlines should use tighter letter spacing and a medium-to-bold weight to command attention, while body text maintains a generous line height for comfortable reading. All caps are used selectively for labels and navigation items to provide a technical, structured feel. Avoid using italic styles unless strictly necessary for editorial distinction.

## Layout & Spacing

The layout follows a **Fixed-width Grid** philosophy, compatible with Bootstrap's 12-column system. It prioritizes "Ample Whitespace" to convey a premium feel.

- **Grid:** Use a 12-column layout with a 24px (1.5rem) gutter.
- **Rhythm:** Vertical spacing should be generous. Use a base 8px unit for small adjustments, but jump to 64px or 128px for section breaks to create a sense of openness.
- **Alignment:** All elements should align strictly to the grid. Use 1-pixel hairline borders (#E5E5EA) to define regions where whitespace alone is insufficient for clarity.

## Elevation & Depth

This design system explicitly rejects shadows and traditional depth. Instead, it uses **Low-contrast Outlines** and **Tonal Layering**.

- **Surfaces:** Depth is suggested by placing #FFFFFF elements on #F5F5F7 backgrounds.
- **Borders:** A consistent 1px solid border in #E5E5EA is the primary tool for containment.
- **Interactions:** Hover states should be indicated by subtle color shifts (e.g., background moving from white to light gray) rather than lifting the element with a shadow.
- **Drawers:** Offcanvas elements (Cart/Account) should slide over the main content with a solid #FFFFFF fill and a 1px border on the leading edge. Use a 20% opacity black overlay for the background dimming to keep the focus sharp.

## Shapes

To maintain a "Sharp" and "Premium" appearance, the design system utilizes a **0px border-radius (Sharp)** across all primary components.

This geometric rigidity reinforces the 3D and architectural nature of the brand. All buttons, input fields, product cards, and offcanvas drawers must have perfectly square corners. This creates a high-contrast, modern look that distinguishes the product from softer, mass-market e-commerce sites.

## Components

### Buttons
- **Primary:** Solid Black (#000000) background, white text, 0px radius. High-padding (16px 32px).
- **Secondary:** Transparent background, 1px border (#E5E5EA), Off-black text.
- **Ghost:** No border or background, underline on hover.

### Product Grids
- Clean 3-column or 4-column layout.
- Images should have a light gray background (#F5F5F7) or be isolated on white.
- Text labels (Product Name, Price) sit below the image with no card container border.

### Sidebar Filters
- Located on the left, using #F5F5F7 as a full-height background.
- Typography for headers should be `label-caps`.
- Checkboxes are simple 16px squares with a black fill when active.

### Offcanvas Drawers
- Used for Cart and Account.
- Slides out from the right.
- Header includes a simple "Close" text link or an outline "X" icon.
- Contents are stacked with thin horizontal separators.

### Inputs
- 1px border (#E5E5EA) on all four sides.
- Placeholder text in #86868B.
- Focus state: border color changes to #000000. No glow or outer shadow.
