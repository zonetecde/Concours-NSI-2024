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
	let sentences =
		'La rose est l’une des plantes les plus cultivées au monde et elle occupe la première place dans le marché des fleurs. Mais les rosiers sont aussi des plantes sauvages.';

	/** @type {Date} */
	let dateDebut = new Date();

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
	 * nbCaracteresCorrects: number,
	 * pourcentageReussite: number,
	 * vitesse: number,
	 * precision: number,
	 * score: number}} */
	let resultats = {
		tempsMisString: '0:00',
		nbErreurs: 0,
		nbCaracteres: 0,
		nbCaracteresCorrects: 0,
		pourcentageReussite: 0,
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
		let tempsMis = Number(dateFin) - Number(dateDebut);

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

	function startExercice() {
		//TODO: Récupère une phrase aléatoire depuis l'API python

		// Remplace les apostrophes par des simples quotes
		sentences = sentences.replaceAll('’', "'");

		hasExerciceStarted = true;

		// Enregistre la date de début (pour calculer le temps mis pour taper la phrase)
		dateDebut = new Date();
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl -mt-12 mb-8">Type Script</h1>

		<Exercice image="" link="/keyboard/type-script" nom="Type Script" handleClick={startExercice} />

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
				{#each lettersStatus as letter}
					<span
						class={'inconsolata ' +
							(letter.typed && !letter.mistake ? 'text-gray-500' : '') +
							' ' +
							(letter.mistake ? ' text-red-400' : '') +
							' ' +
							(letter.letter === ESPACE ? 'text-sm -mx-1 font-bold' : '') +
							' ' +
							(letter.letter === ESPACE && !letter.typed ? 'text-yellow-400' : '')}
						>{letter.letter}</span
					>
				{/each}
			</p>
		</div>

		{#if hasExerciceEnded}
			<div
				transition:fade
				class="absolute inset-0 backdrop-blur-sm flex items-center justify-center"
			>
				<div class="flex flex-col gap-y-4 w-3/5 py-12 px-12 bg-[#625a66] shadow-xl rounded-xl">
					<div class="text-2xl text-justify">
						<h2 class="text-4xl font-bold text-center mb-8">Vos résultats :</h2>

						<p class="text-white">Temps mis : {resultats.tempsMisString}</p>
						<p class="text-white">Nombre de caractères : {resultats.nbCaracteres}</p>
						<p class="text-white">
							Nombre de caractères corrects : {resultats.nbCaracteresCorrects}
						</p>
						<p class="text-white">Nombre d'erreurs : {resultats.nbErreurs}</p>

						<p class="text-white">Pourcentage de réussite : {resultats.pourcentageReussite}%</p>
						<p class="text-white">Vitesse : {resultats.vitesse} caractères par seconde</p>
						<p class="text-white">Précision : {resultats.precision}</p>

						<p class="text-white font-bold text-center mt-8">Score : {resultats.score}</p>
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
