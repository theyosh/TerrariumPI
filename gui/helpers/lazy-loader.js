import {leaveLoaderFor, waitForLoader} from "../constants/ui"
import {emptyPromise} from "./promise-helpers"

export default function lazyLoader(resourceTask, showLoader, hideLoader) {
	if (!(resourceTask instanceof Promise))
		return emptyPromise

	let loaderShowed = false
	const beforeShowTimer = setTimeout(() => {
		loaderShowed = new Date()
		showLoader()
	}, waitForLoader)

	return resourceTask
		.then(res => {
			if (!loaderShowed) {
				clearTimeout(beforeShowTimer)
				hideLoader()
				return res
			}

			if (new Date() - loaderShowed > leaveLoaderFor) {
				hideLoader()
				return res
			}

			// this leaves the loader showed for additional time
			return new Promise(resolve => {
				setTimeout(() => {
					hideLoader()
					resolve(res)
				}, leaveLoaderFor - (new Date() - loaderShowed))
			})
		})
		.catch(err => {
			hideLoader()
			throw err
		})
}
