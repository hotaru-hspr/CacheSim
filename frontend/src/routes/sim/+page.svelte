<script lang="ts">
  import { onMount } from "svelte";

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
    L1_cache_hit: "",
    Victim_cache: [],
    Victim_cache_hit: "",
    L2_cache: [],
    L2_cache_hit: "",
    address: "",
  };

  let animateHit = true;
  let animateBall = true;

  onMount(() => {
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => {
        resp = data;
      });
  });

  function handleClick() {
    fetch("http://localhost:8000/", { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        resp = data;
        animateHit = true;
        animateBall = true;

        setTimeout(() => {
          animateHit = false;
          animateBall = false;
        }, 1000);
      });
  }
</script>
<div class="relative bg-svg">
  <div class="flex flex-col justify-between items-center h-screen px-10">
    <div>
      <div class="text-center">
        <div class="flex justify-center space-x-4 py-5">
          <div class="mb-4 text-[#ADD8E6] rounded-lg p-4 text-xl square"></div>
          <div class="mb-4 text-center justify-center bg-red-500 text-white rounded-lg p-4 text-3xl cpu relative">
            <p class="py-2">CPU</p>
            <button on:click={handleClick} class="bg-blue-500 hover:bg-blue-700 text-white font-bold px-4 py-1 rounded text-xl">
              Get memory
            </button>
            <div class="ball-l1 {resp.L1_cache_hit === 'Hit' && animateBall ? 'l1-1' : ''}"></div>
            <div class="ball-v {resp.Victim_cache_hit === 'Hit' && animateBall ? 'v-1' : ''}"></div>
            <div class="ball-l2 {resp.L2_cache_hit === 'Hit' && animateBall ? 'l2-1' : ''}"></div>
            <div class="ball-r {resp.L1_cache_hit === 'Miss' && resp.Victim_cache_hit === 'Miss' && resp.L2_cache_hit === 'Miss' && animateBall ? 'ram-1' : ''}"></div>
          </div>
          <div class="mb-4 text-[#ADD8E6] rounded-lg p-4 text-xl square"></div>
        </div>
        <div class="flex justify-center space-x-4 py-5">
          <div id='l1' class="flex-none bg-green-500 text-white rounded-lg p-4 text-xl box px-5 {resp.L1_cache_hit === 'Hit' && animateHit ? 'l1-hit' : ''}">
            <p class="text-xl mb-2">L1 Cache</p>
            <div class="overflow-y-auto h-80">
              <table class="w-full">
                {#each resp["L1_cache"] as line}
                  <tr><td style="font-size: 24px;">{line}</td></tr>
                {/each}
              </table>
            </div>
          </div>
          <div id='v' class="flex-none bg-blue-500 text-white rounded-lg p-4 text-xl box px-5 {resp.Victim_cache_hit === 'Hit' && animateHit ? 'v-hit' : ''}">
            <p class="text-xl mb-2">Victim Cache</p>
            <div class="overflow-y-auto h-80">
              <table class="w-full">
                {#each resp.Victim_cache as line}
                  <tr><td style="font-size: 24px;">{line}</td></tr>
                {/each}
              </table>
            </div>
          </div>
          <div id='l2' class="flex-none bg-yellow-500 text-white rounded-lg p-4 text-xl box px-5 {resp.L2_cache_hit === 'Hit' && animateHit ? 'l2-hit' : ''}">
            <p class="text-xl mb-2">L2 Cache</p>
            <div class="overflow-y-auto h-80">
              <table class="w-full">
                {#each resp.L2_cache as line}
                  <tr><td style="font-size: 24px;">{line}</td></tr>
                {/each}
              </table>
            </div>
          </div>
        </div>
        <div id='ram' class="mt-4 bg-purple-500 text-white rounded-lg p-4 text-4xl py-2 {resp.L1_cache_hit === 'Miss' && resp.Victim_cache_hit === 'Miss' && resp.L2_cache_hit === 'Miss' && animateHit ? 'ram-hit'  : ''}">
          RAM
        </div>
      </div>
    </div>
    <div class="flex justify-center mt-2 items-center py-2">
      <p class="px-5 text-2xl">Address: {resp.address?resp.address:"-"}</p>
      <p class="px-5 text-2xl">L1 Cache: {resp.L1_cache_hit?resp.L1_cache_hit:"-"}</p>
      <p class="px-5 text-2xl">Victim Cache: {resp.Victim_cache_hit?resp.Victim_cache_hit:"-"}</p>
      <p class="px-5 text-2xl">L2 Cache: {resp.L2_cache_hit?resp.L2_cache_hit:"-"}</p>
    </div>
  </div>
</div>

<style>
  @keyframes ripple {
    0% {
      transform: scale(0);
      opacity: 1;
    }
    100% {
      transform: scale(1);
      opacity: 0;
    }
  }
  @keyframes l1-1 {
		0% {
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
    100% {
      transform: translate(0, 0);
    }
	}
	@keyframes v-1 {
    0% {
      transform: translate(0, 0);
    }
		50% {
      transform: translate(0, 60px);
    }
    100% {
      transform: translate(0, 0);
    }
  }
	@keyframes l2-1 {
    0% {
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
    100% {
      transform: translate(0, 0);
    }
  }
	@keyframes ram-1 {
    0% {
      transform: translate(0, 0);
    }
    50% {
      transform: translate(0, 500px);
    }
		100% {
      transform: translate(0, 0);
    }
  }
  .l1-hit {
    animation: ripple 0.25s linear;
  }
  .v-hit {
    animation: ripple 0.25s linear;
  }
  .l2-hit {
    animation: ripple 0.25s linear;
  }
  .ram-hit {
    animation: ripple 0.25s linear;
  }
  .square {
    width: 400px;
    height: 150px;
  }
  .cpu {
    width: 700px;
    height: 150px;
    position: relative;
  }
  .box {
    width: 500px;
    height: 400px;
  }
  .bg-svg {
  background-image: url('lines.svg');
  background-size: cover;
  background-repeat: no-repeat;
  }
  .ball-l1 {
    width: 10px;
    height: 10px;
    background-color: black;
    border-radius: 50%;
    position: absolute; 
    top: 66%;
    left: 0%; 
    transform: translate(-50%, -50%);
    animation: l1-1 0.25s linear;
  }
  .ball-v {

    width: 10px;
    height: 10px;
    background-color: black;
    border-radius: 50%;
    position: absolute; 
    top: 100%;
    left: 51%; 
    transform: translate(-50%, -50%);
    animation: v-1 0.25s linear;
  }
  .ball-l2 {
    width: 10px;
    height: 10px;
    background-color: black;
    border-radius: 50%;
    position: absolute; 
    top: 66%;
    left: 100%; 
    transform: translate(-50%, -50%);
    animation: l2-1 0.5s linear;
  }
  .ball-r {
    width: 10px;
    height: 10px;
    background-color: black;
    border-radius: 50%;
    position: absolute; 
    top: 100%;
    left: 86.9%; 
    transform: translate(-50%, -50%);
    animation: ram-1 1s linear;
  }
</style>
