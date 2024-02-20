export default class JeuBacRow {
	completer = false; // Le joueur a-t-il complété la ligne ? Si oui, on ne peut plus la modifier

	/**
	 * @param {string} lettre
	 * @param {Mot[]} cols
	 **/
	constructor(lettre, cols = []) {
		this.lettre = lettre;
		this.cols = cols;
	}
}

export class Mot {
	/** @type {string | null} **/
	valide = null; // Le mot est-il valide ou non ?

	/** @type {string} **/
	theme = ''; // Le thème du mot

	/** @type {string} **/
	mot = ''; // Le mot entré par le joueur

	/**
	 * @param {string} theme
	 **/
	constructor(theme) {
		this.theme = theme;
	}
}
