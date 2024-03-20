<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Api from '../../../api/Api';
	import { PlayAudio } from '$lib/GlobalFunc';
	import { fade } from 'svelte/transition';

	/** @type {Array<import('$lib/classes/Niveau').Niveau>} */
	let niveaux = []; // Les différents niveaux récupérés depuis python

	/** @type {import('$lib/classes/Niveau').Niveau} */
	let selectedLevelObj; // Le niveau sélectionné

	/** @type {number} */
	let audioPosition = 0; // La position actuelle de l'audio

	/** @type {number} */
	let score = 0; // Le score actuel

	/** @type {number} */
	let scoreMax = 0; // Le score maximum possible

	/** @type {Array<string>} */
	let keys = []; // Les lettres dans l'ordre du clavier

	/** @type {Array<any>} */
	let keysScored = []; // Les lettres déjà scorés

	/** @type {Array<string>} */
	let keyboardLayout = ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n']; // Le layout du clavier pour trier les touches dans l'ordre

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

	/**
	 * Appelée lorsque la fenêtre est chargée
	 * Récupère les niveaux depuis python
	 */
	onMount(async () => {
		window.addEventListener('keydown', keyDown);
		window.addEventListener('keyup', keyUp);

		// Récupère le niveau sélectionné depuis python
		niveaux = await Api.api.recuperer_niveaux_rythme();

		//startExercice();
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
	 * Sinon, vérifie si la touche appuyée est dans les touches à appuyer pour le temps actuel
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
					// Prevent de le score plusieurs fois
					if (!keysScored.find((x) => x.key == touche.key && x.time == touche.time)) {
						score++;
						keysScored.push({
							time: touche.time,
							key: touche.key
						});
					}
				} else {
					// Regarde si elle est toujours appuyée après le temps de maintien
					setTimeout(() => {
						if (touchesAppuyees.includes(event.key)) {
							// Prevent de le score plusieurs fois
							if (!keysScored.find((x) => x.key == touche.key && x.time == touche.time)) {
								score++;
								keysScored.push({
									time: touche.time,
									key: touche.key
								});
							}
						}
					}, touche.hold_time * 0.5 * 1000 - (audioPosition - touche.time) * 1000); // Au moins la moiitié du temps de maintien
				}
			} else {
				// Touche appuyée au mauvais moment
				//PlayAudio('/audio/pop_sound.mp3');
			}
		}
	}

	/**
	 * Démarre l'exercice
	 * Récupère le niveau sélectionné et démarre l'audio
	 */
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

		<Exercice image="/keyboard/rythme.jpg" nom="Rythme" handleClick={startExercice} />

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">Règles de l'exercice :</p>
			<p class="text-lg">
				Des cercles tomberons du haut de l'écran. Appuyer sur la touche correspondante lorsque le cercle est entre les deux barres. <br />Si le cercle se prolonge, appuyez sur la touche correspondante
				au moment où il commence à toucher la ligne jusqu'à ce qu'il finisse de tomber entièrement.
			</p>
		</div>

		<div class="md:w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl">
			<div class="flex flex-col w-full">
				<p class="pr-2 mb-2">Niveaux :</p>

				<div class="flex gap-x-8">
					{#each niveaux as niveau}
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<!-- svelte-ignore a11y-no-static-element-interactions -->
						<div
							class="w-48 h-20 bg-blue-300 outline outline-2 outline-blue-400 flex items-center flex-col justify-center rounded-xl"
							on:click={() => {
								selectedLevelName = niveau.Nom;
							}}
						>
							<label class="font-bold" for={niveau.Nom}>{niveau.Nom}</label>
							<p>Difficulté : {niveau.Difficulte}/5</p>
							<input type="radio" bind:group={selectedLevelName} id={niveau.Nom} name="niveau" class="mt-2" value={niveau.Nom} />
						</div>
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
									
									top: ${audioPosition >= touche.time - 4 ? `calc(100% + ${touche.hold_time * 120}px)` : `calc(-10% - ${touche.hold_time * 120}px)`}; 
									transition: top ${touche.time - audioPosition + 1 + (touche.hold ? touche.hold_time * 1.55 : 0)}s linear, background-color 0.2s ease; ${
										Math.abs(audioPosition - touche.time) < (touche.hold ? touche.hold_time * 0.7 : 0.1) && touchesAppuyees.includes(key) ? 'background-color: red;' : 'background-color: #4d4bd4;'
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

	{#if hasExerciceEnded}
		<div transition:fade class="absolute inset-0 backdrop-blur-sm flex items-center justify-center bg-black bg-opacity-20">
			<div class="flex flex-col gap-y-4 w-3/5 py-12 px-12 bg-[#abc8d6] border-4 border-[#859aa5] text-black shadow-xl rounded-xl">
				<div class="text-2xl text-justify">
					<h2 class="text-4xl font-bold text-center mb-8">Vos résultats :</h2>
					<p>Vous avez un score de {score}. <br />Votre précision est de {Math.round((score / scoreMax) * 100)}%</p>
				</div>
				<div class="flex justify-center gap-x-8 mt-4 h-14">
					<button
						class="bg-yellow-400 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-yellow-500 transition-all w-2/5"
						on:click={() => {
							window.location.reload();
						}}
					>
						Recommencer
					</button>

					<a on:click={quit} class="bg-red-400 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-red-500 transition-all w-2/5 flex items-center justify-center" href="/keyboard">Retour</a>
				</div>
			</div>
		</div>
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>

<style>
	.key {
		transition: top 1s linear, background-color 0.1s linear;
	}
</style>
