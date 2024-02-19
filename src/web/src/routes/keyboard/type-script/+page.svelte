<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import { blur, fade } from 'svelte/transition';
	import Api from '../../../api/Api';
	import { PlayAudio } from '$lib/GlobalFunc';
	import toast from 'svelte-french-toast';

	/** @type {string} */
	const ESPACE = ' ⸱ '; // Caractère de remplacement pour les espaces

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {boolean} */
	let hasExerciceEnded = false; // L'exercice est terminé ?

	/** @type {string}*/
	let sentences = ''; // La phrase à taper

	/** @type {string} */
	let source = ''; // La source de la phrase

	/** @type {Date} */
	let tempsDebut = new Date(); // Date de début de l'exercice

	/** @type {string} */
	let chronometreStr = '0:00'; // Temps écoulé depuis le début de l'exercice (format MM:ss)

	/** @type {boolean} */
	let isFetching = false; // Est-ce qu'on est en train de récupérer une phrase depuis l'API python ?

	/** @type {string} */
	let langue = 'fr'; // Langue de la phrase à récupérer

	/** @type {boolean} */
	let caseSensitive = true; // Majuscules sensibles ?

	/** @type {boolean} */
	let accentSensitive = true; // Accents sensibles ?

	/** @type {number} */
	let nbreMotsTapes = 0; // Nombre de mots tapés

	/** @type {number} */
	let nbreMotsTotal = 0; // Nombre de mots total

	/** @type {Array<string>} */
	$: letters = sentences.split(''); // La phrase à taper, séparée en lettres

	// Status de chaque lettre (tapée, fausse, etc.)
	/** @type {Array<{letter: string, typed: boolean, mistake: boolean}>} */
	$: lettersStatus = letters.map((_letter) => {
		return {
			letter: _letter.trim() || ESPACE, // La lettre à tapper. Si c'est un espace, on affiche le caractère de remplacement
			typed: false, // La lettre a été tapée par l'utilisateur ?
			mistake: false // L'utilisateur a fait une erreur en tappant cette lettre ?
		};
	});

	// Résultats de l'exercice
	/** @type {{
	 * tempsMisString: string,
	 * nbErreurs: number,
	 * nbCaracteres: number,
	 * vitesse: number,
	 * precision: number,
	 * score: number}} */
	let resultats = {
		tempsMisString: '0:00',
		nbErreurs: 0,
		nbCaracteres: 0,
		vitesse: 0,
		precision: 0,
		score: 0
	};

	onMount(() => {
		window.addEventListener('keyup', keyUp);

		window.addEventListener('keydown', keyDown);
	});

	/**
	 * Appelé lorsqu'une touche est relâchée
	 * @param {KeyboardEvent} event
	 */
	function keyUp(event) {
		if (event.key.length === 1 && event.key !== ' ') PlayAudio('../audio/key1_release.mp3');
		else if (event.key === 'Enter') PlayAudio('../audio/key1_enter_release.mp3');
		else if (event.key === 'Backspace') PlayAudio('../audio/key1_return_release.mp3');
		else if (event.key === ' ') PlayAudio('../audio/key1_space_release.mp3');
	}

	/**
	 * Appelé lorsqu'une touche est appuyée
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		if (event.key.length === 1 && event.key !== ' ') PlayAudio('../audio/key1_press.mp3');
		else if (event.key === 'Enter') PlayAudio('../audio/key1_enter_press.mp3');
		else if (event.key === 'Backspace') PlayAudio('../audio/key1_return_press.mp3');
		else if (event.key === ' ') PlayAudio('../audio/key1_space_press.mp3');

		if (hasExerciceStarted) {
			// Une touche a été appuyée,
			// on doit mettre à jour le status de la lettre correspondante

			// Vérifie que c'est une lettre
			if (event.key.length !== 1) return;

			let currentLetter = lettersStatus.find((letter) => !letter.typed);

			if (currentLetter) {
				currentLetter.typed = true;

				let letterToType = currentLetter.letter;

				// Si l'utilisateur a choisi de ne pas tenir compte des majuscules
				if (!caseSensitive) {
					letterToType = letterToType.toLowerCase();
				}

				// Si l'utilisateur a choisi de ne pas tenir compte des accents
				if (!accentSensitive) {
					letterToType = letterToType.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
				}

				// Si la lettre tapée est différente de la lettre attendue
				if ((letterToType === ESPACE ? ' ' : letterToType) !== event.key) {
					currentLetter.mistake = true;
				}

				// Met à jour le nombre de mots tapés
				if (letterToType === ESPACE) {
					nbreMotsTapes++;
				}

				// Si toutes les lettres ont été tapées
				if (lettersStatus.every((letter) => letter.typed)) {
					handleSentencesCompleted();
				}
			}

			lettersStatus = [...lettersStatus]; // Force la mise à jour du tableau
		} else if (event.key === 'Enter') {
			// L'utilisateur a appuyé sur ENTRÉE pour commencer l'exercice

			startExercice();
		}
	}

	/**
	 * Appelé lorsque l'utilisateur a terminé de taper les phrases
	 * @returns {void}
	 */
	function handleSentencesCompleted() {
		hasExerciceEnded = true;

		// Calcul du temps mis pour taper la phrase
		let dateFin = new Date();

		/** @type {number} */
		let tempsMis = Number(dateFin) - Number(tempsDebut);

		// Calcul de stats
		let nbErreurs = lettersStatus.filter((letter) => letter.mistake).length;
		let nbCaracteres = lettersStatus.length;

		// Appel l'API python pour récupérer les scores
		Api.api
			.calculer_score_typescript({
				temps_mis: tempsMis,
				nb_erreurs: nbErreurs,
				nb_caracteres: nbCaracteres
			})
			.then(
				/**
				 * @param response {any}
				 */ (response) => {
					resultats = response;
				}
			);
	}

	async function startExercice() {
		// Récupère une phrase aléatoire depuis l'API python
		hasExerciceStarted = true;

		isFetching = true;

		console.log(langue);
		const response = await Api.api.recuperer_phrase_aleatoire_typescript(langue);
		sentences = response.phrase;
		source = response.titre;

		// Met à jour le nombre de mots total
		nbreMotsTotal = sentences.split(' ').length;
		nbreMotsTapes = 0;

		isFetching = false;

		// Enregistre la date de début (pour calculer le temps mis pour taper la phrase)
		tempsDebut = new Date();

		// Met à jour le chronomètre toutes les secondes
		const chronometre = setInterval(() => {
			let dateFin = new Date();
			let tempsMis = Number(dateFin) - Number(tempsDebut);

			let minutes = Math.floor(tempsMis / 60000);
			let secondes = Math.floor((tempsMis % 60000) / 1000);

			// Met à jour le temps écoulé
			chronometreStr = `${minutes}:${secondes < 10 ? '0' : ''}${secondes}`;

			if (hasExerciceEnded) {
				clearInterval(chronometre);
			}
		}, 1000);
	}

	/**
	 * Appelé lorsque l'utilisateur quitte la page
	 * @returns {void}
	 */
	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keyup', keyUp);
		window.removeEventListener('keydown', keyDown);
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl -mt-12 mb-8">Type Script</h1>

		<Exercice
			image="/keyboard/typescript2.jpg"
			link="/keyboard/type-script"
			nom="Type Script"
			handleClick={startExercice}
		/>

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">Règles de l'exercice :</p>
			<p class="text-lg">
				Vous devrez écrire le texte qui s'affichera le plus rapidement possible, tout en minimisant
				les erreurs de frappe.
			</p>
		</div>

		<div
			class="w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl"
		>
			<div class="flex">
				<p class="pr-2">Langue :</p>
				<select bind:value={langue}>
					<option value="fr">Français</option>
					<option value="en">Anglais</option>
					<option value="de">Allemand</option>
					<option value="ar">Arabe</option>
					<option value="es">Espagnol</option>
					<option value="it">Italien</option>
				</select>
			</div>

			<label for="majuscules" class="text-lg">
				<input
					type="checkbox"
					class="ml-4 mr-1"
					id="majuscules"
					bind:checked={caseSensitive}
				/>Majuscules</label
			>

			<label for="accents" class="text-lg"
				><input
					type="checkbox"
					class="ml-4 mr-0.5"
					id="accents"
					bind:checked={accentSensitive}
				/>Accents</label
			>
		</div>

		<p class="mt-4">Appuyez sur ENTRÉE pour commencer l'exercice</p>
	{:else}
		<div class="flex flex-col w-full">
			{#if !isFetching}
				<p>Nombre de mots tapés : {nbreMotsTapes}/{nbreMotsTotal}</p>
				<p>Temps : {chronometreStr}</p>

				<p class="mt-4 text-2xl text-justify">
					{#each lettersStatus as letter, i}
						<span
							class={'inconsolata ' +
								// Couleur des lettres tapées
								(letter.typed && !letter.mistake ? 'text-gray-700' : '') +
								' ' +
								// Couleur des lettres tapées et fausses
								(letter.mistake ? ' text-red-700' : '') +
								' ' +
								// Taille des espaces
								(letter.letter === ESPACE ? 'text-sm px-1 font-bold' : '') +
								' ' +
								// Couleur des espaces non tapés
								(letter.letter === ESPACE && !letter.typed ? 'text-gray-800' : '') +
								' ' +
								// Souligne la lettre à taper
								((i === 0 && lettersStatus[0].typed === false) ||
								(i > 0 && lettersStatus[i - 1].typed && !lettersStatus[i].typed)
									? ' underline'
									: '')}>{letter.letter}</span
						>
					{/each}
				</p>

				<p class="text-right mt-3">{source}</p>
			{/if}
		</div>

		{#if isFetching}
			<div
				transition:fade
				class="absolute inset-0 backdrop-blur-sm flex items-center justify-center"
			>
				<!-- Roue de chargement -->
				<div class="flex justify-center flex-col gap-y-3 items-center h-full">
					<svg
						class="animate-spin h-10 w-10 text-black"
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
					>
						<circle
							class="opacity-25"
							cx="12"
							cy="12"
							r="10"
							stroke="currentColor"
							stroke-width="4"
						/>
						<path
							class="opacity-75"
							fill="currentColor"
							d="M4 12a8 8 0 018-8V0c4.418 0 8 3.582 8 8s-3.582 8-8 8-8-3.582-8-8z"
						/>
					</svg>

					<p class="text-black font-bold text-2xl ml-3">
						Récupération d'une phrase aléatoire depuis python...
					</p>

					<p class="text-black text-sm ml-3">
						Si ce processus prend trop de temps, veuillez changer de connexion internet
					</p>
				</div>
			</div>
		{/if}

		{#if hasExerciceEnded}
			<div
				transition:fade
				class="absolute inset-0 backdrop-blur-sm flex items-center justify-center"
			>
				<div
					class="flex flex-col gap-y-4 w-3/5 py-12 px-12 bg-[#be97bb] text-black shadow-xl rounded-xl"
				>
					<div class="text-2xl text-justify">
						<h2 class="text-4xl font-bold text-center mb-8">Vos résultats :</h2>

						<p>Temps mis : {resultats.tempsMisString}</p>
						<p>Nombre de caractères : {resultats.nbCaracteres}</p>

						<p>Nombre d'erreurs : {resultats.nbErreurs}</p>

						<p>Vitesse : {resultats.vitesse} caractères par seconde</p>
						<p>Précision : {resultats.precision}</p>

						<p class=" font-bold text-center mt-8">Score : {resultats.score}</p>
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

						<a
							on:click={quit}
							class="bg-red-400 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-red-500 transition-all w-2/5 flex items-center justify-center"
							href="/keyboard">Retour</a
						>
					</div>
				</div>
			</div>
		{/if}
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>
