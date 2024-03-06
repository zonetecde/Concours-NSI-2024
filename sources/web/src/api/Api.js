// @ts-nocheck
export default class Api {
	static api = pywebview.api;

	static openPythonProject = async (nom) => {
		Api.api.ouvrir_exercice(nom);
	};
}
