# Parkinson's Toolkit - Content Repository

This repository contains the content files for the **Parkinson's Toolkit app** - a web application designed to provide evidence-based information and support for people living with Parkinson's disease, their families, and caregivers.

## Content Management

**Easy Updates**: Content maintainers can edit the markdown files in `./pages-content` in this repository. Changes are automatically reflected in the web application without requiring redeployments.

**Separation of Concerns**:

- **Text content** lives here as markdown files
- **Images** are stored in the web app repository and positioned via CSS
- **Navigation structure** is defined in `navigation.json`

## Web Application Integration

This content repository is designed to be dynamically consumed by a web application:

- **Markdown files** are fetched from GitHub and rendered in real-time
- **Content updates** are immediate - no build process required

### Content Categories

Content is organized into 12 main categories:

- **Information** - Core Parkinson's knowledge
- **Wellbeing** - Health and lifestyle guidance
- **Management** - Medical and symptom management
- **Daily Life** - Practical living advice
- **Support** - Emotional and family support
- **Legal/Financial** - Practical planning matters
- **Treatment** - Medical treatments and teams
- **Healthcare** - Medical appointments and care
- **Planning** - Future care planning
- **Activities** - Work, hobbies, and interests
- **Resources** - Additional support and information
- **Special** - Specific topics like COVID-19
