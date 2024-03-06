<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Api from '../api/Api';

	onMount(() => {
		// Simule un clique sur un link <a> pour aller à la racine du site
		//document.querySelector('a')?.click();
		setTimeout(() => {
			Api.api.restart();
		}, 1000);
	});
</script>

<div class="flex flex-col items-center justify-center h-screen w-screen">
	<h1 class="font-bold text-5xl">Oops !</h1>
	<p class="text-2xl mt-5">Une erreur est survenue, relancement du programme...</p>
</div>
