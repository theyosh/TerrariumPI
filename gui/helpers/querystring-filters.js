import {parse, stringify} from "qs"

export const stringifyFilters = (filters, newFilters, partial = false, mapper = (x => x)) => {
	let theFilters = partial
		? {
			...filters,
			...newFilters
		}
		: newFilters

	const mappedFilters = mapper(theFilters)

	Object.keys(mappedFilters)
		.forEach(key => {
			if (!mappedFilters[key])
				delete mappedFilters[key]
		})

	return stringify(mappedFilters)
}

export const parseQuerystringFilters = (querystring, parser = (x => x)) => {
	if (!querystring)
		return parser({})

	const qsParsed = parse(querystring)

	return parser(qsParsed)
}
