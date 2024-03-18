<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';

	let phraseExplicatique = '';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-4xl -mt-12">Entrainement au clavier</h1>

	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[90%]">
		<Exercice
			image="/keyboard/typescript.jpg"
			link="/keyboard/type-script"
			nom="Type Script"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = 'Apprenez à taper plus vite et à mieux connaitre votre clavier')}
		/>
		<Exercice
			image="/keyboard/rythme.jpg"
			nom="Rythme"
			link="/keyboard/rythme"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = 'Dans le style de Guitar Hero, améliorer votre coordination en tapant au rythme de la musique')}
		/>
		<Exercice
			image="/keyboard/reaction.jpg"
			nom="Reaction"
			link="/keyboard/reaction"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = 'Améliorer votre temps de réaction en écrivant des caractères le plus vite possible')}
		/>
		<Exercice
			image="/keyboard/bac.jpg"
			nom="Jeu du Bac"
			link="/keyboard/bac"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = 'Jeu de culture générale, taper de vous-même vos réponses aux thèmes sélectionnés')}
		/>
		<Exercice
			image="/keyboard/stenographie.jpg"
			nom="Sténographie"
			link="/keyboard/stenographie"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = 'Ecrivez le script entendu le plus vite possible et le plus précisément possible')}
		/>
	</div>

	<p class="text-center text-base lg:bottom-10 bottom-5 lg:text-xl absolute left-1/2 -translate-x-1/2">{phraseExplicatique}</p>

	<Retour urlToGo="/" />
</div>
