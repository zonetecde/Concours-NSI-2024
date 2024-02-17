<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import toast from 'svelte-french-toast';
	import { fade } from 'svelte/transition';
	import { PlayAudio } from '$lib/GlobalFunc';
	import JeuBacRow, { Mot } from './JeuBacRow';

	/** @type {Array<string>} */
	let themes = [
		'Animaux',
		'Pays',
		'Fruits',
		'Légumes',
		'Métiers',
		'Sport',
		'...',
		'...',
		'...',
		'...',
		'...',
		'...',
		'...',
		'...',
		'...',
		'...'
	]; // Les thèmes disponibles. TODO: Récupérer les thèmes depuis l'API python

	/** @type {Array<string>} */
	let selectedThemes = ['Animaux', 'Pays', 'Fruits', 'Légumes', 'Métiers']; // Les thèmes sélectionnés par l'utilisateur (par défaut les 5 ci-gauche)

	/** @type {boolean} */
	let hasExerciceStarted = false;

	/** @type {number} */
	let nombreDeRound = 3; // Le nombre de ligne de l'exercice

	/** @type {Array<string>} */
	let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

	/** @type {string} */
	let rouletteAlphabet = ''; // La lettre de la roulette actuellement affichée

	/** @type {Array<JeuBacRow>} */
	let rows = [];

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

	/**
	 * Appelée lorsqu'on appuie sur ENTRÉE
	 * Vérifie que l'utilisateur a sélectionné 5 thèmes
	 * Si oui, démarre l'exercice
	 */
	function startExercice() {
		if (selectedThemes.length < 5) {
			toast.error('Veuillez sélectionner 5 thèmes');
			return;
		}

		hasExerciceStarted = true;

		startRound();
	}

	/**
	 * Appelée lorsqu'un thème est sélectionné ou désélectionné
	 * Si le thème est déjà sélectionné, le retire des thèmes sélectionnés
	 * Sinon, l'ajoute aux thèmes sélectionnés
	 * Si l'utilisateur a déjà sélectionné 5 thèmes, l'empêche de sélectionner plus de thèmes
	 * @param {any} e
	 * @param {string} theme
	 */
	function handleThemeSelected(e, theme) {
		if (selectedThemes.includes(theme)) {
			selectedThemes = selectedThemes.filter((t) => t !== theme);
		} else {
			if (selectedThemes.length < 5) {
				selectedThemes = [...selectedThemes, theme];
			} else {
				e.target.checked = false;
				toast.error('Vous ne pouvez pas sélectionner plus de 5 thèmes');
			}
		}
	}

	async function startRound() {
		startRoulette().then((lettre) => {
			// Ajoute la ligne pour cette lettre
			rows = [
				...rows,
				new JeuBacRow(
					lettre,
					selectedThemes.map((theme) => new Mot(theme))
				)
			];
		});
	}

	/**
	 * Démarre la roulette
	 * @returns {Promise<string>}
	 */
	function startRoulette() {
		let counter = 0;

		return new Promise((resolve) => {
			let roulette = function () {
				counter += 1;

				let newLetter = '';

				do {
					newLetter = alphabet[Math.floor(Math.random() * alphabet.length)];
				} while (newLetter === rouletteAlphabet || rows.find((row) => row.lettre === newLetter)); // Tant que la lettre est la même que la précédente ou qu'elle a déjà été utilisée

				rouletteAlphabet = newLetter;

				PlayAudio('../audio/roulette.mp3');

				if (counter < 50) {
					// Vérifie qu'on est toujours sur la page
					if (hasExerciceStarted) setTimeout(roulette, calculateInterval(counter)); // Ralentit la roulette
				} else {
					// Affiche la lettre 3 secondes avant de lancer l'exercice
					setTimeout(() => {
						rouletteAlphabet = '';

						// Retourne la lettre de la roulette
						resolve(newLetter);
					}, 1000);
				}
			};
			setTimeout(roulette, counter);
		});
	}

	/**
	 * Calcule l'intervalle entre chaque changement de lettre de la roulette
	 * Plus le compteur est élevé, plus l'intervalle est grand (pour ralentir la roulette)
	 * @param {number} counter
	 * @returns {number}
	 */
	function calculateInterval(counter) {
		if (counter > 44) {
			return counter * 8;
		} else if (counter < 35) {
			return counter * 3;
		} else {
			return counter * 5.5;
		}
	}

	/**
	 * Appelée lorsqu'on clique sur le bouton de validation
	 */
	function validateRow() {
		// TODO: Vérifier les réponses à l'aide de l'API python

		// Marque la dernière ligne du tableau comme complète
		rows[rows.length - 1].completer = true;

		// Regarde si il y a d'autres rounds à faire
		if (rows.length < nombreDeRound) {
			startRound();
		}
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	{#if !hasExerciceStarted}
		<h1 class="font-bold text-3xl -mt-12 mb-8">Jeu du Bac</h1>

		<Exercice
			image="/keyboard/bac.jpg"
			link="/keyboard/bac"
			nom="Jeu du Bac"
			handleClick={startExercice}
		/>

		<div class="text-center">
			<p class="mt-8 text-xl mb-4">Règles de l'exercice :</p>
			<p class="text-lg">
				Trouvez et écrivez un mot correspondant à chaque thème choisi qui commence par la lettre
				donnée le plus rapidement possible
			</p>
		</div>

		<div
			class="w-full max-w-full mt-4 p-4 justify-center items-center flex flex-row bg-[#ffffff25] rounded-xl"
		>
			<div class="flex flex-col w-full">
				<p class="pr-2">Veuillez sélectionner 5 thèmes :</p>

				<div class="flex overflow-x-scroll py-2">
					{#each themes as theme}
						<div class="flex items-center justify-center bg-[#fcfcfcab] rounded-xl p-2 m-2 gap-x-2">
							<input
								type="checkbox"
								id={theme}
								name={theme}
								value={theme}
								checked={selectedThemes.includes(theme)}
								on:change={(e) => handleThemeSelected(e, theme)}
							/>
							<label for={theme}>{theme}</label>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<p class="mt-8">Appuyez sur ENTRÉE pour commencer l'exercice</p>
	{:else}
		<p class="-mt-10 text-3xl mb-5 font-bold">Jeu du Bac</p>

		<div
			class="bg-[#ffffffea] shadow-xl rounded-lg border-2 border-[#1d1b1bde] h-4/5 w-full text-center relative"
		>
			<!-- Header -->
			<div class="flex">
				<p
					class="border-r-2 w-[8%] h-10 border-[#1d1b1b8c] pt-1 flex items-center justify-center border-b-2"
				>
					Lettre
				</p>

				{#each selectedThemes as theme, i}
					<p
						class="last:border-r-0 w-[18.4%] border-r-2 h-10 border-[#1d1b1b8c] border-b-2 pt-1 flex items-center justify-center"
					>
						{theme}
					</p>
				{/each}
			</div>

			<!-- Rows -->
			{#each rows as row}
				<div class="flex" transition:fade>
					<p
						class="border-r-2 h-10 w-[8%] border-[#1d1b1b8c] pt-1 flex items-center justify-center border-b-2"
					>
						{row.lettre}
					</p>

					{#each selectedThemes as theme, i}
						{#if row.completer}
							<p
								class="last:border-r-0 w-[18.4%] border-r-2 h-10 border-[#1d1b1b8c] bg-[#cce6e9] border-b-2 flex pt-0.5 items-center px-2"
							>
								{row.cols.find((col) => col.theme === theme)?.mot}
							</p>
						{:else}
							<input
								type="text"
								spellcheck="false"
								bind:value={row.cols[i].mot}
								placeholder={row.lettre}
								class="last:border-r-0 w-[18.4%] outline-none px-2 border-r-2 h-10 border-[#1d1b1b8c] border-b-2 flex items-center justify-center"
							/>
						{/if}
					{/each}
				</div>
			{/each}

			<button
				class="w-12 h-12 px-2 rounded-full py-2 absolute bottom-3 hover:scale-110 duration-150 right-3 shadow-xl cursor-pointer bg-green-800"
				on:click={validateRow}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="white"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
				</svg>
			</button>
		</div>

		{#if rouletteAlphabet}
			<div
				transition:fade
				class="absolute inset-0 backdrop-blur-sm flex items-center justify-center"
			>
				<p
					class="inconsolata text-9xl text-black bg-white px-12 py-3 rounded-3xl border-4 border-gray-500 font-bold"
				>
					{rouletteAlphabet}
				</p>
			</div>
		{/if}
	{/if}

	<Retour
		urlToGo="/keyboard"
		taille="w-10 h-10 bottom-3 left-3"
		toExecuteBefore={() => {
			// Enlève les event listeners
			window.removeEventListener('keydown', keyDown);
			// Force l'arrêt de la roulette
			hasExerciceStarted = false;
		}}
	/>
</div>
