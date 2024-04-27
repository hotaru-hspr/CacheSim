<script lang="ts">
</script>

<div class="flex items-center min-h-screen w-full px-10">
	<div class="">
		<h1 class="py-50 text-6xl">Cache Simulator</h1>
		<br />
		<p class="text-xl">Before you continue,</p>
		<p class="text-xl">
			Make sure you have the FastAPI server running in the background (main.py from the repository).
		</p>
		<br />
		<a href="https://www.github.com/hotaru-hspr/CacheSim"
			><p class="text-xl underline hover:text-gray-600">Click here for GitHub Repo</p></a
		><br /><br />
		<div class="bg-[#F4F4F4] shadow-md hover:bg-sky-100 w-fit rounded-2xl px-3 py-3">
			<button
				on:click={() => {
					window.location.href = '/sim';
				}}>Next</button
			>
		</div>
	</div>
</div>
