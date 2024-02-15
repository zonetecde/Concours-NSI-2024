<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import { blur, fade } from 'svelte/transition';
	import Api from '../../../api/Api';

	/** @type {string} */
	const ESPACE = ' ⸱ ';

	/** @type {boolean} */
	let hasExerciceStarted = false;

	/** @type {boolean} */
	let hasExerciceEnded = false;

	/** @type {string}*/
	let sentences = ''; // La phrase à taper

	/** @type {Date} */
	let tempsDebut = new Date();

	/** @type {boolean} */
	let isFetching = false; // Est-ce qu'on est en train de récupérer une phrase depuis l'API python ?

	/** @type {Array<string>} */
	$: letters = sentences.split('');

	/** @type {Array<{letter: string, typed: boolean, mistake: boolean}>} */
	$: lettersStatus = letters.map((_letter) => {
		return {
			letter: _letter.trim() || ESPACE, // La lettre à tapper. Si c'est un espace, on affiche le caractère de remplacement
			typed: false, // La lettre a été tapée par l'utilisateur ?
			mistake: false // L'utilisateur a fait une erreur en tappant cette lettre ?
		};
	});

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
		window.addEventListener('keydown', (event) => {
			if (hasExerciceStarted) {
				// Une touche a été appuyée,
				// on doit mettre à jour le status de la lettre correspondante

				// Vérifie que c'est une lettre
				if (event.key.length !== 1) return;

				let currentLetter = lettersStatus.find((letter) => !letter.typed);
				if (currentLetter) {
					currentLetter.typed = true;

					// Si la lettre tapée est différente de la lettre attendue
					if ((currentLetter.letter === ESPACE ? ' ' : currentLetter.letter) !== event.key) {
						currentLetter.mistake = true;
					}

					// Si toutes les lettres ont été tapées
					if (lettersStatus.every((letter) => letter.typed)) {
						handleSentencesCompleted();
					}
				}
				lettersStatus = [...lettersStatus]; // Force la mise à jour du tableau
			} else {
				// L'utilisateur a appuyé sur une touche pour commencer l'exercice

				startExercice();
			}
		});
	});

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

		const response = await Api.api.recuperer_phrase_aleatoire_typescript();
		sentences = response.phrase;

		isFetching = false;

		// Enregistre la date de début (pour calculer le temps mis pour taper la phrase)
		tempsDebut = new Date();
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl -mt-12 mb-8">Type Script</h1>

		<Exercice
			image="/keyboard/typescript.png"
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
			<p class="mt-4">Appuyez sur n'importe quelle touche pour commencer l'exercice.</p>
		</div>
	{:else}
		<div class="flex flex-col gap-y-4">
			<p class="text-2xl text-justify">
				{#each lettersStatus as letter, i}
					<span
						class={'inconsolata ' +
							// Couleur des lettres tapées
							(letter.typed && !letter.mistake ? 'text-gray-500' : '') +
							' ' +
							// Couleur des lettres tapées et fausses
							(letter.mistake ? ' text-red-400' : '') +
							' ' +
							// Taille des espaces
							(letter.letter === ESPACE ? 'text-sm -mx-1 font-bold' : '') +
							' ' +
							// Couleur des espaces non tapés
							(letter.letter === ESPACE && !letter.typed ? 'text-gray-800' : '') +
							' ' +
							// Souligne la lettre à taper
							(i === 0 || (i > 0 && lettersStatus[i - 1].typed && !lettersStatus[i].typed)
								? ' underline'
								: '')}>{letter.letter}</span
					>
				{/each}
			</p>
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
				</div>
			</div>
		{/if}

		{#if hasExerciceEnded}
			<div
				transition:fade
				class="absolute inset-0 backdrop-blur-sm flex items-center justify-center"
			>
				<div
					class="flex flex-col gap-y-4 w-3/5 py-12 px-12 bg-[#b9e6ec] text-black shadow-xl rounded-xl"
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

						<button
							class="bg-red-400 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-red-500 transition-all w-2/5"
							on:click={() => {
								window.location.href = '/keyboard';
							}}>Retour</button
						>
					</div>
				</div>
			</div>
		{/if}
	{/if}

	<Retour urlToGo="/keyboard" />
</div>
