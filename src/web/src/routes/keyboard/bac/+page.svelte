<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import toast from 'svelte-french-toast';

	function startExercice() {}

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

	/**
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
						<div class="flex items-center justify-center bg-[#ffffff25] rounded-xl p-2 m-2 gap-x-2">
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
	{/if}

	<Retour urlToGo="/keyboard" taille="w-10 h-10 bottom-3 left-3" />
</div>
