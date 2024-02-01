<script>
	import Retour from '$lib/Retour.svelte';
	import Exercice from './Exercice.svelte';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-3xl -mt-12">Exercice d'aide à la sourie</h1>

	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[80%]">
		<Exercice image="" nom="Mouse Road" />
		<Exercice image="" nom="Dodge The Cube" />
		<Exercice image="" nom="Nom de l'exercice" />
		<Exercice image="" nom="Nom de l'exercice" />
		<Exercice image="" nom="Nom de l'exercice" />
	</div>

	<Retour />
</div>
