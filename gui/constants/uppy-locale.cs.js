export default {
	strings: {
		// When `inline: false`, used as the screen reader label for the button that closes the modal.
		closeModal: "Zavřít okno",
		// Used as the screen reader label for the plus (+) button that shows the “Add more files” screen
		addMoreFiles: "Přidat více souborů",
		// TODO
		addingMoreFiles: "Přídává se více souborů",
		// Used as the header for import panels, e.g., “Import from Google Drive”.
		importFrom: "Importovat z %{name}",
		// When `inline: false`, used as the screen reader label for the dashboard modal.
		dashboardWindowTitle: "Uppy přehledové okno (ESC k ukončení)",
		// When `inline: true`, used as the screen reader label for the dashboard area.
		dashboardTitle: "Uppy přehled",
		// Shown in the Informer when a link to a file was copied to the clipboard.
		copyLinkToClipboardSuccess: "Odkaz zkopírován",
		// Used when a link cannot be copied automatically — the user has to select the text from the
		// input element below this string.
		copyLinkToClipboardFallback: "Kopírovat odkaz níže",
		// Used as the hover title and screen reader label for buttons that copy a file link.
		copyLink: "Kopírovat odkaz",
		// Used as the hover title and screen reader label for file source icons, e.g., “File source: Dropbox”.
		fileSource: "Zdroj souboru: %{name}",
		// Used as the label for buttons that accept and close panels (remote providers or metadata editor)
		done: "Hotovo",
		// TODO
		back: "Zpět",
		// Used as the screen reader label for buttons that remove a file.
		removeFile: "Odebrat soubor",
		// Used as the screen reader label for buttons that open the metadata editor panel for a file.
		editFile: "Editovat soubor",
		// Shown in the panel header for the metadata editor. Rendered as “Editing image.png”.
		editing: "Editovaný soubor: %{file}",
		// Text for a button shown on the file preview, used to edit file metadata
		edit: "Editovat",
		// Used as the screen reader label for the button that saves metadata edits and returns to the
		// file list view.
		finishEditingFile: "Dokončit úpravu souboru",
		// TODO
		saveChanges: "Uložit změny",
		// Used as the label for the tab button that opens the system file selection dialog.
		myDevice: "Moje zařízení",
		// Shown in the main dashboard area when no files have been selected, and one or more
		// remote provider plugins are in use. %{browse} is replaced with a link that opens the system
		// file selection dialog.
		dropPasteImport: "%{dropPaste} nebo naimportujte",
		// Shown in the main dashboard area when no files have been selected, and no provider
		// plugins are in use. %{browse} is replaced with a link that opens the system
		// file selection dialog.
		dropPaste: "%{dropHint}, vložte nebo %{browse}",
		// TODO
		dropHint: "Přetáhněte sem soubory",
		// This string is clickable and opens the system file selection dialog.
		browse: "Procházet",
		// Used as the hover text and screen reader label for file progress indicators when
		// they have been fully uploaded.
		uploadComplete: "Nahrávání dokončeno",
		// TODO
		uploadPaused: "Nahrávání pozastaveno",
		// Used as the hover text and screen reader label for the buttons to resume paused uploads.
		resumeUpload: "Obnovit nahrávání",
		// Used as the hover text and screen reader label for the buttons to pause uploads.
		pauseUpload: "Pozastavit nahrávání",
		// Used as the hover text and screen reader label for the buttons to retry failed uploads.
		retryUpload: "Nahrát znovu",
		// Used as the hover text and screen reader label for the buttons to cancel uploads.
		cancelUpload: "Nahrávání zrušeno",

		// Used in a title, how many files are currently selected
		xFilesSelected: {
			0: "%{smart_count} soubor vybrán",
			1: "%{smart_count} soubory vybrané",
			2: "%{smart_count} souborů vybraných"
		},
		// TODO
		uploadingXFiles: {
			0: "Nahrává se %{smart_count} soubor",
			1: "Nahrávají se %{smart_count} soubory",
			2: "Nahrává se %{smart_count} souborů"
		},
		// TODO
		processingXFiles: {
			0: "Zpracovává se %{smart_count} soubor",
			1: "Zpracovávájí se %{smart_count} soubory",
			2: "Zpracovává se %{smart_count} souborů"
		},

		// The "powered by Uppy" link at the bottom of the Dashboard.
		// **NOTE**: This string is called `poweredBy2` for backwards compatibility reasons.
		// See https://github.com/transloadit/uppy/pull/2077
		poweredBy2: "Powered by %{uppy}",

		// @uppy/status-bar strings:
		uploading: "Nahrává se",
		complete: "Dokončeno"
		// ...etc
	}
}
