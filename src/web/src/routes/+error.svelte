<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	onMount(() => {
		// Simule un clique sur un link <a> pour aller à la racine du site
		//document.querySelector('a')?.click();
	});
</script>

<div class="flex flex-col items-center justify-center">
	<h1>{$page.status}: {$page.error?.message}</h1>

	<a href="/" class="text-4xl font-bold">Retour à l'accueil</a>
</div>
