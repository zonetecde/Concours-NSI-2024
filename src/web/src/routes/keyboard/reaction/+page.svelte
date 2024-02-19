<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Api from '../../../api/Api';

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

	onMount(() => {
		window.addEventListener('keydown', keyDown);
	});

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
		hasExerciceStarted = true;

		// Initialisation de l'exercice depuis l'API
		Api.api.init_reaction(allowUppercase, allowAccents, allowSpecialCharacters, nombreDeReactions);

		// Demande à l'utilisateur de se préparer
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
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
	{:else}{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>
