<script>
	/** @type {string} */
	export let urlToGo;

	/** @type {string} */
	export let taille = 'w-16 h-16 bottom-6 left-4';
</script>

<a class={'absolute ' + taille} href={urlToGo}>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		fill="none"
		viewBox="0 0 24 24"
		stroke-width="1.5"
		stroke="black"
	>
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			d="m11.25 9-3 3m0 0 3 3m-3-3h7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
		/>
	</svg>
</a>
