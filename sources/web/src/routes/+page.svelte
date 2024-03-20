<script>
	import Api from '../api/Api';

	function handle() {
		// provoke a svelte internal error
		window.location.href = '/keyboadrd';
	}
</script>

<div class="flex h-screen items-center justify-center w-full" id="main">
	<div class="w-10/12 h-5/6 flex flex-col items-center gap-y-16">
		<h1 class="font-bold text-5xl">Keymaster</h1>

		<div class="flex flex-row w-full h-4/5 text-2xl gap-x-16 text-center">
			<a href="/keyboard" class="w-1/2 flex items-center justify-center flex-col gap-y-12 hover:scale-110 duration-150 cursor-pointer">
				<img src="keyboard.png" alt="Clavier" class="h-40 object-contain" />
				<p>Entrainement au clavier</p>
			</a>
			<a href="/mouse_keyboard" class="w-2/3 flex items-center justify-center flex-col gap-y-12 hover:scale-110 duration-150 cursor-pointer">
				<img src="mouse_keyboard.png" alt="Souris_clavier" class="h-40 p-4 object-contain" />

				<p>Entrainement au clavier et à la souris</p>
			</a>
			<a href="/mouse" class="w-1/2 flex items-center justify-center flex-col gap-y-12 hover:scale-110 duration-150 cursor-pointer">
				<img src="mouse.png" alt="Souris" class="h-40 p-4 object-contain" />

				<p>Entrainement à la souris</p>
			</a>
		</div>
	</div>
</div>

<style>
	/* Style du fond de la fenêtre */
	#main {
		--s: 200px;
		--c: #9cb7dd;

		--_g: #0000 8%, var(--c) 0 17%, #0000 0 58%;
		background: linear-gradient(135deg, #0000 20.5%, var(--c) 0 29.5%, #0000 0) 0 calc(var(--s) / 4), linear-gradient(45deg, var(--_g)) calc(var(--s) / 2) 0,
			linear-gradient(135deg, var(--_g), var(--c) 0 67%, #0000 0), linear-gradient(45deg, var(--_g), var(--c) 0 67%, #0000 0 83%, var(--c) 0 92%, #0000 0), #9dbedd;
		background-size: var(--s) var(--s);
	}
</style>
