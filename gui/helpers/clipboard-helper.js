export function copyToClipboard(text) {
	return navigator.clipboard.writeText(text)
}

export function readFromClipboard() {
	return navigator.clipboard.readText()
}
