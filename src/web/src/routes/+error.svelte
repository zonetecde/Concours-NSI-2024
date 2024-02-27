<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Api from '../api/Api';

	onMount(() => {
		// Simule un clique sur un link <a> pour aller à la racine du site
		//document.querySelector('a')?.click();

		Api.api.restart();
	});
</script>

<div class="flex flex-col items-center justify-center h-screen w-screen">
	<h1>{$page.status}: {$page.error?.message}</h1>

	<a href="/" class="text-4xl font-bold">Retour à l'accueil</a>
</div>
