<script>
	import Exercice from '$lib/Exercice.svelte';
	import Retour from '$lib/Retour.svelte';
	import { onMount } from 'svelte';
	import Api from '../../../api/Api';
	import { langue } from '$lib/Store';

	onMount(() => {
		window.addEventListener('keydown', keyDown);
	});

	/**
	 * Appelée lorsqu'une touche est appuyée
	 * Si la touche est ENTRÉE et que l'exercice n'a pas encore commencé, démarre l'exercice
	 * @param {KeyboardEvent} event
	 */
	function keyDown(event) {
		if (event.key === 'Enter') {
			startExercice();
		}
	}

	function startExercice() {
		Api.openPythonProject('Rosu!');
	}

	function quit() {
		// Enlève les event listeners
		window.removeEventListener('keydown', keyDown);
	}
</script>

<div class="flex pt-10 px-10 h-screen justify-center flex-col items-center w-screen">
	<h1 class="font-bold text-3xl mb-6 -mt-3">Rosu!</h1>

	<Exercice image="/mouse/rosu.png" nom="Rosu!" handleClick={() => Api.openPythonProject('Rosu!')} imgStyle=" object-contain " />

	<div class="text-center">
		<p class="mt-8 text-xl mb-4">{$langue == 'fr' ? "Règles de l'exercice :" : 'Rules of the exercise :'}</p>
		<p class="text-lg">
			{$langue == 'fr'
				? "Des cercles de couleurs apparaîtront à l'écran. Cliquez dessus lorsqu'ils sont entièrement remplis, en suivant le rythme de la musique."
				: 'Colored circles will appear on the screen. Click on them when they are fully filled, following the rhythm of the music.'}
		</p>
	</div>

	<p class="mt-8 mb-5">{$langue == 'fr' ? "Appuyez sur ENTRÉE pour commencer l'exercice" : 'Press ENTER to start the exercise'}</p>

	<Retour urlToGo="/mouse" taille="w-10 h-10 bottom-3 left-3" toExecuteBefore={quit} />
</div>
