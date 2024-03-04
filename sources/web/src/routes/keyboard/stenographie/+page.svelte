<script>
	import Exercice from '$lib/Exercice.svelte';
	import { PlayAudio, keyDownAudio, keyUpAudio } from '$lib/GlobalFunc';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Fetching from '$lib/Fetching.svelte';
	import Api from '../../../api/Api';

	/** @type {boolean} */
	let isFetching = false;

	/**
	 * Les audios des phrases ainsi que les phrases au format [(texte, audio file path), ...]
	 * @type {Array<[string, string]>}
	 */
	let audios = [];

	/** @type {[string, string] | undefined} */
	//let currentAudio = []; // L'audio actuellement joué avec sa retranscription
	let currentAudio = ['test', '/audio/stenographie/fr-sb-74.wav']; // L'audio actuellement joué avec sa retranscription

	/** @type {string} */
	let tapedSentence = ''; // La phrase tapée par l'utilisateur

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {boolean} */
	let hasExerciceEnded = false; // L'exercice est terminé ?

	/** @type {boolean} */
	let checkMaj = true; // Autoriser les majuscules dans les chaines de caractères ?

	/** @type {boolean} */
	let checkAccents = true; // Autoriser les accents dans les chaines de caractères ?

	/** @type {boolean} */
	let checkPonctuations = false; // Autoriser les caractères spéciaux dans les chaines de caractères ?

	onMount(() => {
		window.addEventListener('keydown', keyDown);
		window.addEventListener('keyup', keyUp);
	});

	/**
	 * Appelée lorsqu'une touche est relâchée
	 * @param {KeyboardEvent} event
	 */
	function keyUp(event) {
		keyUpAudio(event);
	}

	/**
	 * Appelée lorsqu'une touche est appuyée
	 * Si la touche est ENTRÉE et que l'exercice n'a pas encore commencé, démarre l'exercice
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		keyDownAudio(event);

		if (event.key === 'Enter' && !hasExerciceStarted) {
			startExercice();
		}
	}

	async function startExercice() {
		// Récupère depuis l'API python les phrases et leurs audios
		hasExerciceStarted = true;

		isFetching = true;
		audios = await Api.api.recuperer_phrase_aleatoire_voxforge();
		isFetching = false;

		playNextAudio();
	}

	/**
	 * Joue l'audio suivant
	 */
	function playNextAudio() {
		if (audios.length === 0) {
			hasExerciceEnded = true;
			return;
		}

		currentAudio = audios.pop();
		// L'audio sera joué dans le render automatiquement (autoplay = true)
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
		window.removeEventListener('keyup', keyUp);
	}

	/**
	 * Appelée lorsqu'on clique sur le bouton de soumission
	 * Vérifie si la phrase est correcte en fonction des options choisies
	 */
	function handleSubmissionButtonClicked() {
		const input = document.querySelector('input');
		const phrase = tapedSentence;

		// Vérifie si la phrase est correcte
		let correct = true;
		if (!checkMaj) {
			correct = correct && !/[A-Z]/.test(phrase);
		}
		if (!checkAccents) {
			correct = correct && !/[À-ÿ]/.test(phrase);
		}
		if (!checkPonctuations) {
			correct = correct && !/[.,\/#!$%\^&\*;:{}=\-_`~()]/.test(phrase);
		}

		if (correct) {
			// Joue l'audio suivant
			playNextAudio();
		} else {
			// Joue un son d'erreur
			const audio = new Audio('/audio/ding.mp3');
			audio.play();
		}
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl mb-6 -mt-3">Réaction!</h1>

		<Exercice image="/keyboard/reaction.jpg" nom="Réaction" handleClick={startExercice} />

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">Règles de l'exercice :</p>
			<p class="text-lg">
				Un audio vous sera joué dans lequel une phrase sera dite. Vous devrez la recopier le plus
				vite possible sans fautes.
			</p>
		</div>

		<div
			class="md:w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl"
		>
			<div class="flex flex-col w-full">
				<p class="pr-2">Options :</p>

				<div class="flex gap-x-8">
					<label for="majuscules" class="text-lg">
						<input
							type="checkbox"
							class="mr-1 accent-blue-800"
							id="majuscules"
							bind:checked={checkMaj}
						/>Majuscules</label
					>

					<label for="accents" class="text-lg"
						><input
							type="checkbox"
							class="mr-0.5 accent-blue-800"
							id="accents"
							bind:checked={checkAccents}
						/>Accents</label
					>

					<label for="specialChars" class="text-lg"
						><input
							type="checkbox"
							class=" mr-0.5 accent-blue-800"
							id="specialChars"
							bind:checked={checkPonctuations}
						/>Ponctuations
					</label>
				</div>
			</div>
		</div>

		<p class="mt-8 mb-5">Appuyez sur ENTRÉE pour commencer l'exercice</p>
	{:else if currentAudio}
		<div class="w-full h-full flex items-center justify-center flex-col">
			<!-- Media player -->
			<audio controls autoplay class="w-1/3">
				<source src={currentAudio[1]} type="audio/wav" />
			</audio>

			<small class="mt-5"
				><i
					>Audio provenant de <a target="_blank" href="https://www.voxforge.org/">VoxForge.org</a
					></i
				></small
			>

			<!-- svelte-ignore a11y-autofocus -->
			<input
				bind:value={tapedSentence}
				type="text"
				class="mt-10 p-2 border-2 outline-none border-[#656c81] rounded-md w-2/3 shadow-xl focus:scale-105 duration-110"
				autofocus
			/>

			<button
				class="mt-8 py-3 px-8 bg-[#5679e4] border-2 border-[#3a4181] text-white rounded-md"
				on:click={handleSubmissionButtonClicked}
			>
				Soumettre
			</button>
		</div>
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />

	{#if isFetching}
		<Fetching Text1="Récupèration d'audios de phrases aléatoires" />
	{/if}
</div>

<style>
	audio::-webkit-media-controls-panel {
		background-color: #6583ad;
	}

	audio::-webkit-media-controls-current-time-display,
	audio::-webkit-media-controls-time-remaining-display {
		text-shadow: none;
	}
</style>
