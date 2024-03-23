<script>
	import Api from '../api/Api';
	import { langue } from './Store';
</script>

<div class="absolute top-3 right-2 flex gap-x-2 bg-blue-400 px-4 py-2 rounded-xl border-2">
	<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
		<path
			stroke-linecap="round"
			stroke-linejoin="round"
			d="m10.5 21 5.25-11.25L21 21m-9-3h7.5M3 5.621a48.474 48.474 0 0 1 6-.371m0 0c1.12 0 2.233.038 3.334.114M9 5.25V3m3.334 2.364C11.176 10.658 7.69 15.08 3 17.502m9.334-12.138c.896.061 1.785.147 2.666.257m-4.589 8.495a18.023 18.023 0 0 1-3.827-5.802"
		/>
	</svg>
	<select
		class="w-32 text-center bg-transparent outline-none"
		on:change={(e) => {
			// @ts-ignore
			langue.set(e.target.value);
			// @ts-ignore
			Api.api.definir_langue(e.target.value);
		}}
		bind:value={$langue}
	>
		<option selected value="fr">Français</option>
		<option value="en">Anglais</option>
	</select>
</div>
