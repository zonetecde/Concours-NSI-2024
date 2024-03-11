<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Api from '../../../api/Api';
	import { PlayAudio } from '$lib/GlobalFunc';

	/** @type {Array<import('$lib/classes/Niveau').Niveau>} */
	let niveaux = []; // Niveaux

	/** @type {import('$lib/classes/Niveau').Niveau} */
	let selectedLevelObj;

	/** @type {number} */
	let audioPosition = 0;

	/** @type {number} */
	let score = 0;

	/** @type {number} */
	let scoreMax = 0;

	/** @type {Array<string>} */
	let keys = [];

	/** @type {Array<string>} */
	let keyboardLayout = ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n'];

	/** @type {Array<string>} */
	let touchesAppuyees = []; // Les touches actuellement appuyées

	/** @type {HTMLAudioElement} */
	let audio;

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {string} */
	let selectedLevelName = 'Blue Ocean'; // Niveau sélectionné

	/** @type {boolean} */
	let hasExerciceEnded = false; // L'exercice est terminé ?

	onMount(async () => {
		window.addEventListener('keydown', keyDown);
		window.addEventListener('keyup', keyUp);

		// Récupère le niveau sélectionné depuis python
		niveaux = await Api.api.recuperer_niveaux_rythme();

		startExercice();
	});

	/**
	 * Appelée lorsqu'une touche est relâchée
	 * @param {KeyboardEvent} event
	 */
	function keyUp(event) {
		if (hasExerciceStarted) {
			// Enlève la touche appuyée
			touchesAppuyees = touchesAppuyees.filter((touche) => touche !== event.key);
		}
	}

	/**
	 * Appelée lorsqu'une touche est appuyée
	 * Si la touche est ENTRÉE et que l'exercice n'a pas encore commencé, démarre l'exercice
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		if (event.key === 'Enter' && !hasExerciceStarted) {
			startExercice();
		} else if (hasExerciceStarted) {
			// Vérifie si la touche appuyée est dans les touches à appuyer pour le temps actuel
			const touche = selectedLevelObj.Touches.find((touche) => touche.key === event.key && Math.abs(audioPosition - touche.time) < 0.35 + (touche.hold ? touche.hold_time * 0.3 : 0));

			if (touche) {
				// Si la touche est déjà appuyée, on ne fait rien
				if (touchesAppuyees.includes(event.key)) return;

				// Ajoute la touche appuyée
				touchesAppuyees.push(event.key);

				if (!touche.hold) {
					// Score +1
					score++;
				} else {
					// Regarde si elle est toujours appuyée après le temps de maintien
					setTimeout(() => {
						if (touchesAppuyees.includes(event.key)) {
							score++;
						}
					}, touche.hold_time * 0.5 * 1000 - (audioPosition - touche.time) * 1000); // Au moins la moiitié du temps de maintien
				}
			} else {
				// Touche appuyée au mauvais moment
				//PlayAudio('/audio/pop_sound.mp3');
			}
		}
	}

	function startExercice() {
		hasExerciceStarted = true;

		const niv = niveaux.find((niveau) => niveau.Nom === selectedLevelName);
		if (niv) {
			scoreMax = niv.Touches.length;
			selectedLevelObj = niv;

			// Récupère les touches du clavier dans le bon ordre
			keys = selectedLevelObj.Touches.map((touche) => touche.key);
			// Distinct
			keys = keys.filter((value, index, self) => self.indexOf(value) === index);
			// Les tries dans l'ordre du clavier
			keys.sort((a, b) => keyboardLayout.indexOf(a) - keyboardLayout.indexOf(b));

			// Joue le son
			audio = new Audio(`/audio/rythme/${selectedLevelObj.Audio}`);
			audio.play();

			const int = setInterval(() => {
				audioPosition = audio.currentTime;
			}, 10);

			// quand l'audio est terminé
			audio.onended = () => {
				clearInterval(int);
				setTimeout(() => {
					hasExerciceEnded = true;
				}, 1000);
			};
		}
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
		window.removeEventListener('keyup', keyUp);
		audio.pause();
	}
</script>

<div class="flex px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl mb-6 mt-7">Rythme</h1>

		<Exercice image="/keyboard/reaction.jpg" nom="Rythme" handleClick={startExercice} />

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">Règles de l'exercice :</p>
			<p class="text-lg">
				Des carrés tomberons du haut de l'écran, appuyez sur la touche correspondante lorsque le carré touche la ligne d'arrivée. <br />Si le carré se prolonge, appuyez sur la touche correspondante au
				moment où il commence à toucher la ligne jusqu'à ce qu'il finisse de tomber entièrement.
			</p>
		</div>

		<div class="md:w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl">
			<div class="flex flex-col w-full">
				<p class="pr-2">Niveaux :</p>

				<div class="flex gap-x-8">
					{#each niveaux as niveau}
						<label for={niveau.Nom}><input type="radio" bind:group={selectedLevelName} id={niveau.Nom} name="niveau" class="mr-2" value={niveau.Nom} />{niveau.Nom}</label>
					{/each}
				</div>
			</div>
		</div>

		<p class="mt-8 mb-5">Appuyez sur ENTRÉE pour commencer l'exercice</p>
	{:else}
		<div class="w-[450px] h-[600px] bg-[#84af80] outline-4 rounded-xl outline-[#206442] outline relative">
			<!-- Barre d'appuie -->
			<div class="absolute border-y-2 border-[#206442] bg-[#ffffff2d] bottom-[90px] h-[40px] w-full" />

			<div class="overflow-hidden w-full h-full grid absolute bottom-0 divide-x-2 divide-[#206442]" style={`grid-template-columns: repeat(${keys.length}, minmax(0, 1fr))`}>
				{#each keys as key}
					<div class="w-full h-full flex justify-center items-center relative">
						{#each selectedLevelObj.Touches as touche}
							{#if touche.key === key}
								<div
									class="w-10 h-10 rounded-full absolute key"
									style={`height: ${touche.hold ? touche.hold_time * 120 : '40'}px;
									
									top: ${audioPosition >= touche.time - 4 ? `calc(100% + ${touche.hold_time * 120}px)` : `calc(-10% - ${touche.hold_time * 120}px)`}; transition-duration: ${
										touche.time - audioPosition + 1 + (touche.hold ? touche.hold_time * 1.55 : 0)
									}s; ${
										Math.abs(audioPosition - touche.time) < (touche.hold ? touche.hold_time * 0.5 : 0.1) && touchesAppuyees.includes(key) ? 'background-color: red;' : 'background-color: #4d4bd4;'
									}`}
								/>
							{/if}
						{/each}

						<p class="text-3xl absolute bottom-[90px] font-bold">{key.toUpperCase()}</p>
					</div>
				{/each}
			</div>
		</div>

		<div class="absolute top-5 w-full flex justify-between items-center px-8">
			<p class="text-2xl">Score : {score}</p>
			<p class="text-2xl">Temps restant : {Math.round(selectedLevelObj.Duree - audioPosition)}</p>
		</div>
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>

<style>
	.key {
		transition: top 1s linear, background-color 0.03s ease;
	}
</style>
