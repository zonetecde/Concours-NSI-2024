<script>
	import Exercice from '$lib/Exercice.svelte';
	import { PlayAudio, keyDownAudio, keyUpAudio } from '$lib/GlobalFunc';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Fetching from '$lib/Fetching.svelte';
	import Api from '../../../api/Api';
	import { langue as lang } from '$lib/Store';

	/** @type {boolean} */
	let isFetching = false;

	/** @type {string} */
	let langue = $lang; // La langue de l'audio

	/**
	 * Les audios des phrases ainsi que les phrases au format [(texte, audio file path), ...]
	 * @type {Array<[string, string]>}
	 */
	let audios = [];

	/** @type {HTMLAudioElement} */
	let audioPlayer;

	/** @type {[string, string] | undefined} */
	let currentAudio = undefined; // L'audio actuellement joué avec sa retranscription
	//let currentAudio = ['test', '/audio/stenographie/fr-sb-74.wav']; // debug

	/** @type {string} */
	let tapedSentence = ''; // La phrase tapée par l'utilisateur

	/** @type {number | null} */
	let similitude = null; // Le pourcentage de similitude entre la phrase tapée et la phrase de l'audio

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {boolean} */
	let hasExerciceEnded = false; // L'exercice est terminé ?

	/** @type {boolean} */
	let checkMaj = false; // Autoriser les majuscules dans les chaines de caractères ?

	/** @type {boolean} */
	let checkOrthographe = true; // Autoriser les accents dans les chaines de caractères ?

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

		if (event.key === 'Enter') {
			if (!hasExerciceStarted) {
				startExercice();
			} else if (!isFetching) {
				handleSubmissionButtonClicked();
			}
		}
	}

	/**
	 * Démarre l'exercice
	 * Récupère depuis l'API python les phrases et leurs audios
	 */
	async function startExercice() {
		// Récupère depuis l'API python les phrases et leurs audios
		hasExerciceStarted = true;

		isFetching = true;
		audios = await Api.api.recuperer_phrase_aleatoire_voxforge(langue);
		isFetching = false;

		playNextAudio();
	}

	/**
	 * Joue l'audio suivant à retrancrire
	 * Si il n'y a plus d'audios, récupère de nouvelles phrases depuis l'API python
	 */
	function playNextAudio() {
		if (audios.length === 0) {
			// Récupère de nouvelles phrases
			startExercice();
			return;
		}

		similitude = null; // Cache la réponse précédente
		tapedSentence = ''; // Réinitialise la phrase tapée

		currentAudio = audios.pop();

		console.log('Playing audio:', currentAudio);

		setTimeout(() => {
			if (audioPlayer && currentAudio) {
				audioPlayer.src = currentAudio[1];
				audioPlayer.play();
			}
		}, 100);
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
		window.removeEventListener('keyup', keyUp);
	}

	/**
	 * Appelée lorsqu'on clique sur le bouton de soumission
	 * Envoye la phrase tapée par l'utilisateur à l'API python pour vérifier si elle est correcte en fonction des options choisies
	 */
	async function handleSubmissionButtonClicked() {
		if (currentAudio && hasExerciceStarted && !isFetching) {
			const phrase = tapedSentence;

			// Vérifie si la phrase est correcte
			// Le résultat est sous la forme [Vrai/Faux, pourcentage de ressemblance]
			const data = await Api.api.verifier_phrase_stenographie(currentAudio[0], phrase, checkMaj, checkOrthographe, checkPonctuations);

			similitude = data[1];
		}
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl mb-6 -mt-3">
			{$lang === 'fr' ? 'Sténographie' : 'Stenography'}
		</h1>

		<Exercice image="/keyboard/stenographie.jpg" nom="Sténographie" handleClick={startExercice} />

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">{$lang === 'fr' ? "Règles de l'exercice :" : 'Exercise rules :'}</p>
			<p class="text-lg">
				{$lang === 'fr'
					? 'Un audio vous sera joué dans lequel une phrase sera dite. Vous devrez la recopier le plus vite possible sans fautes.'
					: 'An audio will be played in which a sentence will be said to you. You will have to transcribe it as quickly as possible without mistakes.'}
			</p>
		</div>

		<div class="md:w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl">
			<div class="flex flex-col w-full">
				<p class="pr-2">{$lang === 'fr' ? 'Options :' : 'Options :'}</p>

				<div class="flex gap-x-8 items-center">
					<label for="accents" class="text-lg"
						><input type="checkbox" class="mr-0.5 accent-blue-800" id="accents" bind:checked={checkOrthographe} />
						{$lang === 'fr' ? "Vérifier l'orthographe et la conjugaison" : 'Check spelling and conjugation'}</label
					>

					<label class="text-lg"
						>{$lang === 'fr' ? "Langue de l'audio :" : 'Audio language :'}
						<select class="p-2 border-2 outline-none border-[#656c81] rounded-md w-[200px]" bind:value={langue}>
							<option value="fr">Français</option>
							<option value="en">Anglais</option>
							<option value="sq">Albanian</option>
							<option value="nl">Dutch</option>
							<option value="de">Allemand</option>
							<option value="he">Hébreu</option>
							<option value="el">Grec</option>
							<option value="it">Italien</option>
							<option value="pt">Portugais</option>
							<option value="ru">Russe</option>
							<option value="es">Espagnol</option>
							<option value="tr">Turc</option>
						</select>
					</label>
				</div>
			</div>
		</div>

		<p class="mt-8 mb-5">{$lang === 'fr' ? "Appuyez sur ENTRÉE l'exercice pour commencer" : 'Press ENTER to start the exercise'}</p>
	{:else}
		<div class="w-full h-full flex items-center justify-center flex-col">
			<!-- Media player -->
			<audio controls class="w-1/3" bind:this={audioPlayer}>
				<source type="audio/wav" />
			</audio>

			<small class="mt-5"><i>{$lang === 'fr' ? 'Audio provenant de' : 'Audio from'} <a target="_blank" href="https://www.voxforge.org/">VoxForge.org</a></i></small>

			<!-- svelte-ignore a11y-autofocus -->
			<input
				bind:value={tapedSentence}
				type="text"
				class="mt-10 p-2 border-2 outline-none border-[#656c81] rounded-md w-2/3 shadow-xl focus:scale-105 duration-110"
				autofocus
				spellcheck="false"
				on:blur={() => {
					const input = document.querySelector('input');
					if (input) input.focus();
				}}
				disabled={similitude !== null || isFetching}
			/>

			{#if similitude !== null && currentAudio}
				<p class="text-2xl text-green-950 font-bold mt-3 w-2/3 text-center">
					<span class="text-lg underline underline-offset-2">Réponse :</span><br />{currentAudio[0]}
				</p>
				<p class="mt-5 text-lg">
					{$lang === 'fr' ? 'Taux de réussite' : 'Success rate'}
					: <span class="font-bold">{similitude}%</span>
				</p>

				<div class="flex gap-x-4">
					<button class="mt-8 py-3 px-8 bg-[#5679e4] border-2 border-[#3a4181] text-white rounded-md" on:click={playNextAudio}> {$lang === 'fr' ? 'Phrase suivante' : 'Next sentence'} </button>
					<button
						class="mt-8 py-3 px-8 bg-[#e45656] border-2 border-[#813a3a] text-white rounded-md"
						on:click={() => {
							// Simule un clic sur le <a> qui a pour id `retour`
							const a = document.getElementById('retour');
							a?.click();
						}}
					>
						{$lang === 'fr' ? "S'arrêter" : 'Stop'}
					</button>
					<button class="mt-8 py-3 px-8 bg-[#b9e456] border-2 border-[#80813a] rounded-md text-black" on:click={startExercice}>
						{$lang === 'fr' ? "Changer l'orateur/oratrice " : 'Change speaker'}
					</button>
				</div>
			{:else}
				<button class="mt-8 py-3 px-8 bg-[#5679e4] border-2 border-[#3a4181] text-white rounded-md" on:click={handleSubmissionButtonClicked}> {$lang === 'fr' ? 'Valider' : 'Submit'} </button>
			{/if}
		</div>
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3 z-50" toExecuteBefore={quit} />

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
