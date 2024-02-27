/**
 * La classe JeuBacRow représente une ligne de la grille du jeu du Bac.
 * Elle contient une lettre et une liste de mots entrés par les joueurs.
 */
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

/**
 * La classe Mot représente un mot entré par un joueur dans une grille du jeu du Bac.
 * L'attribut "valide" est null si le mot n'a pas encore été validé, "true" si le mot est valide et "false" s'il ne l'est pas.
 */
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
