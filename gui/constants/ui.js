export const TypingDebounceDelay = 300

// these constants are used for rendering loading notifications
// do not show loader if response arrives before `waitForLoader` time
// and do not hide loader, if the response arrives after `waitForLoader` and before `leaveLoaderFor`
export const waitForLoader = 45
export const leaveLoaderFor = 234

export const BaseHtmlTitle = process.env.BASE_HTML_TITLE