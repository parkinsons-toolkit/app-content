# Parkinson's Toolkit - Content Repository

This repository contains the content files for the [Parkinson's Toolkit app](https://github.com/parkinsons-toolkit/parkinsons-toolkit-app) - a web application designed to provide evidence-based information and support for people living with Parkinson's disease, their families, and caregivers.

## Content Management

### Adding text content

Content maintainers can edit the markdown files in `./pages-content` in this repository. Changes are automatically reflected in the web application without requiring redeployments.

Make sure the name of the `.md` file is the same as the URL you would like the page to be accessed from in the app. For example, the file `what-is-parkinsons.md` would be accessed in the web app from `app-domain/what-is-parkinsons`. Use dashes `-` as separators and avoid using special characters.

### Adding links

#### Internal Links (To Other Pages on Our Site)

Use HTML <a> tags with the `internal-link` class:

&lt;a href="/learn/what-is-parkinsons" class="internal-link"&gt;What is Parkinson's&lt;/a&gt;

&lt;a href="/learn/managing-symptoms/tremor" class="internal-link"&gt;Tremor&lt;/a&gt;

#### External Links (To Other Websites)

Use HTML <a> tags with the `external-link` class:

&lt;a href="https://www.parkinsons.org.uk" class="external-link" target="\_blank" rel="noopener noreferrer"&gt;Parkinson's UK&lt;/a&gt;

&lt;a href="https://www.nhs.uk/conditions/parkinsons-disease" class="external-link" target="\_blank" rel="noopener noreferrer"&gt;NHS Information&lt;/a&gt;

_Note_: The `target="_blank" rel="noopener noreferrer` makes sure the link opens in a new tab. Simply remove those attributes if opening in a new tab is not desired.

### Adding image content

Images can be stored in `./images` and inserted into the markdown files directly with:

`<img src="https://raw.githubusercontent.com/parkinsons-toolkit/app-content/refs/heads/dev/images/linked-image-name.png" alt="example-alt-text" class="example-class">`

The branch name in the image URL will automatically be replaced with either `main` or `dev` during the web application runtime.

### Adding video content

Videos can be pulled in from external sources such as embedded YouTube videos. These can be inserted as an `iframe` with e.g:

```
<div class="video-container">
<iframe
  width="560"
  height="315"
  src="https://www.youtube-nocookie.com/embed/ikVplhl5zZw"
  title="YouTube video player"
  allowfullscreen>
</iframe>
</div>
```

To get the above embed link in YouTube, go to the YouTube video and click 'Share' - then select the 'embed' button to copy the embed link.

_Note_: If there is a query string (denoted with a ?) in the embed URL like this: `exampleurl?si=abc123` then make sure to remove everything from the ? onwards, otherwise the link won't work. See this relevant [issue ticket](https://github.com/parkinsons-toolkit/parkinsons-toolkit-app/issues/50#issuecomment-3159753051) for more information.

_Note_: The `no-cookie` part of the url ensures the video embed respects enhanced privacy features and does not load cookies until the user interacts with the video.

## Security Guidelines for Content Contributors

⚠️ **IMPORTANT**: This repository supports HTML within markdown to enable rich content (videos, styled elements). Please follow these security guidelines:

**✅ SAFE PRACTICES:**

- Use standard markdown syntax for text, headers, lists, and links
- Embed YouTube videos using provided HTML templates
- Add images using standard markdown image syntax

**❌ NEVER ADD:**

- `<script>` tags or JavaScript code
- Event handlers (`onclick`, `onload`, `onmouseover`, etc.)
- Form elements (`<form>`, `<input>`, `<button>` with actions)
- External iframes from non-approved domains
- Suspicious or unfamiliar HTML code from external sources

**🔍 REVIEW PROCESS:**

- All content changes require pull request review
- Reviewers should check for suspicious HTML elements
- When in doubt, ask the development team about HTML additions
- Test content locally when possible before submitting

**📋 APPROVED HTML ELEMENTS:**

- `<div class="video-container">` for YouTube embeds
- `<iframe src="https://www.youtube-nocookie.com/embed/...">` for approved videos
- `<img>` tags with GitHub raw URLs for images
- Basic styling divs with approved CSS classes

If you need to add new HTML elements or are unsure about content safety, please consult with the development team first.

## Web Application Integration

This content repository is designed to be dynamically consumed by a web application:

- **Markdown files** are fetched from GitHub and rendered in real-time
- **Content updates** are immediate - no build process required

## Use of git branches

Use the `dev` branch to test out new content ideas.

When you are happy, open a pull request to merge your changes into `main`.

The web application will automatically use the content from the `dev` branch for local development and `main` during production.
