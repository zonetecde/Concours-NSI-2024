<script>
	import Exercice from '$lib/Exercice.svelte';
	import LanguagePicker from '$lib/LanguagePicker.svelte';
	import Retour from '$lib/Retour.svelte';
	import { langue } from '$lib/Store';

	let phraseExplicatique = '';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-4xl -mt-12">
		{$langue === 'fr' ? "Exercice d'aide au clavier" : 'Keyboard training'}
	</h1>

	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[90%]">
		<Exercice
			image="/keyboard/typescript.jpg"
			link="/keyboard/type-script"
			nom="Type Script"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = $langue === 'fr' ? 'Apprenez à taper plus vite et à mieux connaitre votre clavier' : 'Learn to type faster and better know your keyboard')}
		/>
		<Exercice
			image="/keyboard/rythme.jpg"
			nom="Rythme"
			link="/keyboard/rythme"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() =>
				(phraseExplicatique =
					$langue === 'fr'
						? 'Dans le style de Guitar Hero, améliorer votre coordination en tapant au rythme de la musique'
						: 'In the style of Guitar Hero, improve your coordination by typing to the beat of the music')}
		/>
		<Exercice
			image="/keyboard/reaction.jpg"
			nom="Reaction"
			link="/keyboard/reaction"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() =>
				(phraseExplicatique =
					$langue === 'fr' ? 'Améliorer votre temps de réaction en écrivant des caractères le plus vite possible' : 'Improve your reaction time by typing characters as fast as possible')}
		/>
		<Exercice
			image="/keyboard/bac.jpg"
			nom="Jeu du Bac"
			link="/keyboard/bac"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() =>
				(phraseExplicatique =
					$langue === 'fr' ? 'Jeu de culture générale, taper de vous-même vos réponses aux thèmes sélectionnés' : 'General knowledge game, type your own answers to the selected themes')}
		/>
		<Exercice
			image="/keyboard/stenographie.jpg"
			nom={$langue === 'fr' ? 'Sténographie' : 'Stenography'}
			link="/keyboard/stenographie"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() =>
				(phraseExplicatique = $langue === 'fr' ? 'Ecrivez le script entendu le plus vite possible et le plus précisément possible' : 'Write the script heard as quickly and accurately as possible')}
		/>
	</div>

	<p class="text-center text-base lg:bottom-10 bottom-5 lg:text-xl absolute left-1/2 -translate-x-1/2">{phraseExplicatique}</p>

	<LanguagePicker />

	<Retour urlToGo="/" />
</div>
