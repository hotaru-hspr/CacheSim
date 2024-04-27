<script lang="ts">
	let l1_anim = false;
	let l2_anim = false;
	let v_anim = false;
	let r_anim = false;

	import { onMount } from 'svelte';

	interface GETResponse {
		L1_cache: string[];
		L1_cache_hit: string;
		Victim_cache: string[];
		Victim_cache_hit: string;
		L2_cache: string[];
		L2_cache_hit: string;
		address: string;
	}

	let resp: GETResponse = {
		L1_cache: [],
		L1_cache_hit: '',
		Victim_cache: [],
		Victim_cache_hit: '',
		L2_cache: [],
		L2_cache_hit: '',
		address: ''
	};

	let animateHit = false;

	onMount(() => {
		fetch('http://localhost:8000/')
			.then((res) => res.json())
			.then((data) => {
				resp = data;
			});
	});

	function handleClick() {
		fetch('http://localhost:8000/', { method: 'POST' })
			.then((res) => res.json())
			.then((data) => {
				console.log(data);
				resp = data;
				document.getElementById('getmem').disabled = true;

				if (resp.L1_cache_hit == 'Miss') {
					l1_anim = true;
					setTimeout(() => {
						if (resp.Victim_cache_hit == 'Miss') {
							v_anim = true;
							setTimeout(() => {
								if (resp.L2_cache_hit == 'Miss') {
									l2_anim = true;
									setTimeout(() => {
										r_anim = true;
										setTimeout(() => {
											animateHit = true;
											setTimeout(() => {
												animateHit = false;
												l2_anim = false;
												r_anim = false;
												l1_anim = false;
												v_anim = false;
												enableButton();
											}, 500);
										}, 1000);
									}, 1000);
								} else {
									l2_anim = true;
									setTimeout(() => {
										animateHit = true;
										setTimeout(() => {
											animateHit = false;
											l2_anim = false;
											l1_anim = false;
											v_anim = false;
											enableButton();
										}, 500);
									}, 1000);
								}
							}, 1000);
						} else {
							v_anim = true;
							setTimeout(() => {
								if (resp.L2_cache_hit == 'Miss') {
									l2_anim = true;
									setTimeout(() => {
										r_anim = true;
										setTimeout(() => {
											animateHit = true;
											setTimeout(() => {
												animateHit = false;
												l2_anim = false;
												r_anim = false;
												l1_anim = false;
												v_anim = false;
												enableButton();
											}, 500);
										}, 1000);
									}, 1000);
								} else {
									l2_anim = true;
									setTimeout(() => {
										animateHit = true;
										setTimeout(() => {
											animateHit = false;
											l2_anim = false;
											l1_anim = false;
											v_anim = false;
											enableButton();
										}, 500);
									}, 1000);
								}
							}, 1000);
						}
					}, 1000);
				} else {
					l1_anim = true;
					setTimeout(() => {
						if (resp.Victim_cache_hit == 'Miss') {
							v_anim = false;
							setTimeout(() => {
								if (resp.L2_cache_hit == 'Miss') {
									l2_anim = false;
									setTimeout(() => {
										r_anim = false;
										setTimeout(() => {
											animateHit = true;
											setTimeout(() => {
												animateHit = false;
												l2_anim = false;
												r_anim = false;
												l1_anim = false;
												v_anim = false;
												enableButton();
											}, 500);
										}, 1000);
									}, 1000);
								} else {
									l2_anim = true;
									setTimeout(() => {
										animateHit = true;
										setTimeout(() => {
											animateHit = false;
											l2_anim = false;
											l1_anim = false;
											v_anim = false;
											enableButton();
										}, 500);
									}, 1000);
								}
							}, 1000);
						} else {
							v_anim = true;
							setTimeout(() => {
								if (resp.L2_cache_hit == 'Miss') {
									l2_anim = false;
									setTimeout(() => {
										r_anim = false;
										setTimeout(() => {
											animateHit = true;
											setTimeout(() => {
												animateHit = false;
												l2_anim = false;
												r_anim = false;
												l1_anim = false;
												v_anim = false;
												enableButton();
											}, 500);
										}, 1000);
									}, 1000);
								} else {
									l2_anim = true;
									setTimeout(() => {
										animateHit = true;
										setTimeout(() => {
											animateHit = false;
											l2_anim = false;
											l1_anim = false;
											v_anim = false;
											enableButton();
										}, 500);
									}, 1000);
								}
							}, 1000);
						}
					}, 1000);
				}
			});
	}

	function enableButton() {
		document.getElementById('getmem').disabled = false;
	}
</script>

<div class="relative bg-img">
	<div class="flex flex-col justify-between items-center h-screen px-10">
		<div>
			<div class="text-center">
				<div class="flex justify-center space-x-4 py-5">
					<div class="mb-4 text-[#ADD8E6] rounded-lg p-4 text-xl square"></div>
					<div
						class="mb-4 text-center justify-center bg-red-500 text-white rounded-lg p-4 text-3xl cpu"
					>
						<p class="py-2">CPU</p>
						<button
							id="getmem"
							on:click={handleClick}
							class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-4 py-1 rounded text-xl"
						>
							Get memory
						</button>
						<div class="ball-l1 {l1_anim ? 'ballanim-l1' : ''}"></div>
						<div class="ball-v {v_anim ? 'ballanim-v' : ''}"></div>
						<div class="ball-l2 {l2_anim ? 'ballanim-l2' : ''}"></div>
						<div class="ball-r {r_anim ? 'ballanim-r' : ''}"></div>
					</div>
					<div
						class="mb-4 text-[#ADD8E6] rounded-lg p-4 text-xl square"
						style="font-size: 10px;"
					></div>
				</div>
				<div class="flex justify-center space-x-4 py-5">
					<div
						id="l1"
						class="flex-none bg-green-500 text-white rounded-lg p-4 text-xl box px-5 {resp.L1_cache_hit ===
							'Hit' && animateHit
							? 'l1-hit'
							: ''}"
					>
						<p class="text-xl mb-2">L1 Cache</p>
						<div class="overflow-y-auto h-80">
							<table class="w-full">
								{#each resp['L1_cache'] as line}
									<div>{line}</div>
								{/each}
							</table>
						</div>
					</div>
					<div
						id="v"
						class="flex-none bg-blue-500 text-white rounded-lg p-4 text-xl box px-5 {resp.Victim_cache_hit ==
							'Hit' && animateHit
							? 'vic-hit'
							: ''}"
					>
						<p class="text-xl mb-2">Victim Cache</p>
						<div class="overflow-y-auto h-32">
							<table class="w-full">
								{#each resp.Victim_cache as line}
									<div>
										{line}
									</div>
								{/each}
							</table>
						</div>
					</div>
					<div
						id="l2"
						class="flex-none bg-yellow-500 text-white rounded-lg p-4 text-xl box px-5 {resp.L2_cache_hit ==
							'Hit' && animateHit
							? 'l2-hit'
							: ''}"
					>
						<p class="text-xl mb-2">L2 Cache</p>
						<div class="overflow-y-auto h-80">
							{#each resp.L2_cache as line}
								<div>
									{line}
								</div>
							{/each}
						</div>
					</div>
				</div>
				<div
					id="ram"
					class="mt-4 bg-purple-500 text-white rounded-lg p-4 text-4xl py-2 {resp.L1_cache_hit ==
						'Miss' &&
					resp.Victim_cache_hit == 'Miss' &&
					resp.L2_cache_hit == 'Miss' &&
					animateHit
						? 'ram-hit'
						: ''}"
				>
					RAM
				</div>
			</div>
		</div>
		<div class="flex justify-center mt-2 items-center py-2">
			<p class="px-5 text-2xl">Address: {resp.address ? resp.address : '-'}</p>
			<p class="px-5 text-2xl">L1 Cache: {resp.L1_cache_hit ? resp.L1_cache_hit : '-'}</p>
			<p class="px-5 text-2xl">
				Victim Cache: {resp.Victim_cache_hit ? resp.Victim_cache_hit : '-'}
			</p>
			<p class="px-5 text-2xl">L2 Cache: {resp.L2_cache_hit ? resp.L2_cache_hit : '-'}</p>
		</div>
	</div>
</div>

<style>
	@keyframes ripple {
		0% {
			transform: scale(0);
			opacity: 0;
		}
		25% {
			transform: scale(0.25);
			opacity: 0.25;
		}
		50% {
			transform: scale(0.5);
			opacity: 0.5;
		}
		75% {
			transform: scale(0.75);
			opacity: 0.75;
		}
		100% {
			transform: scale(1);
			opacity: 1;
		}
	}
	@keyframes l1-1 {
		0%,
		100% {
			transform: translate(0, 0);
		}
		25% {
			transform: translate(-180px, 0);
		}
		50% {
			transform: translate(-180px, 100px);
		}
		75% {
			transform: translate(-180px, 0);
		}
	}
	@keyframes vic-1 {
		0%,
		100% {
			transform: translate(0, 0);
		}
		50% {
			transform: translate(0, 60px);
		}
	}
	@keyframes l2-1 {
		0%,
		100% {
			transform: translate(0, 0);
		}
		25% {
			transform: translate(160px, 0);
		}
		50% {
			transform: translate(160px, 100px);
		}
		75% {
			transform: translate(160px, 0);
		}
	}
	@keyframes ram-1 {
		0%,
		100% {
			transform: translate(0, 0);
		}
		50% {
			transform: translate(0, 500px);
		}
	}
	.l1-hit {
		animation: ripple 0.5s ease;
	}
	.vic-hit {
		animation: ripple 0.5s ease;
	}
	.l2-hit {
		animation: ripple 0.5s ease;
	}
	.ram-hit {
		animation: ripple 0.5s ease;
	}
	.square {
		width: 400px;
		height: 150px;
	}
	.cpu {
		width: 700px;
		height: 150px;
	}
	.box {
		width: 500px;
		height: 400px;
	}
	.bg-img {
		background-image: url('https://raw.githubusercontent.com/hotaru-hspr/CacheSim/main/frontend/static/lines.png');
		background-size: 100% auto;
		background-repeat: no-repeat;
	}
	.ball-l1 {
		width: 10px;
		height: 10px;
		background-color: black;
		border-radius: 50%;
		position: relative;
		top: -8%;
		left: -1.5%;
		transform: translate(-50%, -50%);
	}
	.ball-v {
		width: 10px;
		height: 10px;
		background-color: black;
		border-radius: 50%;
		position: absolute;
		top: 19.7%;
		left: 50.4%;
		transform: translate(-50%, -50%);
	}
	.ball-l2 {
		width: 10px;
		height: 10px;
		background-color: black;
		border-radius: 50%;
		position: absolute;
		top: 14%;
		left: 70.5%;
		transform: translate(-50%, -50%);
	}
	.ball-r {
		width: 10px;
		height: 10px;
		background-color: black;
		border-radius: 50%;
		position: absolute;
		top: 19.6%;
		left: 65.2%;
		transform: translate(-50%, -50%);
	}

	.ballanim-r {
		animation: ram-1 1s linear;
	}

	.ballanim-l2 {
		animation: l2-1 1s linear;
	}

	.ballanim-v {
		animation: vic-1 0.25s linear;
	}

	.ballanim-l1 {
		animation: l1-1 1s linear;
	}
</style>
