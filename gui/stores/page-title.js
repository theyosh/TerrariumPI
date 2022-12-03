import {writable} from "svelte/store"
import {setHtmlTitle} from "../helpers/router-html-title"

export const pageTitle = writable()
export let customPageTitleUsed = writable(false)

export function setCustomPageTitle(title) {
	pageTitle.set(title)
	customPageTitleUsed.set(true)
}

export function listenPageTitleChanged() {
	return pageTitle.subscribe(title => {
		setHtmlTitle(title)
	})
}
