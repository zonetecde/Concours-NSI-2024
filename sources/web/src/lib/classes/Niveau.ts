export interface Niveau {
	Nom: string;
	Audio: string;
	Difficulte: number;
	Touches: Touche[];
}

export interface Touche {
	key: string;
	hold_time: number;
	hold: boolean;
	time: number;
}
