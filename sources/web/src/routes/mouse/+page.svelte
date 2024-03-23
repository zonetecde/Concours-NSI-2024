<script>
	import Exercice from '$lib/Exercice.svelte';
	import LanguagePicker from '$lib/LanguagePicker.svelte';
	import Retour from '$lib/Retour.svelte';
	import { langue } from '$lib/Store';
	import Api from '../../api/Api';

	let phraseExplicatique = '';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-3xl -mt-12">{$langue === 'fr' ? "Exercice d'aide à la souris" : 'Mouse training'}</h1>

	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[90%]">
		<Exercice
			image="/mouse/sm.png"
			nom={$langue === 'fr' ? 'Aide contre Parkinson' : 'Parkinson Eradicator'}
			link="/mouse/sm"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = $langue === 'fr' ? 'Améliorer votre précision et votre vitesse de déplacement de la souris' : 'Improve your mouse accuracy and speed')}
		/>
		<Exercice
			image="/mouse/rosu.png"
			nom="Rosu!"
			imgStyle=" object-contain "
			link="/mouse/rosu"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = $langue === 'fr' ? 'Améliorer votre précision et votre rythme à la souris' : 'Improve your mouse accuracy and rhythm')}
		/>
	</div>

	<p class="text-center text-base lg:bottom-10 bottom-5 lg:text-xl absolute left-1/2 -translate-x-1/2">{phraseExplicatique}</p>

	<LanguagePicker />

	<Retour urlToGo="/" />
</div>
