<script>
	/** @type {string} */
	export let nom;
	/** @type {string} */
	export let image;
</script>

<div class="flex flex-col text-center gap-y-3 hover:scale-110 duration-150">
	<img src={image} alt="img du jeu" class="bg-yellow-400 md:h-56 md:w-80 h-28 w-40" />

	<p class="text-lg">{nom}</p>
</div>
