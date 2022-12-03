import { Toastr } from "svelte-adminlte"

import {nl2br} from "../helpers/string-helpers"

const Opts = {
  newestOnTop: true,
  positionClass: "toast-top-right",
  showDuration: "300",
  hideDuration: "1000",
  preventDuplicates: true,
	timeOut: "4000",
  extendedTimeOut: "1500",
  showEasing: "swing",
  hideEasing: "linear",
  showMethod: "fadeIn",
  hideMethod: "fadeOut"
}

export const successNotification = (message, title = null, options = {}) => {
	Toastr.success(nl2br(message), title, {...Opts,...options})
}

export const warningNotification = (message, title = null, options = {}) => {
	Toastr.warning(nl2br(message), title, {...Opts,...options})
}

export const errorNotification = (message, title = null, options = {}) => {
	Toastr.error(nl2br(message), title, {...Opts,...options})
}