<script lang="ts">

    interface Response {
        L1_cache: string[];
        Victim_cache: string[];
        L2_cache: string[];
        address: string;
    }

    let resp: Response = {
        L1_cache: [],
        Victim_cache: [],
        L2_cache: [],
        address: '',
    };

        fetch("http://localhost:8000/")
        .then((res) => res.json())
        .then((data) => {
            resp = data;
        });

    function handleClick() {
        fetch("http://localhost:8000/", { method: "POST" })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                fetch("http://localhost:8000/")
                    .then((res) => res.json())
                    .then((data) => {
                        resp = data;
                    });
            });
    }
</script>

<div class='flex flex-col justify-between items-center h-screen px-10'>
    <div>
        <div class="text-center">
            <div class="flex justify-center space-x-4 py-5">
                <div class="mb-4 text-[#ADD8E6] rounded-lg p-4 text-xl square"></div>
                <div class="mb-4 text-center justify-center bg-red-500 text-white rounded-lg p-4 text-3xl square">
                    <p class="py-2">CPU</p>
                    <button on:click={handleClick} class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 py-1 rounded text-xl">
                        Get memory
                    </button>
                </div>
                <div class="mb-4 text-[#ADD8E6] rounded-lg p-4 text-xl square"></div>
            </div>
            <div class="flex justify-center space-x-4 py-5">
                <div class="flex-none bg-green-500 text-white rounded-lg p-4 text-xl box px-5">
                    <p class="text-xl mb-2">L1 Cache</p>
                    <div class="overflow-y-auto h-32">
                        <table class="w-full">
                            {#each resp["L1_cache"] as line}
                                <tr><td>{line}</td></tr>
                            {/each}
                        </table>
                    </div>
                </div>
                <div class="flex-none bg-blue-500 text-white rounded-lg p-4 text-xl box px-5">
                    <p class="text-xl mb-2">Victim Cache</p>
                    <div class="overflow-y-auto h-32">
                        <table class="w-full">
                            {#each resp["Victim_cache"] as line}
                                <tr><td>{line}</td></tr>
                            {/each}
                        </table>
                    </div>
                </div>
                <div class="flex-none bg-yellow-500 text-white rounded-lg p-4 text-xl box px-5">
                    <p class="text-xl mb-2">L2 Cache</p>
                    <div class="overflow-y-auto h-32">
                        <table class="w-full">
                            {#each resp["L2_cache"] as line}
                                <tr><td>{line}</td></tr>
                            {/each}
                        </table>
                    </div>
                </div>
            </div>
            <div class="mt-4 bg-purple-500 text-white rounded-lg p-4 text-4xl py-2">RAM</div>
        </div>
    </div>
    <div class="flex justify-center mt-2 items-center">
        <p class='px-5'>
            Address: {resp.address}
        </p>
        <p class='px-5'>L1 Cache: -</p>
        <p class='px-5'>Victim Cache: -</p>
        <p class='px-5'>L2 Cache: -</p>
    </div>    
</div>

<style>
    .square {
        width: 150px;
        height: 150px;
    }
    .box {
        width: 500px;
        height: 400px;
    }
</style>
