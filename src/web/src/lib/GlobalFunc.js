/**
 * @param {string} soundFile
 * @description - Joue un fichier audio
 */
export const PlayAudio = (soundFile) => {
	const audio = new Audio(soundFile);
	audio.play();
};
