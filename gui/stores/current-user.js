import {writable} from "svelte/store"

const currentUserStore = writable(null)

export default currentUserStore
