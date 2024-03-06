<script>
	import { fade } from 'svelte/transition';

	/** @type {string} */
	export let Text1;
	/** @type {string} */
	export let Text2 = 'Si ce processus prend trop de temps, veuillez changer de connexion internet';
</script>

<div transition:fade class="absolute inset-0 backdrop-blur-sm flex items-center justify-center">
	<!-- Roue de chargement -->
	<div class="flex justify-center flex-col gap-y-3 items-center h-full">
		<svg
			class="animate-spin h-10 w-10 text-black"
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
			viewBox="0 0 24 24"
		>
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0c4.418 0 8 3.582 8 8s-3.582 8-8 8-8-3.582-8-8z"
			/>
		</svg>

		<p class="text-black font-bold text-2xl ml-3">
			{Text1}
		</p>

		<p class="text-black text-sm ml-3">
			{Text2}
		</p>
	</div>
</div>
