<script>
	import Api from '../api/Api';
</script>

<div class="flex h-screen items-center justify-center w-full">
	<div class="w-10/12 h-5/6 flex flex-col items-center gap-y-16">
		<h1 class="font-bold text-5xl">Keymaster</h1>

		<div class="flex flex-row w-full h-4/5 text-2xl gap-x-16">
			<a
				href="/keyboard"
				class="w-1/2 flex items-center justify-center flex-col gap-y-12 hover:scale-110 duration-150 cursor-pointer"
			>
				<img src="keyboard.png" alt="Clavier" class="h-40 object-contain" />
				<p>Entrainement au clavier</p>
			</a>
			<a
				href="/mouse"
				class="w-1/2 flex items-center justify-center flex-col gap-y-12 hover:scale-110 duration-150 cursor-pointer"
			>
				<img src="mouse.png" alt="Souris" class="h-40 p-4 object-contain" />

				<p>Entrainement à la souris</p>
			</a>
		</div>
	</div>
</div>
