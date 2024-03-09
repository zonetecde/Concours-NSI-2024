<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Api from '../../../api/Api';

	/** @type {Array<import('$lib/classes/Niveau').Niveau>} */
	let niveaux = []; // Niveaux

	/** @type {import('$lib/classes/Niveau').Niveau} */
	let selectedLevelObj;

	/** @type {number} */
	let audioPosition = 0;

	/** @type {Array<any>} */
	let circlesToDraw = [];

	/** @type {Array<string>} */
	let keys = ['f', 'g', 'j', 'k'];

	/** @type {HTMLAudioElement} */
	let audio;

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {string} */
	let selectedLevelName = 'Blue Ocean'; // Niveau sélectionné

	/** @type {boolean} */
	let hasExerciceEnded = false; // L'exercice est terminé ?

	/** @type {boolean} */
	let allowUppercase = true; // Autoriser les majuscules dans les chaines de caractères ?

	/** @type {boolean} */
	let allowAccents = true; // Autoriser les accents dans les chaines de caractères ?

	/** @type {boolean} */
	let allowSpecialCharacters = false; // Autoriser les caractères spéciaux dans les chaines de caractères ?

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
	function keyUp(event) {}

	/**
	 * Appelée lorsqu'une touche est appuyée
	 * Si la touche est ENTRÉE et que l'exercice n'a pas encore commencé, démarre l'exercice
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		if (event.key === 'Enter' && !hasExerciceStarted) {
			startExercice();
		}

		if (event.key === 'Escape') {
			// Arrête tout les audios TODO: delete
			audio.pause();
		}
	}

	function startExercice() {
		hasExerciceStarted = true;

		const niv = niveaux.find((niveau) => niveau.Nom === selectedLevelName);
		if (niv) {
			selectedLevelObj = niv;

			// Joue le son
			audio = new Audio(`/audio/rythme/${selectedLevelObj.Audio}`);
			audio.play();

			const int = setInterval(() => {
				audioPosition = audio.currentTime;
			}, 10);

			// quand l'autio est terminé
			audio.onended = () => {
				clearInterval(int);
			};
		}
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
		window.removeEventListener('keyup', keyUp);
		audio.pause();
	}

	$: if (audioPosition) {
		console.log(audio.currentTime);
	}
</script>

<div class="flex px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl mb-6 mt-7">Rythme</h1>

		<Exercice image="/keyboard/reaction.jpg" nom="Rythme" handleClick={startExercice} />

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">Règles de l'exercice :</p>
			<p class="text-lg">
				Des carrés tomberons du haut de l'écran, appuyez sur la touche correspondante lorsque le
				carré touche la ligne d'arrivée. <br />Si le carré se prolonge, appuyez sur la touche
				correspondante au moment où il commence à toucher la ligne jusqu'à ce qu'il finisse de
				tomber entièrement.
			</p>
		</div>

		<div
			class="md:w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl"
		>
			<div class="flex flex-col w-full">
				<p class="pr-2">Niveaux :</p>

				<div class="flex gap-x-8">
					{#each niveaux as niveau}
						<label for={niveau.Nom}
							><input
								type="radio"
								bind:group={selectedLevelName}
								id={niveau.Nom}
								name="niveau"
								class="mr-2"
								value={niveau.Nom}
							/>{niveau.Nom}</label
						>
					{/each}
				</div>
			</div>
		</div>

		<p class="mt-8 mb-5">Appuyez sur ENTRÉE pour commencer l'exercice</p>
	{:else}
		<div
			class="w-[450px] h-[600px] bg-[#84af80] outline-4 rounded-xl outline-[#206442] outline relative"
		>
			<!---->
			<div class="absolute border-t-2 border-[#206442] bottom-[110px] w-full" />

			<div
				class="w-full h-full grid absolute bottom-0 divide-x-2 divide-[#206442]"
				style={`grid-template-columns: repeat(${keys.length}, minmax(0, 1fr))`}
			>
				{#each keys as key}
					<div class="w-full h-full flex justify-center items-center relative">
						{#each selectedLevelObj.Touches as touche}
							{#if touche.key === key}
								<div
									class="w-10 h-10 bg-[#206442] rounded-full absolute key"
									style={`top: ${
										audioPosition >= touche.time - 4 ? '79%' : '0'
									}; transition-duration: ${touche.time - audioPosition}s`}
								/>
							{/if}
						{/each}

						<p class="text-3xl absolute bottom-9 font-bold">{key.toUpperCase()}</p>
					</div>
				{/each}
			</div>
		</div>
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>

<style>
	.key {
		transition: top 4s linear;
	}
</style>
