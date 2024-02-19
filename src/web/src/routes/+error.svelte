<script>
	import { onMount } from 'svelte';

	onMount(() => {
		// Simule un clique sur un link <a> pour aller à la racine du site
		document.querySelector('a')?.click();
	});
</script>

<div class="flex items-center justify-center">
	<a href="/" class="text-4xl font-bold">Retour à l'accueil</a>
</div>
