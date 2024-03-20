<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import PythonApi from '../../../api/Api';
	import { fade } from 'svelte/transition';
	import { PlayAudio, StopAudio, keyDownAudio, keyUpAudio } from '$lib/GlobalFunc';
	import Fetching from '$lib/Fetching.svelte';
	import { langue } from '$lib/Store';

	/** @type {boolean} */
	let isFetching = false; // L'API est en train de récupérer les données depuis Python ?

	/** @type {boolean} */
	let hasExerciceStarted = false; // L'exercice a commencé ?

	/** @type {number} */
	let nombreDeReactions = 6; // Le nombre de réactions à afficher

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

	/** @type {Array<Array<any>>} */
	let tempsDeReactions = []; // Les temps de réaction de l'utilisateur en millisecondes

	/** @type {number} */
	let indexReaction = 0; // Index de la réaction actuelle

	/** @type {boolean} */
	let countdown_visible = false; // Le compte à rebours est visible ? (avant le début de l'exercice)

	/** @type {number} */
	let countdown = 3; // Compte à rebours avant le début de l'exercice

	/** @type {number} */
	let score = 0; // Le score du joueur

	/** @type {number} */
	let temps_moyen_difficulte = 0; // Le temps moyen de réaction par rapport à la difficulté

	/** @type {number} */
	let temps_moyen_total = 0; // Le temps moyen de réaction total

	onMount(() => {
		window.addEventListener('keydown', keyDown);
		window.addEventListener('keyup', keyUp);

		//@ts-ignore
		window.afficherReaction = afficherReaction;
	});

	/**
	 * Appelée depuis l'API python lorsqu'une réaction est à afficher
	 * @param {string} reaction_a_afficher
	 */
	function afficherReaction(reaction_a_afficher) {
		// Vérifie si l'exercice a commencé (ou que l'utilisateur n'a pas quitté la page)
		if (hasExerciceStarted) {
			// Arrête le tictac
			StopAudio('/audio/tictac.mp3');

			PlayAudio('/audio/ding.mp3');

			// Affiche la réaction à l'écran
			reaction = reaction_a_afficher;
			tempsDebut = Date.now();

			// Met le focus sur l'input de la réaction
			setTimeout(() => {
				reactionTextInput.focus();
			}, 0);
		}
	}

	/**
	 * Appelée lorsqu'une touche est relâchée
	 * @param {KeyboardEvent} event
	 */
	function keyUp(event) {
		keyUpAudio(event);
	}

	/**
	 * Appelée lorsqu'une touche est appuyée
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		keyDownAudio(event);

		// Si la touche est ENTRÉE et que l'exercice n'a pas encore commencé, démarre l'exercice
		if (event.key === 'Enter' && !hasExerciceStarted) {
			startExercice();
		}
	}

	/**
	 * Démarre l'exercice
	 * Envoie les paramètres choisis à l'API et attend que l'API initialise l'exercice
	 */
	async function startExercice() {
		// Initialisation de l'exercice depuis l'API

		isFetching = true;

		// Envoie les paramètres choisis à l'API
		await PythonApi.api.init_reaction(allowUppercase, allowAccents, allowSpecialCharacters, nombreDeReactions);

		// Attend un petit peu pour montrer que l'API est en train d'intialiser l'exercice
		await new Promise((r) => setTimeout(r, 1200));

		isFetching = false;

		// Demande à l'utilisateur de se préparer
		hasExerciceStarted = true;
		countdown_visible = true;
		countdown = 3;
		indexReaction = 0;

		PlayAudio('/audio/countdown.mp3');

		const countdown_interval = setInterval(() => {
			// Au cas où l'utilisateur quitte l'exercice avant le début
			if (hasExerciceStarted) {
				countdown--;
				if (countdown === 0) {
					countdown_visible = false;
					PythonApi.api.lancer_reaction(indexReaction); // Lance la première réaction
					// Lance le tictac
					PlayAudio('/audio/tictac.mp3');
					clearInterval(countdown_interval);
				}
			}
		}, 1000);
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
		window.removeEventListener('keyup', keyUp);
		// @ts-ignore
		window.removeEventListener('afficherReaction', afficherReaction);
		// Arrête le tictac
		StopAudio('/audio/tictac.mp3');
		StopAudio('/audio/countdown.mp3');
		hasExerciceStarted = false;
	}

	/**
	 * Appelée lorsque l'utilisateur a tapé une chaine de caractères dans l'input de la réaction
	 * Compare la chaine de caractères tapée par l'utilisateur avec la chaine de caractères attendue
	 */
	$: if (typedReaction) {
		// Compare la chaine de caractères tapée par l'utilisateur avec la chaine de caractères attendue
		if (typedReaction === reaction) {
			// Calcule le temps de réaction de l'utilisateur en millisecondes
			const dateNow = Date.now();
			const tempsDeReaction = dateNow - tempsDebut;

			tempsDeReactions.push([reaction, tempsDeReaction]);

			reaction = ''; // Efface la réaction pour attendre la prochaine
			typedReaction = ''; // Efface la chaine de caractères tapée par l'utilisateur

			indexReaction++;
			if (indexReaction < nombreDeReactions) {
				// Lance la prochaine réaction
				PythonApi.api.lancer_reaction(indexReaction);
				PlayAudio('/audio/tictac.mp3');
			} else {
				// Si c'était la dernière réaction, on termine l'exercice
				exerciceEnded();
			}
		}
	}

	/**
	 * Appelée lorsque l'exercice est terminé
	 * Envoie les temps de réaction à l'API pour récupérer les statistiques
	 */
	async function exerciceEnded() {
		// Envoie les temps de réaction à l'API pour récupérer les statistiques
		const resultats = await PythonApi.api.calculer_score_reaction(tempsDeReactions);
		score = resultats.score;
		temps_moyen_difficulte = resultats.temps_moyen_difficulte;
		temps_moyen_total = resultats.temps_moyen_total;

		hasExerciceEnded = true;
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl mb-6 -mt-3">Réaction!</h1>

		<Exercice image="/keyboard/reaction.jpg" nom="Réaction" handleClick={startExercice} />

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">
				{$langue == 'fr' ? "Règles de l'exercice :" : 'Rules of the exercise :'}
			</p>
			<p class="text-lg">
				{$langue == 'fr'
					? "Des chaines de caractères aléatoire appraîtront à l'écran dans des intervalles de temps aléatoire. Vous devrez écrire la chaine de caractère le plus rapidement possible."
					: 'Random strings will appear on the screen at random intervals. You will have to write the string as quickly as possible.'}
			</p>
		</div>

		<div class="md:w-full max-w-[1000px] mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl">
			<div class="flex flex-col w-full">
				<p class="pr-2">{$langue == 'fr' ? 'Paramètres :' : 'Settings :'}</p>

				<div class="flex gap-x-8">
					<label for="majuscules" class="text-lg">
						<input type="checkbox" class="mr-1 accent-blue-800" id="majuscules" bind:checked={allowUppercase} />
						{$langue == 'fr' ? 'Majuscules' : 'Uppercase'}
					</label>

					<label for="accents" class="text-lg"
						><input type="checkbox" class="mr-0.5 accent-blue-800" id="accents" bind:checked={allowAccents} />
						{$langue == 'fr' ? 'Accents' : 'Accents'}
					</label>

					<label for="specialChars" class="text-lg"
						><input type="checkbox" class=" mr-0.5 accent-blue-800" id="specialChars" bind:checked={allowSpecialCharacters} />
						{$langue == 'fr' ? 'Caractères spéciaux' : 'Special characters'}
					</label>

					<label for="nombreDeReactions" class="text-lg">
						{$langue == 'fr' ? 'Nombre de réactions' : 'Number of reactions'} :
						<input type="number" class="w-12 ml-1 px-2 outline-none" id="nombreDeReactions" bind:value={nombreDeReactions} />
					</label>
				</div>
			</div>
		</div>

		<p class="mt-8 mb-5">{$langue == 'fr' ? "Appuyez sur Entrée pour commencer l'exercice" : 'Press Enter to start the exercise'}</p>
	{:else if countdown_visible}
		<div class="flex flex-col items-center">
			<p class="text-5xl font-bold mb-4">{countdown}</p>
			<p class="text-xl font-bold mb-4">{$langue == 'fr' ? 'Préparez-vous...' : 'Get ready...'}</p>
		</div>
	{:else if reaction}
		<div out:fade class="flex flex-col items-center">
			<p class="text-5xl font-bold mb-4 inconsolata">{reaction}</p>
			<p class="text-sm font-bold mb-4">{$langue == 'fr' ? 'Écrivez la chaine de caractères ci-dessus' : 'Write the string of characters above'}</p>
			<input type="text" bind:value={typedReaction} bind:this={reactionTextInput} class="text-3xl inconsolata outline-none shadow-xl py-3 font-bold text-center" />
		</div>
	{/if}
	{#if hasExerciceEnded}
		<div transition:fade class="absolute inset-0 backdrop-blur-sm flex items-center justify-center bg-black bg-opacity-20">
			<div class="flex flex-col gap-y-4 w-3/5 py-12 px-12 bg-[#abc8d6] text-black shadow-xl rounded-xl border-2">
				<div class="text-2xl text-justify">
					<h2 class="text-4xl font-bold text-center mb-8">{$langue == 'fr' ? 'Vos résultats' : 'Your results'} :</h2>
					<p>
						{$langue == 'fr' ? 'Votre score est de' : 'Your score is'} <span class="font-bold">{score}</span> points.<br /><br />

						{$langue == 'fr' ? "Temps moyen d'écriture par rapport à la difficulté" : 'Average writing time according to the difficulty'}:{' '}
						<span class="font-bold">{temps_moyen_difficulte}ms</span><br /><br />
						{$langue == 'fr' ? "Temps moyen d'écriture" : 'Average writing time'}{' :'}
						<span class="font-bold">{temps_moyen_total}ms</span>
					</p>
				</div>
				<div class="flex justify-center gap-x-8 mt-4 h-14">
					<button
						class="bg-yellow-400 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-yellow-500 transition-all w-2/5"
						on:click={() => {
							window.location.reload();
						}}
					>
						{$langue == 'fr' ? 'Recommencer' : 'Restart'}
					</button>

					<a on:click={quit} class="bg-red-400 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-red-500 transition-all w-2/5 flex items-center justify-center" href="/keyboard">
						{$langue == 'fr' ? 'Quitter' : 'Quit'}
					</a>
				</div>
			</div>
		</div>
	{/if}

	{#if isFetching}
		<Fetching Text1={$langue === 'fr' ? 'Envois des paramètres choisi à Python...' : 'Sending the chosen parameters to Python...'} Text2="" />
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>
