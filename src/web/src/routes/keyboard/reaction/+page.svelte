<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Api from '../../../api/Api';
	import { fade } from 'svelte/transition';

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {number} */
	let nombreDeReactions = 6;

	/** @type {boolean} */
	let hasExerciceEnded = false; // L'exercice est terminé ?

	/** @type {boolean} */
	let allowUppercase = true; // Autoriser les majuscules dans les chaines de caractères ?

	/** @type {boolean} */
	let allowAccents = true; // Autoriser les accents dans les chaines de caractères ?

	/** @type {boolean} */
	let allowSpecialCharacters = false; // Autoriser les caractères spéciaux dans les chaines de caractères ?

	/** @type {string}*/
	let reaction = ''; // La chaine de caractères à écrire

	/** @type {number} */
	let tempsDebut; // Temps auquel la réaction a été affichée (pour calculer le temps de réaction de l'utilisateur)

	/** @type {string} */
	let typedReaction = ''; // La chaine de caractères tapée par l'utilisateur

	/** @type {HTMLInputElement} */
	let reactionTextInput; // La référence à l'input de la réaction (pour le focus)

	/** @type {number[]} */
	let tempsDeReactions = []; // Les temps de réaction de l'utilisateur en millisecondes

	/** @type {number} */
	let indexReaction = 0; // Index de la réaction actuelle

	/** @type {boolean} */
	let countdown_visible = false; // Le compte à rebours est visible ? (avant le début de l'exercice)

	/** @type {number} */
	let countdown = 3; // Compte à rebours avant le début de l'exercice

	onMount(() => {
		window.addEventListener('keydown', keyDown);

		//@ts-ignore
		window.afficherReaction = afficherReaction;
	});

	/**
	 * Appelée depuis l'API python lorsqu'une réaction est à afficher
	 * @param {string} reaction_a_afficher
	 */
	function afficherReaction(reaction_a_afficher) {
		// Affiche la réaction à l'écran
		reaction = reaction_a_afficher;
		tempsDebut = Date.now();

		// Met le focus sur l'input de la réaction
		setTimeout(() => {
			reactionTextInput.focus();
		}, 0);
	}

	/**
	 * Appelée lorsqu'une touche est appuyée
	 * Si la touche est ENTRÉE et que l'exercice n'a pas encore commencé, démarre l'exercice
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		if (event.key === 'Enter' && !hasExerciceStarted) {
			startExercice();
		}
	}

	function startExercice() {
		// Initialisation de l'exercice depuis l'API
		Api.api.init_reaction(allowUppercase, allowAccents, allowSpecialCharacters, nombreDeReactions);

		// Demande à l'utilisateur de se préparer
		hasExerciceStarted = true;
		countdown_visible = true;
		countdown = 3;
		indexReaction = 0;

		const countdown_interval = setInterval(() => {
			countdown--;
			if (countdown === 0) {
				countdown_visible = false;
				Api.api.lancer_reaction(indexReaction); // Lance la première réaction
				clearInterval(countdown_interval);
			}
		}, 1000);
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
	}

	$: if (typedReaction) {
		// Compare la chaine de caractères tapée par l'utilisateur avec la chaine de caractères attendue
		if (typedReaction === reaction) {
			reaction = ''; // Efface la réaction pour attendre la prochaine
			typedReaction = ''; // Efface la chaine de caractères tapée par l'utilisateur

			// Calcule le temps de réaction de l'utilisateur en millisecondes
			const dateNow = Date.now();
			const tempsDeReaction = dateNow - tempsDebut;

			tempsDeReactions.push(tempsDeReaction);

			indexReaction++;
			if (indexReaction < nombreDeReactions) {
				// Lance la prochaine réaction
				Api.api.lancer_reaction(indexReaction);
			} else {
				// Si c'était la dernière réaction, on termine l'exercice
				hasExerciceEnded = true;
				Api.api.terminer_exercice_reaction();
			}
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
				Des chaines de caractères aléatoire appraîtront à l'écran dans des intervalles de temps
				aléatoire. Vous devrez écrire la chaine de caractère le plus rapidement possible.
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
							class="mr-1"
							id="majuscules"
							bind:checked={allowUppercase}
						/>Majuscules</label
					>

					<label for="accents" class="text-lg"
						><input
							type="checkbox"
							class="mr-0.5"
							id="accents"
							bind:checked={allowAccents}
						/>Accents</label
					>

					<label for="specialChars" class="text-lg"
						><input
							type="checkbox"
							class=" mr-0.5"
							id="specialChars"
							bind:checked={allowSpecialCharacters}
						/>Caractères spéciaux
					</label>
				</div>
			</div>
		</div>

		<p class="mt-8 mb-5">Appuyez sur ENTRÉE pour commencer l'exercice</p>
	{:else if countdown_visible}
		<div class="flex flex-col items-center">
			<p class="text-5xl font-bold mb-4">{countdown}</p>
			<p class="text-xl font-bold mb-4">Préparez-vous...</p>
		</div>
	{:else if reaction}
		<div out:fade class="flex flex-col items-center">
			<p class="text-5xl font-bold mb-4 inconsolata">{reaction || 'ABC'}</p>
			<p class="text-sm font-bold mb-4">Écrivez la chaine de caractères ci-dessus</p>
			<input
				type="text"
				bind:value={typedReaction}
				bind:this={reactionTextInput}
				class="text-3xl inconsolata outline-none shadow-xl py-3 font-bold text-center"
			/>
		</div>
	{:else if hasExerciceEnded}
		<div class="flex flex-col items-center">
			<p class="text-5xl font-bold mb-4">Exercice terminé !</p>
			<p class="text-xl font-bold mb-4">Bravo !</p>
		</div>
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>
