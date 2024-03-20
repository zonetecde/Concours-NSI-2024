<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { langue } from '$lib/Store';
	import Api from '../../api/Api';

	let phraseExplicatique = '';
</script>

<div class="flex pt-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-3xl -mt-12">{$langue === 'fr' ? "Exercice d'aide à du clavier et de la souris" : 'Keyboard and mouse training'}</h1>
	<div class="flex gap-x-8 gap-y-10 items-center justify-center flex-wrap mt-10 w-[90%]">
		<Exercice
			image="/mouse_keyboard/vw.png"
			imgStyle=" object-contain "
			nom="Verbal Warfare"
			link="/mouse_keyboard/vw"
			on:mouseleave={() => (phraseExplicatique = '')}
			on:mouseenter={() => (phraseExplicatique = $langue === 'fr' ? 'Améliore votre précision de frappe au clavier et votre temps de réaction!' : 'Improve your typing accuracy and reaction time!')}
		/>
	</div>
	<p class="text-center text-base lg:bottom-10 bottom-5 lg:text-xl absolute left-1/2 -translate-x-1/2">{phraseExplicatique}</p>
	<Retour urlToGo="/" />
</div>
