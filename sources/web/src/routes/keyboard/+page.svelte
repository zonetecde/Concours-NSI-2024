<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-4xl -mt-12">Entrainement au clavier</h1>

	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[90%]">
		<Exercice image="/keyboard/typescript.jpg" link="/keyboard/type-script" nom="Type Script" />
		<Exercice image="" nom="Falling words" />
		<Exercice image="/keyboard/reaction.jpg" nom="Reaction" link="/keyboard/reaction" />
		<Exercice image="/keyboard/bac.jpg" nom="Jeu du Bac" link="/keyboard/bac" />
		<Exercice image="" nom="Sténographie" link="/keyboard/stenographie" />
	</div>

	<Retour urlToGo="/" />
</div>
