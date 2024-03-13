<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import Api from '../../api/Api';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-3xl -mt-12">Exercice d'aide à la souris</h1>

	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[90%]">
		<Exercice image="/mouse/sm.png" nom="Scary Maze" link="/mouse/sm" />
		<Exercice image="" nom="Dodge The Cube" />
		<Exercice image="/mouse/rosu.png" nom="Rosu!" imgStyle=" object-contain " link="/mouse/rosu" />
		<Exercice image="" nom="Nom de l'exercice" />
		<Exercice image="" nom="Nom de l'exercice" />
	</div>

	<Retour urlToGo="/" />
</div>
