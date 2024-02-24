/**
 * Array contenant les fichiers audio en cours de lecture
 * @type {Array<HTMLAudioElement>}
 */
let playingAudios = [];

/**
 * @param {string} soundFile
 * @description - Joue un fichier audio
 */
export const PlayAudio = (soundFile) => {
	const audio = new Audio(soundFile);
	playingAudios.push(audio);
	audio.play();
	audio.onended = () => {
		playingAudios = playingAudios.filter((el) => el !== audio);
	};
};

/**
 * @param {string} soundFile
 * @description - Arrête la lecture du fichier audio
 */
export const StopAudio = (soundFile) => {
	const audio = playingAudios.find((el) => el.src.includes(soundFile));
	if (audio) {
		audio.pause();
		playingAudios = playingAudios.filter((el) => el !== audio);
	}
};

/**
 * @param {KeyboardEvent} event
 * @description - Joue un fichier audio en fonction de la touche pressée
 **/
export const keyDownAudio = (event) => {
	if (event.key.length === 1 && event.key !== ' ') PlayAudio('/audio/key1_press.mp3');
	else if (event.key === 'Enter') PlayAudio('/audio/key1_enter_press.mp3');
	else if (event.key === 'Backspace') PlayAudio('/audio/key1_return_press.mp3');
	else if (event.key === ' ') PlayAudio('/audio/key1_space_press.mp3');
};

/**
 * @param {KeyboardEvent} event
 * @description - Joue un fichier audio en fonction de la touche relâchée
 **/
export const keyUpAudio = (event) => {
	if (event.key.length === 1 && event.key !== ' ') PlayAudio('/audio/key1_release.mp3');
	else if (event.key === 'Enter') PlayAudio('/audio/key1_enter_release.mp3');
	else if (event.key === 'Backspace') PlayAudio('/audio/key1_return_release.mp3');
	else if (event.key === ' ') PlayAudio('/audio/key1_space_release.mp3');
};
