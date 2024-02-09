<script>
	/** @type {string} */
	export let nom;
	/** @type {string} */
	export let image;
	/** @type {string} */
	export let link = '';
	/** @type {(() => void) | null} */
	export let handleClick = null;

	/**
	 * Appelé lorsque l'utilisateur clique sur l'exercice
	 * Navigue vers la page de l'exercice
	 * @returns {void}
	 */
	function handleExerciceClicked() {
		if (handleClick) {
			handleClick();
			return;
		}
	}
</script>

<a
	href={link || ''}
	class="flex flex-col text-center gap-y-3 hover:scale-110 duration-150 xl:h-56 xl:w-80 md:w-52 md:h-40 h-28 w-40 items-center justify-center bg-gray-800 shadow-md rounded-md p-2 cursor-pointer hover:shadow-lg transition-all"
	on:click={handleExerciceClicked}
>
	<img src={image} alt="img du jeu" class="bg-yellow-400 w-full h-full" />

	<p class="text-lg">{nom}</p>
</a>
